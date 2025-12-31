# Implementation Plan: Cloud-Native Kubernetes Deployment

**Branch**: `005-phase4-k8s-deployment` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/005-phase4-k8s-deployment/spec.md`

## Summary

Deploy the Todo AI Chatbot application (Phase 3 output) to a local Kubernetes cluster using Minikube with production-grade patterns: multi-stage Docker containers, Helm charts for package management, Dapr service mesh for mTLS and state management, NGINX ingress for HTTP routing, and comprehensive security controls (RBAC, Network Policies, non-root containers, resource limits). All infrastructure code generated via AI-assisted DevOps tools (Gordon, kubectl-ai, kagent) and validated against security standards before deployment.

## Technical Context

**Language/Version**: Python 3.13 (backend), Node.js 20 (frontend), Bash (scripts)  
**Primary Dependencies**: Docker Desktop 4.53+, Minikube, Helm 3.x, kubectl, Dapr CLI 1.12+, Gordon (Docker AI), kubectl-ai, kagent  
**Storage**: Neon PostgreSQL (existing from Phase 2/3), Redis (Dapr state store for local), Kubernetes etcd (cluster state)  
**Testing**: Helm lint, helm template validation, kubectl dry-run, security validation (@constitution-enforcer), Dapr validation (@dapr-validator)  
**Target Platform**: Minikube (local Kubernetes), Docker containers (Linux amd64/arm64)  
**Project Type**: Multi-component cloud-native application (frontend + backend + infrastructure)  
**Performance Goals**: All pods Running/Ready within 5 minutes, Frontend page load < 3 seconds, End-to-end chat < 10 seconds  
**Constraints**: Container images < target sizes (frontend 200MB, backend 300MB), Resource limits enforced (CPU/memory), mTLS mandatory, Zero critical security violations  
**Scale/Scope**: 3 application components (frontend, backend, MCP server), 42 Kubernetes resources, Single namespace deployment, Development environment (1 replica per component)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Status**: Template constitution file found (not project-specific)

**Key Requirements from Specification**:
1. ✅ **Security by Default**: Non-root containers, resource limits, RBAC, network policies, secrets management
2. ✅ **No Manual Infrastructure Code**: All YAML generated via Helm/@helm-chart-generator, Dockerfiles via Gordon
3. ✅ **Environment Parity**: Local Minikube mirrors production Kubernetes patterns
4. ✅ **Stateless & Scalable**: Applications horizontally scalable, state in external stores (PostgreSQL, Redis)
5. ✅ **Quality Gates**: Lint → Security scan → Validation → Dry-run → Deploy → Verify

**Validation Approach**:
- All Helm charts validated with `@constitution-enforcer` skill
- All Dapr components validated with `@dapr-validator` skill  
- Security violations BLOCK deployment until resolved

## Project Structure

### Documentation (this feature)

```
specs/005-phase4-k8s-deployment/
├── plan.md                 # This file (/sp.plan command output)
├── research.md             # Phase 0 output - Technology decisions
├── data-model.md           # Phase 1 output - Infrastructure entities
├── quickstart.md           # Phase 1 output - Deployment guide
├── contracts/
│   └── helm-values-schema.yaml  # Phase 1 output - Helm values contract
├── checklists/
│   └── requirements.md     # Spec validation checklist
└── tasks.md                # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```
hackathon-todo/
├── phase-3/                    # Existing application code
│   ├── backend/                # FastAPI application
│   └── frontend/               # Next.js application
│
├── phase-4/                    # NEW - Kubernetes deployment (this phase)
│   ├── backend/                # Copied from phase-3, with additions
│   │   ├── src/todo_api/       # Existing application code
│   │   ├── pyproject.toml      # Existing dependencies
│   │   ├── Dockerfile          # NEW - Multi-stage container build
│   │   └── .dockerignore       # NEW - Build optimization
│   │
│   ├── frontend/               # Copied from phase-3, with additions
│   │   ├── src/                # Existing Next.js application
│   │   ├── package.json        # Existing dependencies
│   │   ├── Dockerfile          # NEW - Multi-stage container build
│   │   └── .dockerignore       # NEW - Build optimization
│   │
│   ├── charts/                 # NEW - Helm package definitions
│   │   └── todo-app/
│   │       ├── Chart.yaml      # Chart metadata
│   │       ├── values.yaml     # Production defaults
│   │       ├── values-dev.yaml # Minikube overrides
│   │       └── templates/
│   │           ├── _helpers.tpl        # Template helpers
│   │           ├── namespace.yaml      # Namespace definition
│   │           ├── frontend/
│   │           │   ├── deployment.yaml
│   │           │   ├── service.yaml
│   │           │   ├── ingress.yaml
│   │           │   ├── serviceaccount.yaml
│   │           │   ├── role.yaml
│   │           │   └── rolebinding.yaml
│   │           ├── backend/
│   │           │   ├── deployment.yaml
│   │           │   ├── service.yaml
│   │           │   ├── serviceaccount.yaml
│   │           │   ├── role.yaml
│   │           │   └── rolebinding.yaml
│   │           ├── security/
│   │           │   └── networkpolicy.yaml
│   │           └── dapr/
│   │               ├── config.yaml      # mTLS configuration
│   │               └── statestore.yaml  # Redis state component
│   │
│   ├── k8s/                    # NEW - Base Kubernetes resources
│   │   ├── namespace.yaml      # Todo namespace definition
│   │   └── secrets-template.yaml  # Secret structure (NOT actual secrets)
│   │
│   ├── scripts/                # NEW - Automation scripts
│   │   ├── setup-minikube.sh   # Cluster initialization
│   │   ├── build-images.sh     # Docker build automation
│   │   ├── deploy.sh           # Helm install/upgrade
│   │   └── cleanup.sh          # Resource cleanup
│   │
│   └── README.md               # NEW - Phase 4 documentation
```

**Structure Decision**: Multi-component cloud-native structure selected because this is a Kubernetes deployment feature. The phase-4/ directory contains application code (copied from phase-3) plus all infrastructure-as-code (Dockerfiles, Helm charts, K8s manifests, scripts). This separates deployment concerns from application logic while maintaining phase lineage.

## Complexity Tracking

**No violations** - All patterns align with cloud-native best practices:
- Helm charts are industry standard for Kubernetes package management
- Dapr sidecar pattern requires no application code changes (zero complexity add)
- Multi-stage Docker builds reduce image size and attack surface
- RBAC and NetworkPolicies are security requirements, not complexity
- Single namespace deployment chosen specifically to reduce complexity

## Phase 0: Research & Technology Decisions

**Status**: ✅ Complete - See [research.md](./research.md)

**Key Decisions Made**:
1. **Orchestration**: Minikube + Docker Desktop (industry standard, cross-platform)
2. **Containerization**: Multi-stage builds with Alpine/Slim bases (security, size optimization)
3. **Package Manager**: Helm 3.x (de facto standard, powerful templating)
4. **Service Mesh**: Dapr 1.12+ with mTLS (zero-code sidecar, portable)
5. **State Store**: Redis via Dapr component (production-like, persistent)
6. **Ingress**: NGINX Ingress Controller (default Minikube addon, simple)
7. **Secrets**: Kubernetes native Secrets (sufficient for local dev)
8. **Namespace**: Single dedicated namespace (`todo`) (simpler discovery, easier RBAC)
9. **Observability**: kubectl logs + 2-day retention (lightweight, built-in)
10. **Resources**: Conservative limits (fits Minikube 4CPU/8GB)
11. **Deployment**: Helm with automatic rollback (atomic, idempotent, safe)
12. **AI Tools**: Gordon, kubectl-ai, kagent (productivity, optimization)
13. **Network**: Default deny NetworkPolicies (zero trust, production parity)

**All NEEDS CLARIFICATION items resolved** - Proceed to Phase 1

## Phase 1: Design & Contracts

**Status**: ✅ Complete

### Data Model

**File**: [data-model.md](./data-model.md)

**Infrastructure Entities Defined**:
1. Deployment Configuration (environment settings)
2. Application Component (frontend, backend, MCP server)
3. Kubernetes Pod (runtime instances)
4. Service (network endpoints)
5. Ingress Route (external HTTP access)
6. Service Account (pod identities)
7. Role & RoleBinding (RBAC permissions)
8. Network Policy (traffic control)
9. Kubernetes Secret (sensitive data)
10. Dapr Component (state store, pub/sub)
11. Dapr Configuration (mTLS settings)
12. Helm Release (application package)

**Entity Relationships**: Documented with lifecycle, validation rules, state transitions

### API Contracts

**File**: [contracts/helm-values-schema.yaml](./contracts/helm-values-schema.yaml)

**Contract Type**: JSON Schema for Helm values.yaml  
**Purpose**: Define expected structure and validation rules for deployment configuration

**Key Sections**:
- `global`: Namespace configuration
- `frontend`: Image, service, ingress, resources, security context
- `backend`: Image, service, Dapr, resources, environment variables, security context
- `dapr`: mTLS, state store, sidecar resources
- `secrets`: Required secret values (database URL, API keys)

**Validation Rules**:
- Image tags cannot be "latest"
- Security contexts enforce non-root (UID 1000)
- Resource requests <= limits
- All secrets reference via secretKeyRef
- Namespace must be DNS-compatible

### Quickstart Guide

**File**: [quickstart.md](./quickstart.md)

**Purpose**: Step-by-step deployment instructions for developers

**Sections**:
1. Prerequisites (tool installation)
2. Start Minikube (cluster initialization)
3. Enable Addons (ingress, metrics-server)
4. Install Dapr (service mesh)
5. Configure Local DNS (todo.local)
6. Build Docker Images (with Gordon optimization tips)
7. Create Namespace
8. Create Secrets
9. Deploy with Helm
10. Verify Deployment
11. Access Application
12. Monitor and Debug (kubectl-ai examples)
13. Common Issues and Solutions
14. Upgrade and Rollback
15. Cleanup
16. Useful Commands Reference

**Estimated Time**: 30-45 minutes for first deployment  
**Success Criteria Checklist**: 20 verification points

## File Generation Order

Following spec-driven development principles:

### Phase 0: Infrastructure Setup (Manual)
1. Install prerequisites (Docker Desktop, Minikube, Helm, kubectl, Dapr CLI)
2. Install AI DevOps tools (Gordon, kubectl-ai, kagent)
3. Verify toolchain: `./scripts/verify-prerequisites.sh`

### Phase 1: Directory Structure
```bash
# Create phase-4 directory structure
mkdir -p phase-4/{backend,frontend,charts/todo-app/templates/{frontend,backend,security,dapr},k8s,scripts}
mkdir -p phase-4/charts/todo-app/charts
```

### Phase 2: Application Code
```bash
# Copy application from phase-3
cp -r phase-3/backend phase-4/backend
cp -r phase-3/frontend phase-4/frontend
```

### Phase 3: Docker Configuration
1. Generate `phase-4/backend/.dockerignore` (Gordon AI)
2. Generate `phase-4/backend/Dockerfile` (Gordon AI: "create optimized multi-stage Dockerfile for FastAPI with UV")
3. Generate `phase-4/frontend/.dockerignore` (Gordon AI)
4. Generate `phase-4/frontend/Dockerfile` (Gordon AI: "create production Dockerfile for Next.js 15 App Router")
5. Validate Dockerfiles (Gordon: "analyze and suggest optimizations")

### Phase 4: Helm Chart Foundation
1. Generate `charts/todo-app/Chart.yaml` (@helm-chart-generator or manual template)
2. Generate `charts/todo-app/values.yaml` (production defaults)
3. Generate `charts/todo-app/values-dev.yaml` (Minikube overrides)
4. Generate `charts/todo-app/templates/_helpers.tpl` (template functions)

### Phase 5: Kubernetes Resources (Frontend)
1. Generate `templates/frontend/deployment.yaml` (@helm-chart-generator)
   - Security context (non-root, read-only FS)
   - Resource limits (100m/500m CPU, 128Mi/256Mi memory)
   - Health checks (liveness, readiness probes)
2. Generate `templates/frontend/service.yaml`
   - Type: ClusterIP, Port: 3000
3. Generate `templates/frontend/ingress.yaml`
   - Host: todo.local, Backend: frontend-svc:3000
   - IngressClass: nginx
4. Generate `templates/frontend/serviceaccount.yaml`
5. Generate `templates/frontend/role.yaml` (minimal RBAC)
6. Generate `templates/frontend/rolebinding.yaml`

### Phase 6: Kubernetes Resources (Backend)
1. Generate `templates/backend/deployment.yaml` (@helm-chart-generator)
   - Security context (non-root, read-only FS)
   - Resource limits (200m/1000m CPU, 256Mi/512Mi memory)
   - Dapr annotations (enabled, app-id, app-port, sidecar limits)
   - Environment variables from secrets
   - Health checks
2. Generate `templates/backend/service.yaml`
   - Type: ClusterIP, Port: 8000
3. Generate `templates/backend/serviceaccount.yaml`
4. Generate `templates/backend/role.yaml` (minimal RBAC)
5. Generate `templates/backend/rolebinding.yaml`

### Phase 7: Security Resources
1. Generate `templates/security/networkpolicy.yaml`
   - Default deny all
   - Allow frontend → backend:8000
   - Allow backend → redis:6379
   - Allow backend → external PostgreSQL
   - Allow Dapr sidecar ↔ sidecar (mTLS port 50001)

### Phase 8: Dapr Components
1. Generate `templates/dapr/config.yaml` (@dapr-validator)
   - mTLS enabled: true
   - Certificate TTL: 24h
   - Clock skew: 15m
2. Generate `templates/dapr/statestore.yaml` (@dapr-validator)
   - Type: state.redis
   - Connection string via secretKeyRef
   - Scopes: [todo-backend]

### Phase 9: Base Kubernetes Resources
1. Generate `k8s/namespace.yaml`
   - Name: todo
   - Labels: env=development
2. Generate `k8s/secrets-template.yaml` (structure only, NOT actual secrets)
   - Keys: database-url, openai-api-key, better-auth-secret

### Phase 10: Automation Scripts
1. Generate `scripts/setup-minikube.sh`
   ```bash
   - minikube start --cpus=4 --memory=8192
   - minikube addons enable ingress
   - minikube addons enable metrics-server
   - dapr init -k --wait
   - echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts
   ```
2. Generate `scripts/build-images.sh`
   ```bash
   - eval $(minikube docker-env)
   - docker build -t todo-frontend:1.0.0 ./frontend
   - docker build -t todo-backend:1.0.0 ./backend
   - docker images | grep todo
   ```
3. Generate `scripts/deploy.sh`
   ```bash
   - kubectl create namespace todo
   - kubectl create secret generic todo-secrets --from-env-file=.env -n todo
   - helm lint ./charts/todo-app
   - helm install todo-app ./charts/todo-app -f values-dev.yaml -n todo --wait --timeout 5m --atomic
   - kubectl get pods -n todo
   - dapr status -k
   - echo "Access: http://todo.local"
   ```
4. Generate `scripts/cleanup.sh`
   ```bash
   - helm uninstall todo-app -n todo
   - kubectl delete namespace todo
   - sudo sed -i '' '/todo.local/d' /etc/hosts
   - minikube stop
   ```

### Phase 11: Documentation
1. Generate `phase-4/README.md`
   - Overview of Phase IV
   - Prerequisites
   - Quick start (link to quickstart.md)
   - Architecture diagram
   - Troubleshooting
   - Next steps

## Validation Gates

### Pre-Implementation Gates
- ✅ Specification complete and validated
- ✅ All clarifications resolved (5 questions answered)
- ✅ Research complete (13 technology decisions documented)
- ✅ Data model defined (12 infrastructure entities)
- ✅ Contracts defined (Helm values schema)

### Pre-Deployment Gates
```bash
# Helm validation
helm lint ./charts/todo-app
# Expected: No errors or warnings

