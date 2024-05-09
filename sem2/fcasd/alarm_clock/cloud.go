package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"sync"
)

type Config struct {
	Password string `json:"password"`
	Alarms   []int  `json:"alarms"`
}

var config Config = Config{Password: "password", Alarms: []int{}}
var configMutex sync.RWMutex

func LoadConfig() {
	configMutex.Lock()
	defer configMutex.Unlock()
	data, err := os.ReadFile("config.json")
	if err != nil && !os.IsNotExist(err) {
		log.Println("Failed to read config file: ", err)
	} else if os.IsNotExist(err) {
		return
	}
	err = json.Unmarshal(data, &config)
	if err != nil {
		log.Println("Failed to unmarshal config: ", err)
	}
}

func SaveConfig() {
	data, err := json.Marshal(config)
	if err != nil {
		log.Println("Failed to marshal config: ", err)
	}
	err = os.WriteFile("config.json", data, 0644)
	if err != nil {
		log.Println("Failed to save config: ", err)
	}
}

func GetIP() string {
	cmd := exec.Command("hostname", "-I")
	output, _ := cmd.Output()
	return strings.TrimSpace(strings.Split(string(output), " ")[0])
}

func RunApi() {
	http.HandleFunc("GET /", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "webui/login.html")
	})
	http.HandleFunc("GET /login.html", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "webui/login.html")
	})
	http.HandleFunc("GET /dashboard.html", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "webui/dashboard.html")
	})

	http.HandleFunc("POST /password", func(w http.ResponseWriter, r *http.Request) {
		configMutex.Lock()
		defer configMutex.Unlock()
		if r.Header.Get("Authorization") != config.Password {
			http.Error(w, "unauthorized", http.StatusUnauthorized)
			return
		}
		password := r.URL.Query().Get("password")
		if password == "" {
			http.Error(w, "password is required", http.StatusBadRequest)
			return
		}
		config.Password = password
		SaveConfig()
		w.Write([]byte("{\"success\":true}\n"))
	})

	http.HandleFunc("GET /alarms", func(w http.ResponseWriter, r *http.Request) {
		configMutex.RLock()
		defer configMutex.RUnlock()
		if r.Header.Get("Authorization") != config.Password {
			http.Error(w, "unauthorized", http.StatusUnauthorized)
			return
		}
		json.NewEncoder(w).Encode(config.Alarms)
	})

	http.HandleFunc("POST /alarm", func(w http.ResponseWriter, r *http.Request) {
		configMutex.Lock()
		defer configMutex.Unlock()
		if r.Header.Get("Authorization") != config.Password {
			http.Error(w, "unauthorized", http.StatusUnauthorized)
			return
		}
		alarm := r.URL.Query().Get("alarm")
		if alarm == "" {
			http.Error(w, "alarm is required", http.StatusBadRequest)
			return
		}
		a, err := strconv.Atoi(alarm)
		if err != nil {
			http.Error(w, "alarm must be an integer", http.StatusBadRequest)
			return
		}
		for _, aa := range config.Alarms {
			if aa == a {
				http.Error(w, "alarm already exists", http.StatusBadRequest)
				return
			}
		}
		config.Alarms = append(config.Alarms, a)
		SaveConfig()
		w.Write([]byte("{\"success\":true}\n"))
	})

	http.HandleFunc("DELETE /alarm", func(w http.ResponseWriter, r *http.Request) {
		configMutex.Lock()
		defer configMutex.Unlock()
		if r.Header.Get("Authorization") != config.Password {
			http.Error(w, "unauthorized", http.StatusUnauthorized)
			return
		}
		alarm := r.URL.Query().Get("alarm")
		if alarm == "" {
			http.Error(w, "alarm is required", http.StatusBadRequest)
			return
		}
		success := "false"
		for i, a := range config.Alarms {
			if strconv.Itoa(a) == alarm {
				success = "true"
				config.Alarms = append(config.Alarms[:i], config.Alarms[i+1:]...)
				break
			}
		}
		SaveConfig()
		w.Write([]byte("{\"success\":" + success + "}\n"))
	})

	println("Starting server on port 8080")
	http.ListenAndServe(":8080", nil)
}
