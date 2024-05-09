package main

import (
	"math/rand/v2"
	"strconv"
)

func GenerateQuestion() (string, string) {
	questionType := rand.IntN(1)
	if questionType == 1 {
		return GenerateSqrtQuestion() // FIXME
	}
	return GenerateSqrtQuestion()
}

func GenerateSqrtQuestion() (string, string) {
	n := rand.IntN(20) + 1
	question := "Solve sqrt " + strconv.Itoa(n*n)
	answer := strconv.Itoa(n)
	return question, answer
}

func GenerateAlgebraQuestion() (string, string) {
	n := rand.IntN(10)
	x := rand.IntN(10)
	question := "Solve " + strconv.Itoa(n) + "x = " + strconv.Itoa(n*x)
	answer := strconv.Itoa(x)
	return question, answer
}