helm template todo-app ./charts/todo-app -f values-dev.yaml
# Expected: Valid YAML output

helm install todo-app ./charts/todo-app --dry-run --debug -n todo
# Expected: Successful simulation

# Security validation (manual or via @constitution-enforcer)
# Check:
- All containers non-root (UID 1000)
- Resource limits defined for all containers
- Secrets referenced via secretKeyRef (no plain text)
- Network policies in place (default deny)
- RBAC roles namespace-scoped (no ClusterRole)
- Image tags not "latest"

# Dapr validation (manual or via @dapr-validator)
# Check:
- mTLS enabled in configuration
- Scopes defined on all components (not empty)
- Connection strings via secretKeyRef
- Sidecar resource limits set
```

### Deployment Gates
```bash
# Image build
docker build -t todo-frontend:1.0.0 ./frontend
# Expected: Exit code 0, image size < 200MB

docker build -t todo-backend:1.0.0 ./backend
# Expected: Exit code 0, image size < 300MB

# Kubernetes validation
kubectl apply -f k8s/namespace.yaml --dry-run=client
# Expected: namespace/todo created (dry run)

# Helm install
helm install todo-app ./charts/todo-app -f values-dev.yaml -n todo --wait --timeout 5m --atomic
# Expected: STATUS: deployed, REVISION: 1
```

### Post-Deployment Gates
```bash
# Pod status
kubectl get pods -n todo
# Expected: All pods Running, frontend 1/1, backend 2/2 (app + Dapr sidecar)

