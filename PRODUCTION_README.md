# Todo App - Production Deployment

## 🚀 Production-Ready for Azure Kubernetes Service

This application is fully configured for enterprise-grade production deployment on Azure Kubernetes Service (AKS) with:

- **High Availability**: 3-20 auto-scaling pods
- **Security**: Non-root containers, secrets management, TLS
- **Monitoring**: Health checks, structured logging, metrics
- **Reliability**: Rolling updates, graceful shutdown, database connection pooling
- **Performance**: Resource optimization, multi-worker processes

## Quick Start

### Prerequisites

- Azure CLI 2.0+
- kubectl 1.25+
- Helm 3.x
- Docker 20.10+

### 1. Set Up Azure Resources

```bash
# Login
az login

# Create resource group
az group create --name todo-app-rg --location eastus

# Create Azure Container Registry
az acr create --resource-group todo-app-rg --name YOURACRNAME --sku Basic

# Create AKS cluster
az aks create \
  --resource-group todo-app-rg \
  --name todo-app-aks \
  --node-count 3 \
  --enable-addons monitoring \
  --attach-acr YOURACRNAME

# Get credentials
az aks get-credentials --resource-group todo-app-rg --name todo-app-aks
```

### 2. Configure Secrets

```bash
# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update helm/todo-app/values.yaml with your secrets
# OR create manually:
kubectl create secret generic todo-app-secrets \
  --from-literal=secret-key='YOUR_SECRET_KEY' \
  --namespace production
```

### 3. Deploy to AKS

```bash
# Using Helm (recommended)
helm install todo-app ./helm/todo-app \
  --namespace production \
  --create-namespace

# OR using kubectl
kubectl apply -f k8s/
```

### 4. Check Status

```bash
# View pods
kubectl get pods -n production

# View services
kubectl get svc -n production

# View ingress
kubectl get ingress -n production

# Check logs
kubectl logs -f deployment/todo-app -n production
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   Internet                      │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│          NGINX Ingress Controller               │
│      (TLS Termination, Load Balancing)          │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│          Kubernetes Service                     │
│      (ClusterIP, Session Affinity)              │
└────────────────────┬────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Pod 1   │  │  Pod 2   │  │  Pod 3   │
│ Todo App │  │ Todo App │  │ Todo App │
│ (4 sync) │  │ (4 sync) │  │ (4 sync) │
└─────┬────┘  └─────┬────┘  └─────┬────┘
      │             │             │
      └─────────────┼─────────────┘
                    ▼
        ┌──────────────────┐
        │  Azure Database  │
        │  for PostgreSQL  │
        └──────────────────┘
```

## Configuration Files

### Must-Update Files

1. **helm/todo-app/values.yaml**
   - `image.repository`: Your ACR name
   - `ingress.hosts`: Your domain
   - `configMap.database-url`: PostgreSQL connection
   - `secrets.secret-key`: JWT secret

2. **k8s/deployment.yaml**
   - `image`: Your ACR image path

3. **azure-aks-deploy.yml**
   - `AZURE_CONTAINER_REGISTRY_NAME`
   - `AZURE_RESOURCE_GROUP`
   - `AZURE_KUBERNETES_SERVICE_NAME`

## Key Features

### 🔄 Auto-Scaling

Scales from 3-20 pods based on:
- CPU utilization (>70%)
- Memory utilization (>80%)

```bash
kubectl get hpa -n production
```

### 🛡️ Security

- Non-root containers
- Pod security contexts
- Kubernetes Secrets
- TLS encryption
- Network policies ready

### 📊 Monitoring

- Health endpoint: `/health`
- Structured JSON logs
- Azure Monitor integration
- Pod metrics
- Resource tracking

### 🔄 Rolling Updates

Zero-downtime deployments:
```bash
helm upgrade todo-app ./helm/todo-app -n production
```

### 💾 Database

PostgreSQL recommended for production:
- Azure Database for PostgreSQL
- Connection pooling
- Automated backups
- High availability

## Deployment Methods

### Method 1: Helm (Recommended)

