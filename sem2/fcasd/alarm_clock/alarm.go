package main

import (
	"time"
)

func IsAlarmSet(t time.Time) bool {
	configMutex.RLock()
	defer configMutex.RUnlock()
	for _, alarm := range config.Alarms {
		if alarm/100 == t.Hour() && alarm%100 == t.Minute() && t.Second() == 0 {
			return true
		}
	}
	return false
}

func TriggerAlarm(t time.Time, cancel chan bool) {
	deactivateBuzzer := make(chan bool)
	go ActivateBuzzer(deactivateBuzzer)

	question, answer := GenerateQuestion()
	time.Sleep(5 * time.Second) // FIXME LCD doesn't behave well on rapid update
	UpdateLCD("", question)
	input := ""
	reader := make(chan string, 16)
	go ReadFromKeypad(reader)
loop:
	for {
		var char string
		select {
		case <-cancel:
			deactivateBuzzer <- true
			break loop
		case char = <-reader:
		}
		if char == "A" || char == "B" || char == "C" || char == "D" {
			if input == answer {
				println("[Debug] Correct input entered, deactivated alarm: " + input)
				deactivateBuzzer <- true
				break loop
			}
			println("[Debug] Incorrect input entered: " + input)
			UpdateLCD("", "Wrong ans!")
			time.Sleep(5 * time.Second)
			UpdateLCD("", question)
			input = ""
		} else {
			input += char
		}
	}
	close(reader)
	time.Sleep(5 * time.Second) // FIXME see above
	UpdateLCD("", GetIP())
}
