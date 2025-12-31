# Phase IV: Cloud-Native Kubernetes Deployment

Deploy the Todo AI Chatbot application to local Kubernetes using Minikube with production-grade patterns: multi-stage Docker builds, Helm charts, Dapr service mesh, NGINX ingress, and comprehensive security controls.

## 📋 Overview

This phase implements a complete Kubernetes deployment pipeline with:
- **3 containerized services**: Frontend (Next.js), Backend (FastAPI), MCP Server (FastMCP)
- **Helm package management**: Environment-specific configuration (dev/prod)
- **Dapr service mesh**: mTLS encryption, state management, observability
- **Security-first**: RBAC, NetworkPolicies, non-root containers, resource limits
- **AI-assisted DevOps**: Gordon (Docker optimization), kubectl-ai, kagent

## 🚀 Quick Start

### Prerequisites

Install required tools (one-time setup):

```bash
# Docker Desktop (v4.53+)
# Download from: https://www.docker.com/products/docker-desktop

# Minikube
# macOS: brew install minikube
# Windows: choco install minikube
# Linux: curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Helm 3.x
# macOS: brew install helm
# Windows: choco install kubernetes-helm
# Linux: curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# kubectl
# macOS: brew install kubectl
# Windows: choco install kubernetes-cli
# Linux: curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Dapr CLI (v1.12+)
# macOS: brew install dapr/tap/dapr-cli
# Windows: powershell -Command "iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex"
# Linux: wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
```

### Automated Deployment

Use the provided scripts for a streamlined deployment:

```bash
cd phase-4

# 1. Setup Minikube cluster with all prerequisites
./scripts/setup-minikube.sh

# 2. Build Docker images in Minikube context
./scripts/build-images.sh

# 3. Deploy application with Helm
./scripts/deploy.sh

# 4. Access the application
# Open in browser: http://todo.local
```

### Manual Deployment

For step-by-step deployment, see [quickstart.md](../specs/005-phase4-k8s-deployment/quickstart.md).

## 📁 Project Structure

```
phase-4/
├── backend/                   # FastAPI backend
│   ├── .dockerignore          # Docker build exclusions
│   ├── Dockerfile             # Multi-stage Python build
│   └── src/                   # Application code (from phase-3)
│
├── frontend/                  # Next.js frontend
│   ├── .dockerignore          # Docker build exclusions
│   ├── Dockerfile             # Multi-stage Node build
│   └── src/                   # Application code (from phase-3)
│
├── mcp-server/                # FastMCP server
│   ├── .dockerignore          # Docker build exclusions
│   ├── Dockerfile             # Multi-stage Python build
│   └── src/                   # MCP tools (from phase-3)
│
├── charts/                    # Helm package definitions
│   └── todo-app/
│       ├── Chart.yaml         # Chart metadata
│       ├── values.yaml        # Production defaults
│       ├── values-dev.yaml    # Minikube overrides
│       └── templates/
│           ├── _helpers.tpl   # Template helpers
│           ├── frontend/      # Frontend K8s resources
│           ├── backend/       # Backend K8s resources
│           ├── mcp-server/    # MCP Server K8s resources
│           ├── security/      # NetworkPolicies
│           └── dapr/          # Dapr components
│
├── k8s/                       # Base Kubernetes resources
│   ├── namespace.yaml         # Todo namespace
│   └── secrets-template.yaml # Secret structure
│
├── scripts/                   # Automation scripts
│   ├── setup-minikube.sh      # Cluster initialization
│   ├── build-images.sh        # Docker build automation
│   ├── deploy.sh              # Helm install/upgrade
│   └── cleanup.sh             # Resource cleanup
│
└── README.md                  # This file
```

## 🛠️ Architecture

### Components

1. **Frontend** (Next.js 15 App Router)
   - Port: 3000
   - Image: `todo-frontend:1.0.0` (< 200MB)
   - Ingress: http://todo.local
   - Replicas: 1 (dev), 3 (prod)

2. **Backend** (FastAPI + UV)
   - Port: 8000
   - Image: `todo-backend:1.0.0` (< 300MB)
   - Dapr-enabled: mTLS, state management
   - Replicas: 1 (dev), 3 (prod)

3. **MCP Server** (FastMCP)
   - Port: 8080
   - Image: `todo-mcp-server:1.0.0` (< 200MB)
   - Provides AI tools for backend
   - Replicas: 1 (dev), 2 (prod)

### Security Features

- **Non-root containers**: All run as UID 1000
- **Read-only filesystems**: Prevents runtime modifications
- **Resource limits**: CPU/memory caps prevent resource exhaustion
- **RBAC**: Minimal permissions per service account
- **NetworkPolicies**: Default deny, explicit allow rules
- **Secrets management**: Credentials from Kubernetes Secrets
- **Image security**: Specific version tags (never "latest")

