# Docker Quick Reference

Quick commands for Docker deployment of the Todo App.

## 🚀 Quick Start

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# Stop
docker-compose down

# Stop and remove database
docker-compose down -v
```

## 📦 Build Commands

```bash
# Build image
docker build -t todo-app:latest .

# Build with tag
docker build -t todo-app:v1.0.0 .
```

## 🏃 Run Commands

```bash
# Basic run
docker run -d -p 8000:8000 --name todo-app todo-app:latest

# Run with persistent storage
docker run -d -p 8000:8000 -v $(pwd)/data:/app/data --name todo-app todo-app:latest

# Run with custom secret key
docker run -d -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e SECRET_KEY="your-secret-key" \
  --name todo-app \
  todo-app:latest
```

## 📊 Monitoring

```bash
# View logs
docker logs todo-app
docker logs -f todo-app

# Check status
docker ps
docker stats todo-app

# Health check
docker inspect --format='{{json .State.Health}}' todo-app
```

## 🔧 Troubleshooting

```bash
# Rebuild from scratch
docker-compose down
docker system prune -a
docker-compose build --no-cache
docker-compose up

# Check logs
docker-compose logs -f

# Enter container
docker exec -it todo-app /bin/bash

# Check port
docker port todo-app
```

## 🌐 Access

- **Web App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔒 Security

1. Change `SECRET_KEY` in production:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. Use environment variables:
   ```bash
   export SECRET_KEY="your-generated-key"
   docker-compose up
   ```

## 📚 Full Documentation

See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for complete deployment guide.