```bash
# Install
helm install todo-app ./helm/todo-app -n production --create-namespace

# Upgrade
helm upgrade todo-app ./helm/todo-app -n production

# Rollback
helm rollback todo-app -n production

# Uninstall
helm uninstall todo-app -n production
```

### Method 2: kubectl

```bash
# Deploy
kubectl apply -f k8s/

# Update
kubectl apply -f k8s/deployment.yaml

# Rollback
kubectl rollout undo deployment/todo-app -n production
```

### Method 3: GitHub Actions

Automated CI/CD with:
- Tests
- Docker build
- ACR push
- AKS deployment
- Status checks

## Health Checks

### Built-in Endpoints

- `/health` - Liveness and readiness probe
  - Checks database connection
  - Returns 200 if healthy, 503 if not

### Manual Check

```bash
# From inside cluster
curl http://todo-app-service.health

# External access (through ingress)
curl https://your-domain.com/health
```

## Troubleshooting

### Pods Not Starting

```bash
kubectl describe pod POD_NAME -n production
kubectl logs POD_NAME -n production
kubectl get events -n production --sort-by='.lastTimestamp'
```

### Database Issues

```bash
# Check connection
kubectl exec -it deployment/todo-app -n production -- bash
psql -h DATABASE_HOST -U USER -d DATABASE

# Verify ConfigMap
kubectl get configmap -n production -o yaml
```

### Ingress Problems

```bash
kubectl describe ingress -n production
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
```

### Scaling Issues

```bash
kubectl describe hpa todo-app -n production
kubectl top pods -n production
kubectl top nodes
```

## Resource Limits

Per pod:
- **CPU**: 250m-500m
- **Memory**: 256Mi-512Mi
- **Workers**: 4 Uvicorn workers

Cluster:
- **Min Pods**: 3
- **Max Pods**: 20
- **Target**: 70% CPU, 80% Memory

## Security Best Practices

1. ✅ Use Kubernetes Secrets for sensitive data
2. ✅ Enable TLS on ingress
3. ✅ Regular security updates
4. ✅ Image scanning in ACR
5. ✅ Network policies for pod isolation
6. ✅ RBAC for Kubernetes access
7. ✅ Regular backups
8. ✅ Monitor Azure Security Center

## Cost Optimization

- Use Spot instances for non-critical workloads
- Configure cluster autoscaler
- Use managed PostgreSQL (Azure Database)
- Schedule scaling for dev/staging
- Monitor resource usage

## Backup & Recovery

### Database

```bash
# Manual backup
pg_dump -h HOST -U USER -d DATABASE > backup.sql

# Azure automated backups
az postgres flexible-server backup list \
  --resource-group todo-app-rg \
  --server-name todo-postgres
```

### Kubernetes State

```bash
# Export configuration
kubectl get all,secrets,configmaps -n production -o yaml > backup.yaml
```

## Support Resources

- 📖 [AKS Deployment Guide](AKS_DEPLOYMENT.md)
- 📖 [Docker Deployment](DOCKER_DEPLOYMENT.md)
- 📖 [Deployment Summary](DEPLOYMENT_SUMMARY.md)
- 🔧 [Troubleshooting Guide](AKS_DEPLOYMENT.md#troubleshooting)

## Architecture Decisions

### Why Kubernetes?

- **Scalability**: Horizontal and vertical scaling
- **Reliability**: Self-healing, rolling updates
- **Portability**: Works on any cloud
- **Ecosystem**: Rich tooling and community

### Why AKS?

- **Managed**: Reduces operational overhead
- **Integration**: Native Azure integration
- **Security**: Built-in security features
- **Monitoring**: Azure Monitor integration

### Why PostgreSQL?

- **Reliability**: ACID compliance
- **Scalability**: Handles concurrent users
- **Performance**: Better than SQLite
- **Managed**: Azure Database options

## Next Steps

1. Deploy to staging environment first
2. Perform load testing
3. Set up monitoring alerts
4. Configure backup automation
5. Document runbooks
6. Train team on Kubernetes operations
7. Set up disaster recovery plan

---

**Production-Ready | Scalable | Secure | Monitored** 🎉