# Service endpoints
kubectl get endpoints -n todo
# Expected: All services have at least one endpoint IP

# Ingress accessibility
curl -I http://todo.local
# Expected: HTTP/1.1 200 OK

# Dapr health
dapr status -k
# Expected: All Dapr system pods healthy

# Health checks
curl http://todo.local/api/health
# Expected: {"status": "healthy"}
```

### Success Criteria Verification

From specification (12 success criteria):

1. ✅ **SC-001**: All pods Running/Ready within 5 minutes  
   `kubectl get pods -n todo --watch` (monitor until all Running)

2. ✅ **SC-002**: Frontend page load < 3 seconds  
   `curl -w "@curl-format.txt" -o /dev/null -s http://todo.local` (time_total < 3.0)

3. ✅ **SC-003**: End-to-end chat < 10 seconds  
   Manual test: Send chat message, measure response time

4. ✅ **SC-004**: Health checks return 200  
   `curl -I http://todo.local/api/health` (HTTP 200)

5. ✅ **SC-005**: Zero critical security violations  
   Run @constitution-enforcer validation

6. ✅ **SC-006**: Dapr mTLS 100% established  
   `dapr status -k` (all healthy), `kubectl logs -n todo <backend-pod> -c daprd | grep mTLS`

7. ✅ **SC-007**: Helm install succeeds (dev + prod values)  
   `helm install --dry-run` with both values files

