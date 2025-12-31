# Quickstart Guide: Phase IV Kubernetes Deployment

**Feature**: Cloud-Native Kubernetes Deployment  
**Date**: 2025-12-31  
**Audience**: Developers with basic Kubernetes knowledge  
**Time to Complete**: 30-45 minutes

---

## Prerequisites

Before starting, ensure you have these tools installed:

| Tool | Version | Installation |
|------|---------|--------------|
| Docker Desktop | 4.53+ | https://www.docker.com/products/docker-desktop |
| Minikube | Latest | `brew install minikube` (Mac) / `choco install minikube` (Windows) |
| Helm | 3.x | `brew install helm` (Mac) / `choco install kubernetes-helm` (Windows) |
| kubectl | Latest | Installed with Docker Desktop |
| Dapr CLI | Latest | https://docs.dapr.io/getting-started/install-dapr-cli/ |

**Optional (AI-assisted DevOps)**:
- Gordon (Docker AI): Included with Docker Desktop 4.53+
- kubectl-ai: `brew install kubectl-ai` or https://github.com/sozercan/kubectl-ai
- kagent: https://github.com/jina-ai/kagent

---

## Step 1: Start Minikube

```bash
# Start Minikube with adequate resources
minikube start --cpus=4 --memory=8192 --driver=docker

# Verify cluster is running
kubectl cluster-info

# Expected output:
# Kubernetes control plane is running at https://127.0.0.1:xxxxx
```

**Troubleshooting**:
- If Minikube fails to start, ensure Docker Desktop is running
- Check available resources: `docker info | grep -E 'CPUs|Total Memory'`
- Delete and retry: `minikube delete && minikube start --cpus=4 --memory=8192`

---

## Step 2: Enable Minikube Addons

```bash
# Enable NGINX Ingress Controller
minikube addons enable ingress

# Enable Metrics Server (for resource monitoring)
minikube addons enable metrics-server

# Verify addons
minikube addons list | grep -E 'ingress|metrics-server'

# Expected output:
# | ingress                     | minikube | enabled ✅       |
# | metrics-server              | minikube | enabled ✅       |
```

---

## Step 3: Install Dapr on Kubernetes

```bash
# Initialize Dapr on cluster
dapr init -k --wait

# Verify Dapr installation
dapr status -k

# Expected output:
# NAME                   NAMESPACE    HEALTHY  STATUS   REPLICAS  VERSION  AGE  CREATED
# dapr-dashboard         dapr-system  True     Running  1         1.12.0   30s  2025-12-31 00:00.00
# dapr-sidecar-injector  dapr-system  True     Running  1         1.12.0   30s  2025-12-31 00:00.00
# dapr-sentry            dapr-system  True     Running  1         1.12.0   30s  2025-12-31 00:00.00
# dapr-operator          dapr-system  True     Running  1         1.12.0   30s  2025-12-31 00:00.00
# dapr-placement-server  dapr-system  True     Running  1         1.12.0   30s  2025-12-31 00:00.00

# Check all Dapr pods are running
kubectl get pods -n dapr-system
```

**Troubleshooting**:
- If init fails: `dapr uninstall -k && dapr init -k --wait`
- Check pod logs: `kubectl logs -n dapr-system <pod-name>`

---

## Step 4: Configure Local DNS

```bash
# Get Minikube IP
minikube ip

# Add to /etc/hosts (Mac/Linux)
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts

# Windows: Add to C:\Windows\System32\drivers\etc\hosts
# <minikube-ip> todo.local

# Verify DNS resolution
ping todo.local -c 3
```

---

## Step 5: Build Docker Images

```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Verify you're using Minikube's Docker
docker ps | grep -i kube

# Navigate to repository root
cd /path/to/hackathon-todo

# Build frontend image
docker build -t todo-frontend:1.0.0 -f phase-4/frontend/Dockerfile phase-4/frontend

# Build backend image
docker build -t todo-backend:1.0.0 -f phase-4/backend/Dockerfile phase-4/backend

# Verify images exist in Minikube
docker images | grep todo

# Expected output:
# todo-frontend    1.0.0    abc123def456    2 minutes ago    180MB
# todo-backend     1.0.0    def456abc789    1 minute ago     290MB
```

**Using Gordon (Docker AI) - Optional**:
```bash
# Optimize backend Dockerfile
docker ai "analyze image size for todo-backend:1.0.0 and suggest optimizations"

# Generate .dockerignore
docker ai "create .dockerignore for Python FastAPI project with UV package manager"
```

---

## Step 6: Create Namespace

```bash
# Create dedicated namespace
kubectl create namespace todo

# Verify namespace
kubectl get namespaces | grep todo

# Set as default context (optional, for convenience)
kubectl config set-context --current --namespace=todo
```

---

## Step 7: Create Kubernetes Secrets

