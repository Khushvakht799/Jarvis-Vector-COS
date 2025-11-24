package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"time"
)

type QueryRequest struct {
	Prompt string `json:"prompt"`
}

type QueryResponse struct {
	Answer    string `json:"answer"`
	Prompt    string `json:"prompt"`
	Timestamp string `json:"timestamp"`
	Service   string `json:"service"`
}

// Функция для вызова Python Brain
func callPythonBrain(prompt string) (map[string]interface{}, error) {
	requestBody := map[string]interface{}{
		"prompt":    prompt,
		"context":   map[string]interface{}{},
		"session_id": "go_session",
	}
	
	jsonBody, err := json.Marshal(requestBody)
	if err != nil {
		return nil, fmt.Errorf("JSON marshal error: %v", err)
	}
	
	resp, err := http.Post("http://localhost:8000/process", "application/json", bytes.NewBuffer(jsonBody))
	if err != nil {
		return nil, fmt.Errorf("Python brain unreachable: %v", err)
	}
	defer resp.Body.Close()
	
	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("Python brain error: %s - %s", resp.Status, string(body))
	}
	
	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("Failed to parse brain response: %v", err)
	}
	
	return result, nil
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	response := map[string]string{
		"status":    "OK",
		"service":   "Jarvis Go Service",
		"timestamp": time.Now().Format(time.RFC3339),
	}
	
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	json.NewEncoder(w).Encode(response)
}

func processHandler(w http.ResponseWriter, r *http.Request) {
	// Set CORS headers
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	
	// Handle preflight
	if r.Method == "OPTIONS" {
		w.WriteHeader(http.StatusOK)
		return
	}
	
	if r.Method != "POST" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req QueryRequest
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading body", http.StatusBadRequest)
		return
	}

	if err := json.Unmarshal(body, &req); err != nil {
		log.Printf("JSON parse error: %v, Body: %s", err, string(body))
		http.Error(w, "Invalid JSON: "+err.Error(), http.StatusBadRequest)
		return
	}

	// Call Python Brain
	brainResponse, err := callPythonBrain(req.Prompt)
	if err != nil {
		log.Printf("Brain service error: %v", err)
		// Fallback to basic processing
		response := QueryResponse{
			Answer:    "Processed by Go (Brain unavailable): " + req.Prompt,
			Prompt:    req.Prompt,
			Timestamp: time.Now().Format(time.RFC3339),
			Service:   "Go Processor",
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
		return
	}

	// Enhanced response with brain data
	enhancedResponse := map[string]interface{}{
		"go_service":    "Go Processor",
		"brain_service": "Python Brain",
		"integrated":    true,
		"brain_data":    brainResponse,
		"processed_by":  "Full Cognitive Pipeline",
		"timestamp":     time.Now().Format(time.RFC3339),
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(enhancedResponse)
}

func main() {
	http.HandleFunc("/health", healthHandler)
	http.HandleFunc("/process", processHandler)
	
	port := ":8081"
	log.Printf("🚀 Jarvis Go service running on port %s", port)
	log.Fatal(http.ListenAndServe(port, nil))
}