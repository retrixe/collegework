package main

import (
	"context"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/websocket"
	"github.com/segmentio/kafka-go"
	"github.com/shirou/gopsutil/v4/cpu"
	"github.com/shirou/gopsutil/v4/mem"
	"github.com/shirou/gopsutil/v4/net"
)

const OCTYNE_USERNAME = "red"
const OCTYNE_PASSWORD = "velvet"
const OCTYNE_URL = "http://localhost:42069"
const OCTYNE_WS_URL = "ws://localhost:42069"
const OCTYNE_PROXY = "BungeeCord"

func loginOctyne() string {
	// Log into Octyne
	loginReq, err := http.NewRequest("GET", OCTYNE_URL+"/login", nil)
	if err != nil {
		log.Fatalln("failed to create login request:", err)
	}
	loginReq.Header.Add("username", OCTYNE_USERNAME)
	loginReq.Header.Add("password", OCTYNE_PASSWORD)
	res, err := http.DefaultClient.Do(loginReq)
	if err != nil || res.StatusCode != 200 {
		log.Fatalln("failed to log in:", err)
	}
	defer res.Body.Close()
	body, err := io.ReadAll(res.Body)
	if err != nil {
		log.Fatalln("failed to read response body:", err)
	}
	parsed := make(map[string]string)
	err = json.Unmarshal(body, &parsed)
	if err != nil {
		log.Fatalln("failed to parse login response:", err)
	}
	return parsed["token"]
}

func main() {
	// Connect to Octyne WebSocket
	octyneToken := loginOctyne()
	octyneConn, _, err := websocket.DefaultDialer.Dial(OCTYNE_WS_URL+"/server/"+OCTYNE_PROXY+"/console",
		http.Header{
			"Authorization":          []string{octyneToken},
			"Sec-WebSocket-Protocol": []string{"console-v2"},
		})
	if err != nil {
		log.Fatalln("dial:", err)
	}
	defer octyneConn.Close()

	// Connect to Kafka server-logs
	kafkaServerLogsConn, err := kafka.DialLeader(context.Background(), "tcp", "localhost:9092", "server-logs", 0)
	if err != nil {
		log.Fatalln("failed to dial leader:", err)
	}
	defer kafkaServerLogsConn.Close()

	// Connect to Kafka system-utilisation
	kafkaSystemUtilisationConn, err := kafka.DialLeader(context.Background(), "tcp", "localhost:9092", "system-utilisation", 0)
	if err != nil {
		log.Fatalln("failed to dial leader:", err)
	}
	defer kafkaSystemUtilisationConn.Close()

	// Send system utilisation data to Kafka
	go func() {
		for {
			cpuUsage, err := cpu.Percent(0, false)
			if err != nil {
				log.Fatalln("failed to get CPU usage:", err)
				continue
			}
			memUsage, err := mem.VirtualMemory()
			if err != nil {
				log.Fatalln("failed to get memory usage:", err)
				continue
			}
			memoryUsage := (1 - float64(memUsage.Available)/float64(memUsage.Total)) * 100
			networkIn, networkOut, err := GetNetworkIO()
			if err != nil {
				log.Fatalln("failed to get network usage:", err)
				continue
			}
			jsonData, err := json.Marshal(map[string]interface{}{
				"timestamp":   time.Now().Format(time.RFC3339),
				"cpu_percent": cpuUsage[0],
				"mem_percent": memoryUsage,
				"mem_used":    memUsage.Total - memUsage.Available,
				"network_in":  networkIn,
				"network_out": networkOut,
			})
			if err != nil {
				log.Fatalln("failed to marshal JSON:", err)
				continue
			}
			kafkaSystemUtilisationConn.SetWriteDeadline(time.Now().Add(10 * time.Second))
			_, err = kafkaSystemUtilisationConn.WriteMessages(kafka.Message{Value: jsonData})
			if err != nil {
				log.Fatalln("failed to write message:", err)
			}
			time.Sleep(10 * time.Second)
		}
	}()

	// Send Octyne console output to Kafka
	messages := make(chan []byte, 100)
	go func() {
		firstOutput := true
		for {
			_, message, err := octyneConn.ReadMessage()
			if err != nil {
				log.Fatalln("read:", err)
			}
			parsed := make(map[string]string)
			err = json.Unmarshal(message, &parsed)
			if err != nil {
				log.Fatalln("failed to parse message:", err)
			}
			if parsed["type"] != "output" {
				continue
			} else if firstOutput {
				firstOutput = false
				continue
			}
			jsonData, err := json.Marshal(map[string]string{"log": parsed["data"], "timestamp": time.Now().Format(time.RFC3339)})
			if err != nil {
				log.Fatalln("failed to marshal JSON:", err)
			}
			messages <- jsonData
		}
	}()

	for {
		select {
		case msg := <-messages:
			println("Received message: " + string(msg))
			kafkaServerLogsConn.SetWriteDeadline(time.Now().Add(10 * time.Second))
			_, err := kafkaServerLogsConn.WriteMessages(kafka.Message{Value: msg})
			if err != nil {
				log.Fatalln("failed to write message:", err)
			}
		case <-time.After(10 * time.Second):
			err := octyneConn.WriteMessage(websocket.TextMessage, []byte("{\"type\":\"ping\",\"id\":\""+time.Now().String()+"\"}"))
			if err != nil {
				log.Fatalln("ping:", err)
			}
		}
	}
}

var prevNetworkIn, prevNetworkOut = uint64(0), uint64(0)
var timeInterval time.Time

func GetNetworkIO() (in uint64, out uint64, err error) {
	ioCounters, err := net.IOCounters(false)
	if err != nil {
		log.Fatalln("failed to get network usage:", err)
		return 0, 0, err
	}
	networkIn, networkOut := uint64(0), uint64(0)
	for i := range ioCounters {
		networkIn += ioCounters[i].BytesRecv
		networkOut += ioCounters[i].BytesSent
	}
	timeDiff := time.Since(timeInterval).Seconds()
	in = (networkIn - prevNetworkIn) / uint64(timeDiff)
	out = (networkOut - prevNetworkOut) / uint64(timeDiff)
	prevNetworkIn, prevNetworkOut = networkIn, networkOut
	timeInterval = time.Now()
	return in, out, nil
}
