### ERSMS - Task Service

This is the Task Service for managing task creation and retrieval within the ERSMS architecture.  
It offers basic endpoints for system health checks and task management, and is prepared for integration with the API Gateway and other services.

---

### 🛠 How to Run Locally

```bash
uvicorn src.main:app --reload --port 8001
```

---

### 🐳 How to Build & Run with Docker

```bash
docker build -t task-service .
docker run -p 8001:8001 task-service
```

---

### 🌐 Endpoints

| Method | Endpoint     | Description             |
|--------|--------------|-------------------------|
| GET    | /health      | Health check            |
| GET    | /ready       | Readiness check         |
| POST   | /tasks       | Create a new task       |
| GET    | /tasks       | List all created tasks  |

#### ✅ EXAMPLE REQUEST to `/tasks` (POST)

```json
{
  "title": "Finish project",
  "description": "Complete the ERSMS milestone 1"
}
```

#### ✅ EXAMPLE RESPONSE from `/tasks` (GET)

```json
[
  {
    "id": 1,
    "title": "Finish project",
    "description": "Complete the ERSMS milestone 1"
  }
]
```

---

### ⚙️ Environment Variables

None required at this stage.

---

### 📦 Requirements

All dependencies are listed in `requirements.txt`.

Install with:

```bash
pip install -r requirements.txt
```

---

### 🧪 Tests

Run tests using:

```bash
python -m pytest tests/
```

Includes:
- `/health` and `/ready` checks
- Task creation and retrieval

---

### ☁️ Kubernetes Deployment

#### Step 1: Build Docker image

```bash
docker build -t task-service .
```

#### Step 2: Push to Registry

```bash
docker tag task-service <registry>/task-service:latest
docker push <registry>/task-service:latest
```

#### Step 3: Apply Kubernetes manifests

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

⚠️ Replace `<registry>` in `deployment.yaml` with your actual image registry path  
(e.g. `ghcr.io/yourusername/task-service:latest`)

---

### 📁 Project Structure

```
task-service/
├── src/
│   └── main.py
├── tests/
│   └── test_main.py
├── .gitignore
├── requirements.txt
├── Dockerfile
├── kubernetes/
│   ├── deployment.yaml
│   └── service.yaml
└── README.md
```
