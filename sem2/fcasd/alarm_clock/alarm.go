package main

import "time"

func IsAlarmSet(t time.Time) bool {
	configMutex.RLock()
	defer configMutex.RUnlock()
	for _, alarm := range config.Alarms {
		if alarm%100 == t.Hour() && alarm/100 == t.Minute() && t.Second() == 0 {
			return true
		}
	}
	return false
}

func TriggerAlarm(t time.Time, cancel chan bool) {
	deactivateBuzzer := make(chan bool)
	go ActivateBuzzer(deactivateBuzzer)

	// TODO: Display question on 2nd line
	ans := "6743" // TODO: Create a proper question
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
			if input == ans {
				deactivateBuzzer <- true
				break
			} else {
				// TODO: Display wrong answer on 2nd line
			}
		} else {
			input += char
		}
	}
	// TODO: Reset 2nd line
}
