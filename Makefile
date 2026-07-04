# Makefile for DocMind project

.PHONY: install dev build test docker-up docker-down clean

install:
	# Install backend dependencies
	pip install -r backend/requirements.txt
	# Install frontend dependencies
	cd frontend && npm install

dev:
	# Start development environment
	./scripts/dev.sh

build:
	# Build frontend for production
	cd frontend && npm run build

test:
	# Run backend tests
	pytest backend/tests
	# Run frontend tests
	cd frontend && npm test

docker-up:
	# Start all services using Docker Compose
	docker-compose up --build -d

docker-down:
	# Stop all services
	docker-compose down

clean:
	# Remove all build artifacts and temporary files
	rm -rf backend/__pycache__
	rm -rf frontend/dist
	rm -rf frontend/node_modules
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete