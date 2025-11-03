# Azure Kubernetes Service (AKS) Deployment Guide

This guide explains how to deploy the Todo App to Azure Kubernetes Service (AKS) for production.

## Prerequisites

- Azure subscription
- Azure CLI installed
- kubectl installed
- Helm 3.x installed
- Docker installed

## Quick Start

### 1. Set Up Azure Resources

```bash
# Login to Azure
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
  --generate-ssh-keys \
  --attach-acr YOURACRNAME

# Get AKS credentials
az aks get-credentials --resource-group todo-app-rg --name todo-app-aks
```

### 2. Set Up Azure Database for PostgreSQL

```bash
# Create PostgreSQL server
az postgres flexible-server create \
  --resource-group todo-app-rg \
  --name todo-postgres \
  --location eastus \
  --admin-user adminuser \
  --admin-password YOUR_SECURE_PASSWORD \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 14 \
  --storage-size 32

# Create database
az postgres flexible-server db create \
  --resource-group todo-app-rg \
  --server-name todo-postgres \
  --database-name todoapp
```

### 3. Deploy Using Helm

```bash
# Update values
cd helm/todo-app
# Edit values.yaml with your settings

# Deploy
helm install todo-app ./helm/todo-app \
  --namespace production \
  --create-namespace \
  --set image.repository=YOURACRNAME.azurecr.io/todo-app \
  --set configMap.database-url="postgresql://adminuser:YOUR_PASSWORD@todo-postgres.postgres.database.azure.com/todoapp"

# Check status
kubectl get pods -n production
helm status todo-app -n production
```

### 4. Set Up Ingress

```bash
# Install NGINX Ingress Controller
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace

# Get external IP
kubectl get service ingress-nginx-controller --namespace=ingress-nginx

# Point your domain to this IP
```

## Deployment Methods

### Method 1: Using Helm (Recommended)

```bash
# Install
helm install todo-app ./helm/todo-app \
  --namespace production \
  --create-namespace

# Upgrade
helm upgrade todo-app ./helm/todo-app \
  --namespace production

# Uninstall
helm uninstall todo-app -n production
```

### Method 2: Using kubectl

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check status
kubectl get all -n production

# Update deployment
kubectl apply -f k8s/deployment.yaml

# Rollback
kubectl rollout undo deployment/todo-app -n production
```

### Method 3: Using GitHub Actions

1. Set up secrets in GitHub:
   - `AZURE_CREDENTIALS`
   - `AZURE_ACR_USERNAME`
   - `AZURE_ACR_PASSWORD`

2. Push to main branch to trigger deployment

## Configuration

### Update Values.yaml

```yaml
image:
  repository: YOURACRNAME.azurecr.io/todo-app
  tag: "latest"

ingress:
  enabled: true
  hosts:
    - host: todo-app.yourdomain.com

configMap:
  database-url: "postgresql://..."
  cors-origins: "https://todo-app.yourdomain.com"
```

### Create Secrets

```bash
# Base64 encode your secret
echo -n 'your-secret-key' | base64

# Update helm/todo-app/values.yaml with encoded value
# Or use kubectl:
kubectl create secret generic todo-app-secrets \
  --from-literal=secret-key='your-secret-key' \
  -n production
```

## Monitoring

### View Logs

```bash
# Pod logs
kubectl logs -f deployment/todo-app -n production

# All pods
kubectl logs -f -l app=todo-app -n production

# Specific pod
kubectl logs POD_NAME -n production
```

### Check Metrics

```bash
# View pods
kubectl get pods -n production

# View services
kubectl get svc -n production

# View ingress
kubectl get ingress -n production

# HPA status
kubectl get hpa -n production

# Node status
kubectl top nodes
kubectl top pods -n production
```

### Azure Monitor Integration

The deployment includes Azure Monitor integration for:
- Container insights
- Pod metrics
- Application performance monitoring

## Scaling

### Manual Scaling

```bash
# Scale deployment
kubectl scale deployment todo-app --replicas=5 -n production

# Or update Helm values
helm upgrade todo-app ./helm/todo-app \
  --namespace production \
  --set replicaCount=5
```

### Automatic Scaling (HPA)

HPA is configured to scale between 3-20 replicas based on CPU (70%) and memory (80%).

```bash
# View HPA status
kubectl get hpa todo-app -n production

# Describe HPA
kubectl describe hpa todo-app -n production
```

## Troubleshooting

### Pod Not Starting

```bash
# Describe pod
kubectl describe pod POD_NAME -n production

# Check events
kubectl get events -n production --sort-by='.lastTimestamp'

# Check logs
kubectl logs POD_NAME -n production
```

### Image Pull Errors

```bash
# Check ACR credentials
az aks update -n todo-app-aks -g todo-app-rg --attach-acr YOURACRNAME

# Create image pull secret manually
kubectl create secret docker-registry acr-secret \
  --docker-server=YOURACRNAME.azurecr.io \
  --docker-username=YOUR_USERNAME \
  --docker-password=YOUR_PASSWORD \
  -n production
```

### Database Connection Issues

```bash
# Test connection from pod
kubectl exec -it deployment/todo-app -n production -- bash
psql -h your-postgres-host -U your-user -d your-database

# Check ConfigMap
kubectl get configmap todo-app-config -n production -o yaml
```

### Ingress Not Working

```bash
# Check ingress controller
kubectl get pods -n ingress-nginx

# Check ingress
kubectl describe ingress todo-app-ingress -n production

# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
```

## Security

### Key Security Features

1. **Non-root user**: Containers run as non-root
2. **Security contexts**: Configured with Pod Security Standards
3. **Secrets management**: Sensitive data stored in Kubernetes Secrets
4. **Network policies**: Can be added for pod-to-pod communication control
5. **TLS**: Ingress configured with TLS
6. **Image scanning**: Use Azure Security Center or Trivy

### Add Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: todo-app-netpol
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: todo-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    - namespaceSelector:
        matchLabels:
          name: monitoring
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
```

## Cost Optimization

- Use Azure Spot instances for non-critical workloads
- Configure cluster autoscaler
- Use managed PostgreSQL instead of self-hosted
- Enable scheduled scaling for dev/staging

## Backup and Recovery

### Database Backup

```bash
# Manual backup
pg_dump -h HOST -U USER -d DATABASE > backup.sql

# Automated backups
az postgres flexible-server backup list \
  --resource-group todo-app-rg \
  --server-name todo-postgres
```

### Kubernetes Backup

```bash
# Export all resources
kubectl get all -n production -o yaml > backup.yaml

# Backup specific resources
kubectl get secrets,configmaps -n production -o yaml > config-backup.yaml
```

## Support

For issues or questions:
- Check Kubernetes documentation: https://kubernetes.io/docs/
- Azure AKS documentation: https://docs.microsoft.com/azure/aks/
- Application logs: `kubectl logs -f deployment/todo-app -n production`

