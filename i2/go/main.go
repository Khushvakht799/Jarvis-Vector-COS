package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "io/ioutil"
)

type TaskRequest struct {
    TaskId string `json:"task_id"`
    Intent string `json:"intent"`
}

type TaskResult struct {
    TaskId string `json:"task_id"`
    Status string `json:"status"`
    Logs   string `json:"logs"`
}

func executeHandler(w http.ResponseWriter, r *http.Request) {
    body, _ := ioutil.ReadAll(r.Body)
    var req TaskRequest
    json.Unmarshal(body, &req)
    fmt.Printf("I2 (Go) received task: %s\n", req.TaskId)
    res := TaskResult{TaskId: req.TaskId, Status: "completed", Logs: "demo log"}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(res)
}

func main() {
    http.HandleFunc("/i2/execute", executeHandler)
    fmt.Println("I2 Go stub listening on :8080")
    http.ListenAndServe(":8080", nil)
}