```bash
# Create secret with database credentials and API keys
kubectl create secret generic todo-secrets \
  --from-literal=database-url="postgresql://user:password@host.com/dbname?sslmode=require" \
  --from-literal=openai-api-key="sk-your-openai-api-key" \
  --from-literal=better-auth-secret="your-32-char-secret-key" \
  -n todo

# Verify secret created
kubectl get secrets -n todo

# Expected output:
# NAME           TYPE     DATA   AGE
# todo-secrets   Opaque   3      5s

# IMPORTANT: Never commit secrets to Git!
# Add .env or secret files to .gitignore
```

**Environment Variables Needed**:
- `DATABASE_URL`: Your Neon PostgreSQL connection string (from Phase 2/3)
- `OPENAI_API_KEY`: Your OpenAI API key (from Phase 3)
- `BETTER_AUTH_SECRET`: Random 32+ character string (generate with `openssl rand -hex 32`)

---

## Step 8: Deploy with Helm

```bash
# Navigate to Helm chart directory
cd phase-4/charts/todo-app

# Lint the chart
helm lint .

# Expected output: No errors or warnings

# Perform dry-run to validate
helm install todo-app . \
  -f values-dev.yaml \
  -n todo \
  --dry-run --debug

# Review the output for any issues

# Deploy to cluster
helm install todo-app . \
  -f values-dev.yaml \
  -n todo \
  --wait \
  --timeout 5m \
  --atomic

# Expected output:
# NAME: todo-app
# LAST DEPLOYED: <timestamp>
# NAMESPACE: todo
# STATUS: deployed
# REVISION: 1
```

**What `--atomic` does**:
- Waits for all pods to be ready
- Automatically rolls back if deployment fails
- Ensures clean state (deployed or nothing)

---

## Step 9: Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n todo

# Expected output (may take 1-2 minutes):
# NAME                        READY   STATUS    RESTARTS   AGE
# frontend-5d7c8b9f6d-abc12   1/1     Running   0          1m
# backend-7f8d9c6b5a-def34    2/2     Running   0          1m

# Note: Backend has 2/2 (app + Dapr sidecar)

# Check services
kubectl get svc -n todo

# Expected output:
# NAME           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
# frontend-svc   ClusterIP   10.96.100.10    <none>        3000/TCP   1m
# backend-svc    ClusterIP   10.96.100.20    <none>        8000/TCP   1m

# Check ingress
kubectl get ingress -n todo

# Expected output:
# NAME           CLASS   HOSTS        ADDRESS          PORTS   AGE
# todo-ingress   nginx   todo.local   192.168.49.2     80      1m

# Check Dapr components
dapr components -k -n todo

# Expected output:
# NAMESPACE  NAME        TYPE          VERSION  SCOPES         CREATED              AGE
# todo       statestore  state.redis   v1       todo-backend   2025-12-31 00:00.00  1m
```

---

## Step 10: Access the Application

```bash
# Option 1: Direct browser access
open http://todo.local

# Option 2: Using curl
curl -I http://todo.local

# Expected HTTP response:
# HTTP/1.1 200 OK
# Server: nginx
# Content-Type: text/html

# Option 3: Using kubectl port-forward (if ingress not working)
kubectl port-forward -n todo svc/frontend-svc 3000:3000

# Then access: http://localhost:3000
```

**What you should see**:
- Todo AI Chatbot interface loads
- Chat functionality works end-to-end
- Tasks can be created, updated, deleted via chat

---

## Step 11: Monitor and Debug

```bash
# View logs from frontend
kubectl logs -n todo -l app=frontend --tail=50 -f

# View logs from backend (app container)
kubectl logs -n todo -l app=backend -c backend --tail=50 -f

# View logs from Dapr sidecar
kubectl logs -n todo -l app=backend -c daprd --tail=50 -f

# Check resource usage
kubectl top pods -n todo

# Expected output:
# NAME                        CPU(cores)   MEMORY(bytes)
# frontend-xxx                50m          150Mi
# backend-xxx                 180m         350Mi

# Describe a pod for detailed info
kubectl describe pod -n todo <pod-name>

# Check Dapr dashboard (optional)
kubectl port-forward -n dapr-system svc/dapr-dashboard 8080:8080

# Access: http://localhost:8080
```

**Using kubectl-ai for debugging**:
```bash
kubectl-ai "check why backend pods are failing"
kubectl-ai "show me resource usage for todo namespace"
kubectl-ai "what's wrong with my ingress configuration"
```

---

## Common Issues and Solutions

### Issue 1: Pods stuck in `ImagePullBackOff`

**Cause**: Docker images not found in Minikube's registry

**Solution**:
```bash
# Ensure you built images with Minikube's Docker
eval $(minikube docker-env)
docker images | grep todo

# Rebuild if missing
docker build -t todo-frontend:1.0.0 ./phase-4/frontend
docker build -t todo-backend:1.0.0 ./phase-4/backend

# Check pod events
kubectl describe pod -n todo <pod-name> | grep -A 10 Events
```

### Issue 2: Ingress returns 503 Service Unavailable

**Cause**: Backend pods not ready or service endpoints missing

**Solution**:
```bash
# Check pod status
kubectl get pods -n todo

# Check service endpoints
kubectl get endpoints -n todo

