### ERSMS - Task Service

This is the Task Service for managing task creation and retrieval within the ERSMS architecture. It uses Firebase for authentication and PostgreSQL for data storage.

### 🛠 How to Run Locally

1. **Set up PostgreSQL:**
```bash
# Using Docker
docker run -d \
  --name postgres-tasks \
  -e POSTGRES_DB=tasks_db \
  -e POSTGRES_USER=tasks_user \
  -e POSTGRES_PASSWORD=tasks_password \
  -p 5432:5432 \
  postgres:15-alpine
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your actual values
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the service:**
```bash
uvicorn src.main:app --reload --port 8002
```

---

### 🐳 How to Build & Run with Docker

```bash
docker build -t task-service .
docker run -p 8002:8002 \
  -e DATABASE_URL=postgresql+asyncpg://tasks_user:tasks_password@host.docker.internal:5432/tasks_db \
  task-service
```

---

### 🌐 Endpoints

| Method | Endpoint           | Description                    | Auth Required |
|--------|-------------------|--------------------------------|---------------|
| GET    | /health           | Health check                   | No            |
| GET    | /ready            | Readiness check                | No            |
| POST   | /tasks            | Create a new task              | Yes           |
| GET    | /tasks            | List user's tasks with filters| Yes           |
| GET    | /tasks/{id}       | Get specific task              | Yes           |
| PUT    | /tasks/{id}       | Update specific task           | Yes           |
| DELETE | /tasks/{id}       | Delete specific task           | Yes           |
| GET    | /users/me/stats   | Get user's task statistics     | Yes           |
| GET    | /admin/tasks      | List all tasks (admin)         | Yes           |

---

### 🔐 Authentication

This service expects Firebase authentication tokens in one of two ways:

**Option 1: Authorization Header**
```http
Authorization: Bearer <firebase-id-token>
```

---

### 📝 API Examples

#### ✅ Create Task
```bash
curl -X POST "http://localhost:8002/tasks" \
  -H "Authorization: Bearer <firebase-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API docs",
    "priority": "high",
    "due_date": "2025-06-15T10:00:00Z"
  }'
```

#### ✅ List Tasks with Filters
```bash
curl -X GET "http://localhost:8002/tasks?status=pending&priority=high&page=1&size=10" \
  -H "Authorization: Bearer <firebase-token>"
```

#### ✅ Update Task
```bash
curl -X PUT "http://localhost:8002/tasks/1" \
  -H "Authorization: Bearer <firebase-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "title": "Updated task title"
  }'
```

---

### ⚙️ Environment Variables

| Variable              | Description                    | Default                     |
|----------------------|--------------------------------|-----------------------------|
| `DATABASE_URL`       | PostgreSQL connection string   | postgresql+asyncpg://...    |
| `SERVICE_PORT`       | Port to run the service        | 8002                        |
| `FIREBASE_PROJECT_ID`| Firebase project ID            | ""                          |
| `GATEWAY_API_URL`    | API Gateway URL                | http://localhost:8000       |
| `USER_SERVICE_URL`   | User service URL               | http://localhost:8001       |
| `DEBUG`              | Enable debug mode              | true                        |

---

### 🗄️ Database Schema

**Tasks Table:**
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    user_id VARCHAR(128) NOT NULL,  -- Firebase UID
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    due_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
```

---

### 🧪 Testing

**Run Tests:**
```bash
python -m pytest tests/ -v
```

**Test with curl:**
```bash
# Health check
curl http://localhost:8002/health

# Create test task (requires token)
curl -X POST "http://localhost:8002/tasks" \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "priority": "low"}'
```

---

### 📁 Project Structure

```
task-service/
├── src/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database connection
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── services.py      # Business logic
│   └── auth.py          # Firebase authentication
├── tests/
│   └── test_main.py     # API tests
├── Dockerfile          # Container definition
├── requirements.txt    # Python dependencies
└── README.md          # This file
```
