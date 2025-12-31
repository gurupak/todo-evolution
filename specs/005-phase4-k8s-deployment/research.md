# Phase 0: Research & Technology Decisions

**Feature**: Cloud-Native Kubernetes Deployment  
**Date**: 2025-12-31  
**Purpose**: Resolve all technical unknowns before implementation

---

## 1. Container Runtime & Orchestration

### Decision: Minikube + Docker Desktop

**Rationale**:
- **Minikube**: Industry-standard local Kubernetes environment, widely adopted for development/testing
- **Docker Desktop**: Provides stable container runtime with native integration on Windows/macOS
- **Compatibility**: Minikube runs seamlessly on Docker Desktop driver
- **Resource Requirements**: 4 CPUs, 8GB RAM suitable for local development without overwhelming developer machines

**Alternatives Considered**:
- **Kind (Kubernetes in Docker)**: More lightweight but less feature-rich for local development
- **K3s**: Production-focused, overkill for local testing
- **MicroK8s**: Ubuntu-centric, less cross-platform support

**Best Practices**:
- Use `eval $(minikube docker-env)` to build images directly in Minikube's Docker daemon (avoids registry push/pull)
- Enable required addons during initialization: `ingress`, `metrics-server`
- Pin Minikube version in documentation for reproducibility

---

## 2. Container Image Strategy

### Decision: Multi-Stage Docker Builds with Alpine/Slim Base Images

**Rationale**:
- **Security**: Minimal base images reduce attack surface
- **Size**: Alpine (5MB) and slim variants significantly smaller than full images
- **Performance**: Faster image pulls and pod startup times
- **Best Practice**: Industry standard for production containerization

**Image Specifications**:

| Component | Base (Build) | Base (Runtime) | Target Size | Strategy |
|-----------|--------------|----------------|-------------|----------|
| Frontend | node:20-alpine | node:20-alpine | < 200MB | Multi-stage: deps → build → runtime |
| Backend | python:3.13-slim | python:3.13-slim | < 300MB | Multi-stage: UV install → runtime |

**Alternatives Considered**:
- **Distroless images**: More secure but harder to debug (no shell)
- **Single-stage builds**: Simpler but include build tools in runtime (security risk, larger size)
- **Full Debian/Ubuntu bases**: Unnecessary bloat for containerized apps

**Best Practices**:
- Always run as non-root user (UID 1000)
- Use `.dockerignore` to exclude unnecessary files
- Pin exact versions in base images (e.g., `node:20.11.0-alpine` not `node:20-alpine`)
- Leverage Gordon (Docker AI) for optimization suggestions

---

## 3. Package Management: Helm

### Decision: Helm 3.x with Multi-Environment Values Files

**Rationale**:
- **De Facto Standard**: Most widely used Kubernetes package manager
- **Templating**: Powerful Go templating for manifest generation
- **Reusability**: Single chart supports dev/staging/prod via values files
- **Rollback Support**: Built-in release history and rollback capabilities

**Chart Structure**:
```
charts/todo-app/
├── Chart.yaml              # Chart metadata
├── values.yaml             # Production defaults
├── values-dev.yaml         # Minikube overrides
├── templates/
│   ├── frontend/           # Frontend K8s resources
│   ├── backend/            # Backend K8s resources
│   ├── security/           # RBAC, NetworkPolicies
│   └── dapr/               # Dapr components
```

**Alternatives Considered**:
- **Kustomize**: Less flexible templating, harder to manage complex variations
- **Raw manifests**: No parameterization, manual environment management
- **Operator pattern**: Overkill for stateless applications

**Best Practices**:
- Use `helm lint` and `helm template` before every install
- Implement automatic rollback via `--wait --timeout` flags
- Separate concerns: base chart + environment-specific values
- Version charts independently from application versions

---

## 4. Service Mesh: Dapr

### Decision: Dapr 1.12+ with mTLS and Scoped Components

**Rationale**:
- **Zero Code Changes**: Sidecar pattern requires no app modifications
- **Built-in mTLS**: Automatic service-to-service encryption
- **Abstraction**: Portable across cloud providers and local environments
- **State Management**: Unified API for PostgreSQL, Redis, etc.

**Components Selected**:

| Component | Type | Implementation | Purpose |
|-----------|------|----------------|---------|
| State Store | state.redis | Redis (local) | Session/cache state with persistence |
| Configuration | Dapr Config | mTLS enabled | Secure service mesh |

**Alternatives Considered**:
- **Istio**: Too complex for local development, resource-intensive
- **Linkerd**: Lighter than Istio but still heavier than Dapr for our use case
- **No service mesh**: Miss out on mTLS, observability, state abstraction