# If no endpoints, check pod readiness probes
kubectl describe pod -n todo <backend-pod-name> | grep -A 5 Readiness
```

### Issue 3: Dapr sidecar fails to inject

**Cause**: Dapr not properly initialized or annotations missing

**Solution**:
```bash
# Verify Dapr is running
dapr status -k

# Check pod annotations
kubectl get pod -n todo <pod-name> -o yaml | grep -A 10 annotations

# Should see:
# dapr.io/enabled: "true"
# dapr.io/app-id: "todo-backend"

# Restart deployment if annotations missing
kubectl rollout restart deployment/backend -n todo
```

### Issue 4: Database connection failures

**Cause**: Incorrect connection string or firewall rules

**Solution**:
```bash
# Verify secret exists and has correct key
kubectl get secret todo-secrets -n todo -o yaml

# Decode and check connection string (locally only!)
kubectl get secret todo-secrets -n todo -o jsonpath='{.data.database-url}' | base64 -d

# Test connection from backend pod
kubectl exec -it -n todo <backend-pod-name> -c backend -- sh
# Inside pod:
# python -c "import psycopg2; psycopg2.connect('your-connection-string')"
```

---

## Upgrade and Rollback

### Upgrade Deployment

```bash
# Update values or image tags
# Edit values-dev.yaml

# Upgrade release
helm upgrade todo-app ./charts/todo-app \
  -f values-dev.yaml \
  -n todo \
  --wait \
  --timeout 5m \
  --atomic

# Check rollout status
kubectl rollout status deployment/backend -n todo
kubectl rollout status deployment/frontend -n todo
```

### Rollback on Failure

```bash
# View release history
helm history todo-app -n todo

# Expected output:
# REVISION  UPDATED                   STATUS      CHART          APP VERSION  DESCRIPTION
# 1         2025-12-31 00:00:00       deployed    todo-app-1.0.0 1.0.0        Install complete
# 2         2025-12-31 00:30:00       failed      todo-app-1.0.0 1.0.0        Upgrade failed

# Rollback to previous revision
helm rollback todo-app 1 -n todo

# Verify rollback success
kubectl get pods -n todo
```

---

## Cleanup

```bash
# Uninstall Helm release
helm uninstall todo-app -n todo

# Delete namespace (removes all resources)
kubectl delete namespace todo

# Stop Minikube (preserves cluster state)
minikube stop

# Delete Minikube cluster (complete cleanup)
minikube delete

# Remove from /etc/hosts (Mac/Linux)
sudo sed -i '' '/todo.local/d' /etc/hosts

# Windows: Manually remove line from C:\Windows\System32\drivers\etc\hosts
```

---

## Next Steps

1. **Production Deployment**: Adapt Helm charts for cloud Kubernetes (EKS, GKE, AKS)
2. **CI/CD Integration**: Automate build and deploy pipeline
3. **Monitoring**: Add Prometheus + Grafana for observability
4. **Scaling**: Test horizontal pod autoscaling (HPA)
5. **Security Hardening**: Add Pod Security Policies, OPA Gatekeeper

---

## Useful Commands Reference

```bash
# Cluster management
minikube status
minikube dashboard
kubectl cluster-info

# Resource inspection
kubectl get all -n todo
kubectl describe <resource> -n todo <name>
kubectl logs -n todo <pod-name> -c <container-name> -f

# Helm operations
helm list -n todo
helm status todo-app -n todo
helm get values todo-app -n todo

# Dapr operations
dapr status -k
dapr dashboard -k
dapr logs -k -a todo-backend -n todo

# Debugging
kubectl exec -it -n todo <pod-name> -- sh
kubectl port-forward -n todo svc/<service-name> <local-port>:<service-port>
kubectl top nodes
kubectl top pods -n todo

# AI-assisted
kubectl-ai "<your question>"
kagent "analyze cluster health"
docker ai "<docker optimization query>"
```

---

## Success Criteria Checklist

- [ ] Minikube cluster running with 4 CPUs, 8GB RAM
- [ ] Dapr installed and all system pods healthy
- [ ] NGINX Ingress Controller enabled
- [ ] `todo.local` resolves to Minikube IP
- [ ] Docker images built and available in Minikube
- [ ] Kubernetes namespace `todo` created
- [ ] Secrets created with database URL and API keys
- [ ] Helm chart deploys successfully (no errors)
- [ ] All pods in `Running` state (frontend 1/1, backend 2/2)
- [ ] Services have endpoints
- [ ] Ingress accessible at http://todo.local
- [ ] Frontend loads in browser
- [ ] Chat functionality works end-to-end
- [ ] Backend connects to Neon PostgreSQL
- [ ] Dapr sidecar injected and mTLS enabled

---

**Estimated Time**: 30-45 minutes for first-time setup  
**Difficulty**: Intermediate (basic Kubernetes knowledge required)

For issues or questions, refer to:
- Minikube docs: https://minikube.sigs.k8s.io/docs/
- Helm docs: https://helm.sh/docs/
- Dapr docs: https://docs.dapr.io/
- kubectl-ai: https://github.com/sozercan/kubectl-ai
