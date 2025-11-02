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
	LoadConfig()
	SaveConfig()

	gpio.Open()
	defer gpio.Close()

	SetupBuzzerPin()
	defer PoweroffBuzzerPin()
	SetupKeypadPins()
	defer PoweroffKeypadPins()

	LcdLineTwo = GetIP()

	// Setup alarm thread
	go (func() {
		t := time.Now()
		ticker := time.NewTicker(time.Second)
		var cancel chan bool
		for {
			UpdateLCD("    "+t.Format("03:04 PM"), "")
			if IsAlarmSet(t) {
				// Cancel any previous alarms
				if cancel != nil {
					cancel <- true
				}

				cancel = make(chan bool, 1)
				go TriggerAlarm(t, cancel)
			} else if cancel == nil {
				// Update the IP every second
				UpdateLCD("", GetIP())
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