**Best Practices**:
- Always define component scopes to limit access
- Use `secretKeyRef` for all sensitive values (never plain text)
- Set sidecar resource limits to prevent resource starvation
- Enable mTLS with reasonable certificate TTL (24h for local)

---

## 5. Ingress Controller

### Decision: NGINX Ingress Controller

**Rationale**:
- **Default Minikube Addon**: One command to enable (`minikube addons enable ingress`)
- **Widely Adopted**: Most documented and supported ingress controller
- **Production Parity**: Same controller used in many cloud environments
- **Simplicity**: Straightforward configuration for basic HTTP routing

**Alternatives Considered**:
- **Traefik**: More features (auto-HTTPS) but added complexity for local dev
- **Kong**: API gateway features unnecessary for this phase
- **HAProxy Ingress**: Less community support and documentation

**Best Practices**:
- Use host-based routing (`todo.local`) for clean URL structure
- Configure `/etc/hosts` to point domain to Minikube IP
- Set appropriate timeout values for long-running API calls
- Enable CORS headers at ingress level if needed

---

## 6. Secrets Management

### Decision: Kubernetes Native Secrets with Base64 Encoding

**Rationale**:
- **Built-in**: No additional tools required for local development
- **Integration**: Native kubectl and Helm support
- **Sufficient for Local**: External secret managers (Vault, AWS Secrets Manager) overkill for Minikube

**Secrets Required**:
```
todo-secrets:
  - database-url (Neon PostgreSQL connection string)
  - openai-api-key (AI model access)
  - better-auth-secret (session encryption)
```

**Alternatives Considered**:
- **External Secrets Operator**: Adds complexity, meant for prod environments
- **HashiCorp Vault**: Over-engineered for local development
- **Sealed Secrets**: Useful for GitOps but unnecessary here

**Best Practices**:
- Never commit secrets to Git
- Use `kubectl create secret` from environment variables or files
- Reference secrets via `secretKeyRef` in pod specs
- Rotate secrets regularly even in development

---

## 7. Namespace Strategy

### Decision: Single Dedicated Namespace (`todo`)

**Rationale**:
- **Simpler Service Discovery**: Services can reference each other by name
- **Easier RBAC Management**: Single namespace for all RBAC rules
- **Development Focus**: Multi-namespace adds complexity without local dev benefits
- **Resource Quotas**: Still possible within single namespace

**Alternatives Considered**:
- **Multiple Namespaces** (frontend, backend, infra): Over-isolation for local testing
- **Default Namespace**: Not production-like, poor practice

**Best Practices**:
- Create namespace explicitly: `kubectl create namespace todo`
- All Helm resources scoped to this namespace
- Use ResourceQuotas to simulate production limits
- NetworkPolicies still enforce isolation within namespace

---

## 8. Observability & Logging

### Decision: Kubernetes Native Logs with 2-Day Retention

**Rationale**:
- **kubectl logs**: Built-in, no additional tools needed
- **2-Day Retention**: Balances debugging needs with disk space on local machine
- **Structured Logging**: JSON logs from FastAPI/Next.js for easier parsing
- **Lightweight**: Avoid Prometheus/Grafana/ELK overhead in local environment

**Alternatives Considered**:
- **Loki + Grafana**: Full observability stack too heavy for Minikube
- **Fluentd + Elasticsearch**: Resource-intensive, production-focused
- **No retention management**: Risk filling disk on long-running local clusters

**Best Practices**:
- Use `kubectl logs -f` for real-time monitoring
- Implement structured JSON logging in applications
- Configure log rotation at container runtime level
- Export critical logs before cluster teardown

---

## 9. Resource Allocation

### Decision: Conservative Limits for Local Development

**Resource Specifications**:

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Frontend | 100m | 500m | 128Mi | 256Mi |
| Backend | 200m | 1000m | 256Mi | 512Mi |
| Dapr Sidecar | 100m | 300m | 128Mi | 256Mi |
| Redis (State) | 100m | 500m | 128Mi | 256Mi |

**Rationale**:
- **Fits Minikube**: Total ~1.5 CPU / 2GB RAM leaves headroom for system pods
- **Prevents Starvation**: Requests guarantee minimum resources
- **Safety Limits**: Prevents runaway processes from crashing cluster
- **Realistic**: Mirrors production patterns of setting limits

**Alternatives Considered**:
- **No Limits**: Risky, pods can consume all cluster resources
- **Higher Limits**: Exceeds typical Minikube capacity
- **BestEffort QoS**: No guarantees, pods evicted under pressure

**Best Practices**:
- Start conservative, increase based on observed usage
- Use `kubectl top pods` to monitor actual consumption
- Set requests = limits for guaranteed QoS (critical pods only)
- Test OOMKilled scenarios to validate recovery

