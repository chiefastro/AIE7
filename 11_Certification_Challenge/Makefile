.PHONY: help build run populate clean logs

# Default target
help:
	@echo "Available commands:"
	@echo "  build     - Build the Docker image"
	@echo "  run       - Run the service using Docker Compose"
	@echo "  populate  - Populate the vector database"
	@echo "  clean     - Stop and remove containers"
	@echo "  logs      - View service logs"

# Build the Docker image
build:
	docker-compose build

# Run the service
up:
	docker-compose up

# Populate the vector database
populate:
	docker-compose run --rm mimi-backend uv run python -m mimi.pipe.pipe

# Stop and remove containers
clean:
	docker-compose down

# View service logs
logs:
	docker-compose logs -f mimi-backend

# Run service in foreground (for debugging)
up-background:
	docker-compose up -d

# Run in development mode with hot reload
dev:
	docker-compose up --build

# Rebuild and restart
rebuild: clean build run 