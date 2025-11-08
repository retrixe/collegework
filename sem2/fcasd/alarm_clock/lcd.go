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
	// FIXME hacky
	line1 = hex.EncodeToString([]byte(line1))
	line2 = hex.EncodeToString([]byte(line2))
	go func() {
		homeDir, err := os.UserHomeDir()
		if err != nil {
			println(err.Error())
			return
		}
		uvPath := filepath.Join(homeDir, ".local", "bin", "uv")
		err = exec.Command(uvPath, "run", "lcd.py", line1, line2).Run()
		if err != nil {
			println(err.Error())
		}
	}()
}