8. ✅ **SC-008**: Data persists across pod restarts  
   Create task → Delete pod → Verify task still exists

9. ✅ **SC-009**: Database connections use SSL  
   Check connection string has `sslmode=require`

10. ✅ **SC-010**: 80% first-attempt deployment success  
    Follow quickstart.md, track success rate

11. ✅ **SC-011**: Images meet size targets  
    `docker images | grep todo` (frontend < 200MB, backend < 300MB)

12. ✅ **SC-012**: Automatic recovery from failures  
    Kill pod: `kubectl delete pod -n todo <pod-name>`, verify automatic restart

## Deployment Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Minikube Cluster                   │
│                   (todo namespace)                   │
│                                                      │
│  ┌───────────────────────────────────────────────┐  │
│  │          NGINX Ingress Controller             │  │
│  │          (minikube addon)                     │  │
│  └────────────────┬──────────────────────────────┘  │
│                   │ http://todo.local                │
│                   ▼                                  │
│  ┌───────────────────────────────────────────────┐  │
│  │  Frontend Service (ClusterIP)                 │  │
│  │  Port: 3000                                   │  │
│  └────────────────┬──────────────────────────────┘  │
│                   │                                  │
│                   ▼                                  │
│  ┌───────────────────────────────────────────────┐  │
│  │  Frontend Pod                                 │  │
│  │  ┌─────────────────────────────────────────┐ │  │
│  │  │ Next.js Container                       │ │  │
│  │  │ - Port 3000                             │ │  │
│  │  │ - Non-root (UID 1000)                   │ │  │
│  │  │ - CPU: 100m/500m, Mem: 128Mi/256Mi      │ │  │
│  │  └─────────────────────────────────────────┘ │  │
│  └────────────────┬──────────────────────────────┘  │
│                   │ Network Policy: Allow egress     │
│                   │ to backend:8000                  │
│                   ▼                                  │
│  ┌───────────────────────────────────────────────┐  │
│  │  Backend Service (ClusterIP)                  │  │
│  │  Port: 8000                                   │  │
│  └────────────────┬──────────────────────────────┘  │
│                   │                                  │
│                   ▼                                  │
│  ┌───────────────────────────────────────────────┐  │
│  │  Backend Pod                                  │  │
│  │  ┌──────────────────┐  ┌──────────────────┐  │  │
│  │  │ FastAPI Container│  │ Dapr Sidecar     │  │  │
│  │  │ - Port 8000      │  │ - Port 3500      │  │  │
│  │  │ - Non-root       │  │ - mTLS enabled   │  │  │
│  │  │ - CPU: 200m/1000m│  │ - CPU: 100m/300m │  │  │
│  │  │ - Mem: 256Mi/512Mi│ │ - Mem: 128Mi/256Mi│ │  │
│  │  └──────────────────┘  └──────────────────┘  │  │
│  └────────────────┬──────────────┬───────────────┘  │
│                   │              │                   │
│                   │              └─► Dapr Components │
│                   │                  - statestore    │
│                   │                  - config (mTLS) │
│                   │                                  │
│                   ▼ Network Policy: Allow egress    │
│  ┌───────────────────────────────────────────────┐  │
│  │  Kubernetes Secrets (todo-secrets)            │  │
│  │  - database-url                               │  │
│  │  - openai-api-key                             │  │
│  │  - better-auth-secret                         │  │
│  └────────────────┬──────────────────────────────┘  │
└───────────────────┼───────────────────────────────┬─┘
                    │                               │
                    ▼                               ▼
      ┌─────────────────────────┐     ┌──────────────────────┐
      │  External PostgreSQL    │     │  Redis (Dapr State)  │
      │  (Neon Database)        │     │  (Local in Minikube) │
      │  - SSL required         │     │  - Persistent volume │
      └─────────────────────────┘     └──────────────────────┘
