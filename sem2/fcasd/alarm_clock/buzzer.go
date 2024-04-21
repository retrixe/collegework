package main

import (
	gpio "github.com/stianeikeland/go-rpio/v4"
)

const BUZZER_PIN = gpio.Pin(12)

func SetupBuzzerPin() {
	BUZZER_PIN.Output()
}

func PoweroffBuzzerPin() {
	BUZZER_PIN.Low()
}

func ActivateBuzzer(stop chan bool) {
	defer BUZZER_PIN.Low()
	BUZZER_PIN.High()
	<-stop
}
