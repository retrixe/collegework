package main

import (
	"encoding/hex"
	"os"
	"os/exec"
	"path/filepath"
	"sync"
)

var LcdLineOne = ""
var LcdLineTwo = ""
var LcdMutex sync.Mutex

func UpdateLCD(line1 string, line2 string) {
	LcdMutex.Lock()
	defer LcdMutex.Unlock()
	// If no change, drop update.
	if (line1 == "" || line1 == LcdLineOne) && (line2 == "" || line2 == LcdLineTwo) {
		return
	}

	if line1 == "" {
		line1 = LcdLineOne
	} else {
		LcdLineOne = line1
	}
	if line2 == "" {
		line2 = LcdLineTwo
	} else {
		LcdLineTwo = line2
	}

	// Pass to python
	line1 = hex.EncodeToString([]byte(line1))
	line2 = hex.EncodeToString([]byte(line2))
	pwd, _ := os.Getwd()
	pythonPath := filepath.Join(pwd, "venv/bin/python")
	lcdControlPath := filepath.Join(pwd, "python/lcd.py")
	go exec.Command(pythonPath, lcdControlPath, line1, line2).Run() // FIXME hacky
}