```

## Resource Allocation

| Component | Replicas | CPU Request | CPU Limit | Memory Request | Memory Limit | Total CPU | Total Memory |
|-----------|----------|-------------|-----------|----------------|--------------|-----------|--------------|
| Frontend | 1 | 100m | 500m | 128Mi | 256Mi | 100m | 128Mi |
| Backend | 1 | 200m | 1000m | 256Mi | 512Mi | 200m | 256Mi |
| Dapr Sidecar (backend) | 1 | 100m | 300m | 128Mi | 256Mi | 100m | 128Mi |
| **Application Total** | **3 containers** | **400m** | **1800m** | **512Mi** | **1024Mi** | **400m** | **512Mi** |
| Dapr System Pods | ~5 | ~200m | ~1000m | ~256Mi | ~512Mi | 200m | 256Mi |
| NGINX Ingress | 1 | ~100m | ~200m | ~90Mi | ~180Mi | 100m | 90Mi |
| **Cluster Total** | **~9 pods** | **~700m** | **~3000m** | **~858Mi** | **~1716Mi** | **700m** | **858Mi** |

**Minikube Capacity**: 4000m CPU / 8192Mi Memory  
**Headroom**: 3300m CPU (82%) / 7334Mi Memory (89%)  
**Safety Margin**: Adequate for local development with occasional spikes

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Image too large** | Slow startup, disk space issues | Use multi-stage builds, Alpine/Slim bases, .dockerignore, Gordon optimization |
| **Minikube resource exhaustion** | Cluster instability, pod evictions | Conservative resource limits, monitoring with `kubectl top`, guidance to stop other apps |
| **Network policy misconfiguration** | Services can't communicate | Default deny + explicit allow, test each policy incrementally, document in data-model.md |
| **Secret leakage** | Credentials exposed | Never commit secrets to Git, use kubectl create from env, .gitignore .env files |
| **Dapr sidecar fails to inject** | Backend loses service mesh capabilities | Validate annotations, check Dapr status, provide troubleshooting in quickstart.md |
| **Ingress not accessible** | Application unreachable from browser | Verify /etc/hosts, check ingress controller status, provide fallback kubectl port-forward |
| **Database connection failure** | Backend can't persist data | SSL required, connection string in secret, test from pod with psql, firewall allowlist Minikube IP |
| **Helm deployment fails** | Manual rollback required | Use --atomic flag for auto-rollback, test with --dry-run first, keep history for manual rollback |

## Next Steps

1. **Phase 2**: Run `/sp.tasks` to generate tasks.md with implementation tasks
2. **Implementation**: Execute file generation order (Phases 1-11 above)
3. **Validation**: Run all quality gates (lint, security, dry-run)
4. **Deployment**: Follow quickstart.md for first deployment
5. **Verification**: Validate all 12 success criteria
6. **Documentation**: Update agent context with new technologies learned

## Appendix: AI Tool Integration

### Gordon (Docker AI) Usage

```bash
# Generate optimized Dockerfiles
docker ai "create optimized multi-stage Dockerfile for FastAPI app with UV package manager and Python 3.13"

