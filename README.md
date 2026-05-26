# SRE Log Analyser

A log analysis system that accepts log entries via REST API, stores them in a database, and uses a local LLM (via Ollama) to explain errors and suggest fixes — built as a portfolio project demonstrating MLOps and SRE engineering skills.

---

## Tech Stack

- **Python 3.13** — core language
- **FastAPI** — REST API framework
- **SQLite** — lightweight relational database for log persistence
- **Ollama (tinyllama/phi3)** — local open source LLM for log analysis
- **Prometheus** — metrics collection and monitoring
- **Docker + Docker Compose** — containerisation
- **Kubernetes (minikube)** — container orchestration

---

## Architecture

A log entry is submitted via the REST API and stored in SQLite. On demand, the `/analyse` endpoint sends the log to a locally running Ollama LLM, which returns an explanation and suggested fix. The analysis is saved back to the database. Prometheus scrapes the `/metrics` endpoint to track log volumes by level and LLM response times.




---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/logs` | Submit a new log entry |
| GET | `/logs` | Retrieve all log entries |
| GET | `/logs/{id}` | Retrieve a specific log entry |
| POST | `/logs/{id}/analyse` | Analyse a log entry using LLM |
| GET | `/metrics` | Prometheus metrics endpoint |
| GET | `/health` | Health check endpoint |

---

## How to Run

### Local Development
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Ollama (in a separate terminal)
ollama serve

# Start the API
uvicorn app.main:app --reload
```
API available at: `http://localhost:8000/docs`

### Docker
```bash
# Ollama must be running natively on your Mac
ollama serve

# Build and start the API container
docker compose up --build
```
API available at: `http://localhost:8000/docs`

### Kubernetes (minikube)
```bash
# Start minikube
minikube start --memory=1800 --cpus=2

# Point Docker to minikube's registry
eval $(minikube docker-env)

# Build image inside minikube
docker build -t sre-log-analyser:latest .

# Deploy
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Get access URL
minikube service sre-log-analyser --url
```

---

## Prometheus Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `sre_logs_total` | Counter | Total number of log entries received |
| `sre_logs_by_level_total` | Counter | Log entries broken down by level (INFO/WARNING/ERROR/CRITICAL) |
| `sre_llm_response_seconds` | Histogram | Time taken for LLM to analyse a log entry |

---

Help Courtesy : Claude for guiding