---

## 10. Deployment Automation

### Decision: Helm Install with Automatic Rollback

**Rationale**:
- **Helm Hooks**: `--wait` flag ensures pods ready before marking success
- **Automatic Rollback**: `--atomic` flag rolls back on failure
- **Idempotent**: `helm upgrade --install` handles both install and update
- **Simple for Local**: More complex tools (Flux, ArgoCD) unnecessary

**Deployment Command**:
```bash
helm upgrade --install todo-app ./charts/todo-app \
  -f ./charts/todo-app/values-dev.yaml \
  -n todo \
  --wait \
  --timeout 5m \
  --atomic
```

**Alternatives Considered**:
- **kubectl apply**: Manual, no rollback, harder to manage
- **Skaffold**: Great for dev workflow but adds learning curve
- **ArgoCD**: GitOps tool, overkill for local deployment

**Best Practices**:
- Always use `--dry-run --debug` before actual deployment
- Set reasonable timeout (5m for all pods to be ready)
- Use `helm history` to track releases
- Test rollback scenarios deliberately

---

## 11. AI-Assisted DevOps Tools

### Decision: Gordon (Docker), kubectl-ai, kagent

**Rationale**:
- **Gordon**: Optimizes Dockerfiles, scans for vulnerabilities, suggests improvements
- **kubectl-ai**: Natural language K8s operations (debugging, scaling, troubleshooting)
- **kagent**: Cluster-level analysis and optimization recommendations
- **Productivity**: Reduces time spent on repetitive tasks and debugging

**Use Cases**:
```bash
# Gordon examples
docker ai "create optimized Dockerfile for FastAPI with UV"
docker ai "analyze image size for todo-backend"

# kubectl-ai examples
kubectl-ai "check why backend pods are failing"
kubectl-ai "scale frontend to 2 replicas"

# kagent examples
kagent "analyze cluster health"
kagent "optimize resource allocation for todo namespace"
```

**Alternatives Considered**:
- **Manual Only**: Slower, more error-prone, misses optimization opportunities
- **Copilot/ChatGPT**: Generic, not Kubernetes/Docker-specific

**Best Practices**:
- Use AI tools for exploration and suggestions, verify before applying
- Combine AI suggestions with manual review
- Document AI-generated configurations for reproducibility
- Update tools regularly for latest best practices

---

## 12. Network Policies

### Decision: Default Deny with Explicit Allow Rules

**Rationale**:
- **Zero Trust**: Deny all traffic by default, explicitly allow only required paths
- **Security Best Practice**: Prevents lateral movement in case of compromise
- **Production Parity**: Mirrors production network security posture

**Required Rules**:
```
frontend → backend:8000 (HTTP)
backend → redis:6379 (Dapr state)
backend → neon-postgresql:5432 (External, allow egress)
dapr-sidecar ↔ dapr-sidecar (mTLS, port 50001)
```

**Alternatives Considered**:
- **No NetworkPolicies**: Simpler but insecure, not production-like
- **Allow All**: Defeats the purpose of network segmentation

**Best Practices**:
- Start with deny-all, add rules incrementally
- Test each policy to ensure required traffic flows
- Document rationale for each allow rule
- Use pod selectors and namespace selectors for precision

---

## Summary of Technical Decisions

| Category | Decision | Key Rationale |
|----------|----------|---------------|
| **Orchestration** | Minikube + Docker Desktop | Industry standard, cross-platform |
| **Containerization** | Multi-stage Alpine/Slim | Security, size optimization |
| **Package Manager** | Helm 3.x | De facto standard, powerful templating |
| **Service Mesh** | Dapr 1.12+ with mTLS | Zero-code sidecar, portable |
| **State Store** | Redis (Dapr component) | Production-like, persistent |
| **Ingress** | NGINX Ingress Controller | Default Minikube addon, simple |
| **Secrets** | Kubernetes Secrets | Native, sufficient for local |
| **Namespace** | Single (`todo`) | Simpler discovery, easier RBAC |
| **Observability** | kubectl logs + 2-day retention | Lightweight, built-in |
| **Resources** | Conservative limits | Fits Minikube, prevents starvation |
| **Deployment** | Helm with auto-rollback | Atomic, idempotent, safe |
| **AI Tools** | Gordon, kubectl-ai, kagent | Productivity, optimization |
| **Network** | Default deny NetworkPolicies | Zero trust, production parity |

---

## Next Steps

All NEEDS CLARIFICATION items resolved. Proceed to:
- **Phase 1**: Data model, API contracts, quickstart guide
- **Implementation**: Follow file generation order in main plan