# Analyze image size
docker ai "analyze todo-backend:1.0.0 image and suggest size optimizations"

# Security scanning
docker ai "scan todo-frontend:1.0.0 for vulnerabilities"

# Generate .dockerignore
docker ai "create .dockerignore for Next.js project to minimize build context"
```

### kubectl-ai Usage

```bash
# Deployment operations
kubectl-ai "deploy todo frontend with 2 replicas"
kubectl-ai "scale backend deployment to 3 replicas"

# Debugging
kubectl-ai "check why backend pods are failing"
kubectl-ai "show me logs for all pods in todo namespace"
kubectl-ai "why is my ingress returning 503"

# Resource management
kubectl-ai "show resource usage for todo namespace"
kubectl-ai "create network policy allowing frontend to backend on port 8000"
```

### kagent Usage

```bash
# Cluster health
kagent "analyze cluster health and resource utilization"

# Optimization
kagent "optimize resource allocation for todo namespace"

# Troubleshooting
kagent "troubleshoot backend service connection issues"
kagent "why are pods being evicted in todo namespace"
```

## Appendix: Helm Commands Reference

```bash
# Linting and validation
helm lint ./charts/todo-app
helm template todo-app ./charts/todo-app -f values-dev.yaml

# Installation
helm install todo-app ./charts/todo-app -f values-dev.yaml -n todo --wait --timeout 5m --atomic

# Upgrade
helm upgrade todo-app ./charts/todo-app -f values-dev.yaml -n todo --wait --timeout 5m --atomic

# Rollback
helm history todo-app -n todo
helm rollback todo-app 1 -n todo

# Status and debugging
helm status todo-app -n todo
helm get values todo-app -n todo
helm get manifest todo-app -n todo

# Cleanup
helm uninstall todo-app -n todo
```

---

**Plan Complete** - Ready for `/sp.tasks` to generate actionable implementation tasks
