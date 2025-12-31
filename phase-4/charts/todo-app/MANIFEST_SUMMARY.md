# Kubernetes Manifest Summary - Phase IV

## Overview
All production-ready Kubernetes manifest files for Todo AI Chatbot deployment have been created.

## Created Files (10 total)

### Backend RBAC (2 files)
1. **backend/role.yaml** (13 lines)
   - RBAC Role with configmaps/secrets read permissions
   - Namespaced to `todo` namespace
   - Uses `todo-app.backend.labels` helper

2. **backend/rolebinding.yaml** (17 lines)
   - Binds backend role to backend service account
   - Scoped to `todo` namespace

### MCP Server (5 files)
3. **mcp-server/deployment.yaml** (51 lines)
   - 2 replicas (from values.yaml)
   - Image: todo-mcp-server:1.0.0
   - Port 8080 (no Dapr annotations)
   - Security context: runAsNonRoot, drop ALL capabilities, read-only filesystem
   - Health probes: /health endpoint
   - Resources: 100m/128Mi (requests), 500m/256Mi (limits)
   - EmptyDir volumes for /tmp

4. **mcp-server/service.yaml** (17 lines)
   - ClusterIP service on port 8080
   - Uses mcpServer.labels helper

5. **mcp-server/serviceaccount.yaml** (10 lines)
   - Service account with automount enabled

6. **mcp-server/role.yaml** (13 lines)
   - RBAC role with configmaps/secrets read permissions

7. **mcp-server/rolebinding.yaml** (17 lines)
   - Binds mcp-server role to mcp-server service account

### Security (1 file)
8. **security/networkpolicy.yaml** (228 lines)
   - **Default Deny**: Blocks all ingress/egress by default
   - **Frontend Policies**:
     - Ingress: From ingress-nginx namespace on port 3000
     - Egress: To backend:8000 + DNS
   - **Backend Policies**:
     - Ingress: From frontend:8000 + Dapr sidecar:50001
     - Egress: To MCP server:8080, PostgreSQL:5432, HTTPS:443, Redis:6379, Dapr sidecar:50001, DNS
   - **MCP Server Policies**:
     - Ingress: From backend:8080
     - Egress: DNS only (minimal permissions)

### Dapr (2 files)
9. **dapr/config.yaml** (35 lines)
   - mTLS enabled (workloadCertTTL: 24h, allowedClockSkew: 15m)
   - Zipkin tracing with 100% sampling
   - Features: ServiceInvocation, State (PubSub disabled)
   - Access control: default deny, allow todo-backend

10. **dapr/statestore.yaml** (33 lines)
    - Type: state.redis
    - Version: v1
    - Scopes: [todo-backend]
    - Metadata: Uses redis-secret (host, password via secretKeyRef)
    - Redis config: TLS enabled, failover enabled, sentinel support, retry settings

## File Structure
```
phase-4/charts/todo-app/templates/
├── backend/
│   ├── deployment.yaml (64 lines) [existing]
│   ├── role.yaml (13 lines) [NEW]
│   ├── rolebinding.yaml (17 lines) [NEW]
│   ├── service.yaml (17 lines) [existing]
│   └── serviceaccount.yaml (10 lines) [existing]
├── mcp-server/
│   ├── deployment.yaml (51 lines) [NEW]
│   ├── role.yaml (13 lines) [NEW]
│   ├── rolebinding.yaml (17 lines) [NEW]
│   ├── service.yaml (17 lines) [NEW]
│   └── serviceaccount.yaml (10 lines) [NEW]
├── frontend/
│   ├── deployment.yaml (55 lines) [existing]
│   ├── ingress.yaml (30 lines) [existing]
│   ├── role.yaml (13 lines) [existing]
│   ├── rolebinding.yaml (17 lines) [existing]
│   ├── service.yaml (17 lines) [existing]
│   └── serviceaccount.yaml (10 lines) [existing]
├── security/
│   └── networkpolicy.yaml (228 lines) [NEW]
└── dapr/
    ├── config.yaml (35 lines) [NEW]
    └── statestore.yaml (33 lines) [NEW]
```

## Security Features
- **RBAC**: All components have dedicated service accounts with minimal permissions
- **Network Policies**: Zero-trust network segmentation with default deny
- **Pod Security**: runAsNonRoot, drop ALL capabilities, read-only filesystem
- **Dapr mTLS**: Mutual TLS for service-to-service communication
- **Secrets**: All sensitive data (DB, API keys, Redis) via Kubernetes secrets

## Helm Template Usage
All files use:
- `{{ .Values.* }}` for configuration values
- Helper functions from `_helpers.tpl`:
  - `todo-app.fullname`
  - `todo-app.backend.labels`
  - `todo-app.mcpServer.labels`
  - `todo-app.backend.serviceAccountName`
  - `todo-app.mcpServer.serviceAccountName`
- Conditional rendering: `{{- if .Values.rbac.create -}}`, `{{- if .Values.dapr.enabled -}}`

## Next Steps
1. Create `redis-secret` with host and password keys
2. Deploy Dapr to the cluster
3. Deploy the Helm chart: `helm install todo-app ./charts/todo-app -n todo --create-namespace`
4. Verify network policies: `kubectl get networkpolicies -n todo`
5. Test Dapr state store: `dapr components -k -n todo`
