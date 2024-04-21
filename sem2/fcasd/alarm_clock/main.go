package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"

	gpio "github.com/stianeikeland/go-rpio/v4"
)

func main() {
	gpio.Open()
	defer gpio.Close()

	SetupBuzzerPin()
	defer PoweroffBuzzerPin()
	SetupKeypadPins()
	defer PoweroffKeypadPins()

	// TODO: Setup LCD 2nd line
	// IP: 192.168.1.121

	// Setup alarm thread
	go (func() {
		t := time.Now()
		ticker := time.NewTicker(time.Second)
		var cancel chan bool
		for {
			println(t.String()) // TODO: Display time to LCD
			if IsAlarmSet(t) {
				// Cancel any previous alarms
				if cancel != nil {
					cancel <- true
				}

				cancel = make(chan bool, 1)
				go TriggerAlarm(t, cancel)
			}
			t = <-ticker.C
		}
	})()

	// Setup API
	go RunApi()

	sigc := make(chan os.Signal, 1)
	go signal.Notify(sigc, os.Interrupt, syscall.SIGTERM)
	fmt.Printf("signal %s: shutting down\n", <-sigc)
}