### Network Flow

```
Internet
    ↓
NGINX Ingress (todo.local)
    ↓
Frontend :3000
    ↓
Backend :8000 (Dapr sidecar)
    ↓
├─ MCP Server :8080
├─ Redis :6379 (Dapr state)
└─ PostgreSQL :5432 (Neon, external)
```

## 📊 Resource Allocation

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Frontend  | 100m        | 500m      | 128Mi          | 256Mi        |
| Backend   | 200m        | 1000m     | 256Mi          | 512Mi        |
| MCP Server| 100m        | 500m      | 128Mi          | 256Mi        |
| Dapr Sidecar | 100m     | 300m      | 128Mi          | 256Mi        |
| **Total (dev)** | **500m** | **2300m** | **640Mi**   | **1280Mi**   |

**Minikube Requirements**: 4 CPU, 8GB RAM

## 🧪 Verification

After deployment, verify all components:

```bash
# Check pods
kubectl get pods -n todo
# Expected: frontend-*, backend-*, mcp-server-* all Running (2/2 for backend with Dapr)

# Check services
kubectl get svc -n todo

# Check ingress
kubectl get ing -n todo

# Check Dapr
dapr status -k

# Test frontend
curl -I http://todo.local
# Expected: HTTP/1.1 200 OK

# Test backend health
kubectl port-forward -n todo svc/todo-app-backend 8000:8000
curl http://localhost:8000/health
```

## 🐛 Troubleshooting

### Pods not starting

```bash
# Check pod logs
kubectl logs -n todo <pod-name>

# Check pod events
kubectl describe pod -n todo <pod-name>

# Check Dapr sidecar logs
kubectl logs -n todo <backend-pod> -c daprd
```

### Image pull errors

```bash
# Verify images in Minikube
eval $(minikube docker-env)
docker images | grep todo

# Rebuild if missing
./scripts/build-images.sh
```

### Ingress not accessible

```bash
# Check ingress addon enabled
minikube addons list | grep ingress

# Verify DNS entry
cat /etc/hosts | grep todo.local

# Get Minikube IP
minikube ip
```

### NetworkPolicy blocking traffic

```bash
# Check network policies
kubectl get networkpolicy -n todo

# Temporarily disable for debugging
kubectl delete networkpolicy -n todo --all

# Redeploy to restore
helm upgrade todo-app ./charts/todo-app -f charts/todo-app/values-dev.yaml -n todo
```

## 🔄 Upgrade & Rollback

### Upgrade application

```bash
# Update image tags in values-dev.yaml
# Then upgrade
helm upgrade todo-app ./charts/todo-app -f charts/todo-app/values-dev.yaml -n todo --wait

# Check rollout status
kubectl rollout status deployment/todo-app-backend -n todo
```

### Rollback to previous version

```bash
# View release history
helm history todo-app -n todo

# Rollback to previous
helm rollback todo-app -n todo

# Rollback to specific revision
helm rollback todo-app 2 -n todo
```

## 🧹 Cleanup

Remove all deployed resources:

```bash
# Quick cleanup
./scripts/cleanup.sh --yes

# Full cleanup (includes Docker images)
./scripts/cleanup.sh --yes --full

# Keep Minikube running
./scripts/cleanup.sh --yes --keep-minikube
```

## 📚 Additional Resources

- **Specification**: [specs/005-phase4-k8s-deployment/spec.md](../specs/005-phase4-k8s-deployment/spec.md)
- **Implementation Plan**: [specs/005-phase4-k8s-deployment/plan.md](../specs/005-phase4-k8s-deployment/plan.md)
- **Task List**: [specs/005-phase4-k8s-deployment/tasks.md](../specs/005-phase4-k8s-deployment/tasks.md)
- **Quickstart Guide**: [specs/005-phase4-k8s-deployment/quickstart.md](../specs/005-phase4-k8s-deployment/quickstart.md)

## 🎯 Success Criteria

- ✅ All pods Running/Ready within 5 minutes
- ✅ Frontend accessible at http://todo.local with < 3s page load
- ✅ End-to-end chat functionality working (< 10s response time)
- ✅ All security controls active (RBAC, NetworkPolicies, non-root)
- ✅ Dapr mTLS enabled for 100% service-to-service communication
- ✅ Data persists across pod restarts
- ✅ Database connections use SSL/TLS encryption
- ✅ Container images meet size targets

## 📝 License

This deployment configuration is part of the Todo AI Chatbot project.
