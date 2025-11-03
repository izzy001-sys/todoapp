# Docker Deployment Guide

This guide explains how to build and deploy the Todo App using Docker.

## Prerequisites

- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)

## Quick Start

### 1. Set up environment variables:

Create a `.env` file from the template:
```bash
cp env.example .env
```

Edit `.env` with your configuration values.

### 2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## Building the Docker Image

### Build the image:
```bash
docker build -t todo-app:latest .
```

### Build with specific tag:
```bash
docker build -t todo-app:v1.0.0 .
```

## Running with Docker Compose

### Development mode:
```bash
docker-compose up
```

### Detached mode (background):
```bash
docker-compose up -d
```

### View logs:
```bash
docker-compose logs -f
```

### Stop the application:
```bash
docker-compose down
```

### Stop and remove volumes (deletes database):
```bash
docker-compose down -v
```

## Running with Docker

### Basic run:
```bash
docker run -d -p 8000:8000 --name todo-app todo-app:latest
```

### Run with persistent storage:
```bash
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --name todo-app \
  todo-app:latest
```

### Run with environment file:
```bash
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  --name todo-app \
  todo-app:latest
```

## Production Deployment

### 1. Set Secure Environment Variables

Copy the environment template and configure it:
```bash
cp env.example .env
```

Edit `.env` file with your production values. **Important**: Generate a secure secret key using:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Key settings for production:
- Set `SECRET_KEY` to a strong random value
- Set `APP_ENV=production`
- Set `DEBUG=false`
- Configure `CORS_ORIGINS` with your domain(s)
- Set appropriate `SQLALCHEMY_DATABASE_URL`

### 2. Deploy with Docker Compose

```bash
docker-compose up -d
```

### 3. Check Status

```bash
docker-compose ps
docker-compose logs -f todo-app
```

## Database Persistence

The application uses SQLite database stored in the `./data` directory. This directory is mounted as a Docker volume to ensure data persists across container restarts.

**Important**: Make sure to backup the `./data` directory regularly in production.

## Security Considerations

1. **Change SECRET_KEY**: Always use a strong, randomly generated secret key in production
2. **Use HTTPS**: For production, use a reverse proxy (nginx) with SSL certificates
3. **Database**: Consider upgrading to PostgreSQL for production use
4. **Environment Variables**: Never commit sensitive data to version control
5. **Firewall**: Restrict access to necessary ports only

## Health Checks

The container includes health checks that verify the application is running:
```bash
docker inspect --format='{{json .State.Health}}' todo-app
```

### Expected healthy output:
```json
{
  "Status": "healthy",
  "FailingStreak": 0
}
```

## Monitoring

### View logs:
```bash
docker logs todo-app
docker logs -f todo-app  # Follow logs
```

### Check container status:
```bash
docker ps
docker ps -a  # Include stopped containers
```

### Execute commands in container:
```bash
docker exec -it todo-app /bin/bash
```

### Check resource usage:
```bash
docker stats todo-app
```

## Troubleshooting

### Container won't start:

1. Check logs:
```bash
docker logs todo-app
docker-compose logs todo-app
```

2. Check if port is already in use:
```bash
# On Linux/Mac
netstat -an | grep 8000

# On Windows
netstat -an | findstr 8000
```

3. Verify Docker is running:
```bash
docker info
```

### Database issues:

1. Remove old database and restart:
```bash
docker-compose down -v
docker-compose up
```

2. Check database file permissions:
```bash
ls -la data/
```

### Permission issues:

Fix data directory permissions:
```bash
# Linux/Mac
sudo chown -R $USER:$USER ./data
chmod -R 755 ./data

# Windows (in PowerShell as Administrator)
icacls .\data /grant Users:F /T
```

### Application not accessible:

1. Check if container is running:
```bash
docker ps
```

2. Check port mapping:
```bash
docker port todo-app
```

3. Test from inside container:
```bash
docker exec todo-app curl http://localhost:8000/docs
```

### Build failures:

1. Clear Docker cache and rebuild:
```bash
docker system prune -a
docker-compose build --no-cache
```

2. Check for syntax errors in Dockerfile:
```bash
docker build -t todo-app:test .
```

## Upgrading

To upgrade to a new version:

1. Pull/build new image:
```bash
docker-compose down
docker-compose build --no-cache
```

2. Restart containers:
```bash
docker-compose up -d
```

3. Verify the upgrade:
```bash
docker-compose ps
docker-compose logs -f
```

## Backup and Restore

### Backup database:
```bash
cp -r ./data ./data-backup-$(date +%Y%m%d)
```

### Restore database:
```bash
docker-compose down
cp -r ./data-backup-YYYYMMDD ./data
docker-compose up
```

## Advanced Configuration

### Custom Database Path

Edit `docker-compose.yml`:
```yaml
volumes:
  - /path/to/custom/data:/app/data
```

### Multiple Environment Files

Create environment-specific files:
```bash
docker-compose --env-file .env.production up
```

### Resource Limits

Add to `docker-compose.yml`:
```yaml
services:
  todo-app:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

## Docker Compose Services

The `docker-compose.yml` file includes:

- **todo-app**: Main FastAPI application
- **nginx** (optional): Reverse proxy for production (commented out)

To enable nginx, uncomment the nginx service in `docker-compose.yml` and create an `nginx.conf` file.

## CI/CD Integration

### GitHub Actions Example:

```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t todo-app:${{ github.sha }} .
      - name: Push to registry
        run: docker push your-registry/todo-app:${{ github.sha }}
```

## Cloud Deployment

### AWS ECS / Fargate

1. Push image to ECR
2. Create ECS task definition
3. Create service with health checks

### Google Cloud Run

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/todo-app
gcloud run deploy --image gcr.io/PROJECT_ID/todo-app
```

### Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name todo-app \
  --image todo-app:latest \
  --ports 8000
```

## Support

For issues, questions, or contributions:
- Check logs: `docker-compose logs`
- Review this guide
- Open an issue on GitHub

