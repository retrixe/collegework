package main

import (
	"time"

	gpio "github.com/stianeikeland/go-rpio/v4"
)

const KEYPAD_R1_PIN = gpio.Pin(21)
const KEYPAD_R2_PIN = gpio.Pin(20)
const KEYPAD_R3_PIN = gpio.Pin(16)
const KEYPAD_R4_PIN = gpio.Pin(26)

const KEYPAD_R1_KEYS = "123A"
const KEYPAD_R2_KEYS = "456B"
const KEYPAD_R3_KEYS = "789C"
const KEYPAD_R4_KEYS = "*0#D"

const KEYPAD_C1_PIN = gpio.Pin(19)
const KEYPAD_C2_PIN = gpio.Pin(13)
const KEYPAD_C3_PIN = gpio.Pin(6)
const KEYPAD_C4_PIN = gpio.Pin(5)

func SetupKeypadPins() {
	KEYPAD_R1_PIN.Output()
	KEYPAD_R2_PIN.Output()
	KEYPAD_R3_PIN.Output()
	KEYPAD_R4_PIN.Output()

	KEYPAD_C1_PIN.Input()
	KEYPAD_C1_PIN.Pull(gpio.PullDown)
	KEYPAD_C2_PIN.Input()
	KEYPAD_C2_PIN.Pull(gpio.PullDown)
	KEYPAD_C3_PIN.Input()
	KEYPAD_C3_PIN.Pull(gpio.PullDown)
	KEYPAD_C4_PIN.Input()
	KEYPAD_C4_PIN.Pull(gpio.PullDown)
}

func PoweroffKeypadPins() {
	KEYPAD_R1_PIN.Low()
	KEYPAD_R2_PIN.Low()
	KEYPAD_R3_PIN.Low()
	KEYPAD_R4_PIN.Low()
}

func pollKeypadRow(row gpio.Pin, keys string) string {
	row.High()
	defer row.Low()
	if KEYPAD_C2_PIN.Read() == gpio.High {
		return string(keys[1])
	} else if KEYPAD_C1_PIN.Read() == gpio.High {
		return string(keys[0])
	} else if KEYPAD_C3_PIN.Read() == gpio.High {
		return string(keys[2])
	} else if KEYPAD_C4_PIN.Read() == gpio.High {
		return string(keys[3])
	}
	return ""
}

func PollKeypad() string {
	if row1 := pollKeypadRow(KEYPAD_R1_PIN, KEYPAD_R1_KEYS); row1 != "" {
		return row1
	} else if row2 := pollKeypadRow(KEYPAD_R2_PIN, KEYPAD_R2_KEYS); row2 != "" {
		return row2
	} else if row3 := pollKeypadRow(KEYPAD_R3_PIN, KEYPAD_R3_KEYS); row3 != "" {
		return row3
	} else if row4 := pollKeypadRow(KEYPAD_R4_PIN, KEYPAD_R4_KEYS); row4 != "" {
		return row4
	}
	return ""
}

func ReadFromKeypad(consumer chan string) {
	defer recover()
	prevInput := ""
	for {
		time.Sleep(2 * time.Millisecond)
		input := PollKeypad()
		time.Sleep(2 * time.Millisecond)
		if input != PollKeypad() { // If input has not held for an extra poll cycle, poll again.
			continue
		}
		if input != "" && input != prevInput {
			consumer <- input
		}
		prevInput = input
	}
}
