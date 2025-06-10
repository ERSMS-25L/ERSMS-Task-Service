test:
	python -m pytest tests/ -v

docker:
	docker-compose up --build

docker-standalone:
	docker build -t task-service .
	docker run -p 8002:8002 -e DATABASE_URL=postgresql+asyncpg://tasks_user:tasks_password@host.docker.internal:5432/tasks_db task-service

docker-fresh: test
	docker build -t task-service .

docker-test:
	docker build -t task-service-test --target test .
	docker run --rm task-service-test

docker-down:
	docker-compose down

docker-clean:
	docker-compose down -v
	docker system prune -f

.PHONY: test docker docker-standalone docker-fresh deploy docker-test docker-down docker-clean