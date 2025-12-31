# Phase 1: Data Model - Infrastructure Components

**Feature**: Cloud-Native Kubernetes Deployment  
**Date**: 2025-12-31  
**Purpose**: Define all infrastructure entities and their relationships

---

## Overview

This phase deals with **infrastructure components** rather than application data models. The "entities" are Kubernetes resources, Helm configurations, and Dapr components that comprise the deployment architecture.

---

## 1. Deployment Configuration

**Purpose**: Environment-specific settings for application deployments

**Attributes**:
- `environment`: Development | Production
- `namespace`: Kubernetes namespace (always "todo" for this phase)
- `replicaCount`: Number of pod instances (1 for dev, configurable for prod)
- `imagePullPolicy`: Never (local) | IfNotPresent | Always
- `domain`: Ingress hostname (todo.local for dev)

**Relationships**:
- Has many: Application Components
- Defines: Resource Quotas, Network Policies
- References: Secrets

**Validation Rules**:
- Namespace must be lowercase alphanumeric + hyphens
- Replica count must be >= 1
- Image pull policy must match environment (Never for local, IfNotPresent for remote registries)
- Domain must be valid hostname format

**State Transitions**:
```
Undefined → Configured → Validated → Applied → Running → Failed
                                                     ↓
                                                  Rolledback
```

---

## 2. Application Component

**Purpose**: Represents a deployable service (frontend, backend, MCP server)

**Attributes**:
- `name`: Component identifier (frontend | backend | mcp-server)
- `image.repository`: Docker image name
- `image.tag`: Specific version (never "latest")
- `service.port`: Container port (3000 for frontend, 8000 for backend)
- `service.type`: ClusterIP | NodePort | LoadBalancer
- `resources.requests`: Minimum guaranteed resources (CPU, memory)
- `resources.limits`: Maximum allowed resources (CPU, memory)
- `healthCheck.livenessProbe`: Endpoint/settings for liveness check
- `healthCheck.readinessProbe`: Endpoint/settings for readiness check
- `env[]`: Environment variables (name, value or secretRef)

**Relationships**:
- Belongs to: Deployment Configuration
- Has one: Service Account
- Has one (optional): Dapr Sidecar
- Has many: Env Variables (some reference Secrets)
- Exposed by: Service, Ingress (frontend only)

**Validation Rules**:
- Image tag must be semver or commit SHA (not "latest")
- Ports must be 1-65535
- Resources: requests <= limits
- Health check paths must start with /
- Service names must be DNS-compatible

**State Transitions**:
```
Defined → Built (Docker image) → Deployed → Running → Healthy
                                         ↓
                                     Failed → Rolledback
```

---

## 3. Kubernetes Pod

**Purpose**: Runtime instance of an Application Component

**Attributes**:
- `name`: Generated (component-name-{hash})
- `namespace`: Deployment namespace
- `phase`: Pending | Running | Succeeded | Failed | Unknown
- `containers[]`: Application container + optional Dapr sidecar
- `volumes[]`: Mounted volumes (secrets, config maps)
- `nodeSelector`: Scheduling constraints
- `securityContext`: User ID (1000), privileges (false), filesystem (readOnly)

**Relationships**:
- Instantiates: Application Component
- Contains: Container(s)
- Mounts: Secrets, ConfigMaps
- Scheduled on: Node (Minikube VM)
- Managed by: Deployment Controller

**Validation Rules**:
- Must run as non-root (UID > 0)
- Privilege escalation must be false
- Read-only root filesystem enforced (except specific writable volumes)
- All capabilities dropped except explicitly needed
- Resource requests and limits defined

**State Transitions**:
```
Pending → ContainerCreating → Running → Ready
              ↓                    ↓
          ImagePullBackOff     CrashLoopBackOff
                                   ↓
                              OOMKilled → Restarting
```

---

## 4. Service

**Purpose**: Network endpoint for accessing Application Component

**Attributes**:
- `name`: Component name (frontend-svc, backend-svc)
- `namespace`: Deployment namespace
- `type`: ClusterIP (internal) | NodePort | LoadBalancer
- `ports[]`: Port mappings (port, targetPort, protocol)
- `selector`: Labels to match pods
- `clusterIP`: Assigned internal IP
- `endpoints[]`: Pod IPs backing this service

**Relationships**:
- Exposes: Application Component (via label selector)
- Targets: Pods
- Referenced by: Ingress (frontend service)
- Used by: Other services (backend service used by frontend)

**Validation Rules**:
- Selector labels must match pod labels exactly
- Target ports must match container ports
- Service name must be DNS-compatible (lowercase, hyphens only)
- At least one port defined

**State Transitions**:
```
Defined → Created → Endpoints Available → Healthy
                        ↓
                  No Endpoints (pods not ready)
```

---

## 5. Ingress Route

**Purpose**: External HTTP access to frontend application

**Attributes**:
- `name`: todo-ingress
- `namespace`: Deployment namespace
- `ingressClassName`: nginx
- `host`: todo.local
- `paths[]`: URL paths and backend services
- `tls[]`: Optional TLS configuration (empty for local)
- `annotations`: NGINX-specific configuration

**Relationships**:
- Routes to: Frontend Service
- Managed by: NGINX Ingress Controller
- Accessed from: Host machine browser

**Validation Rules**:
- Host must be resolvable (via /etc/hosts)
- Backend service must exist in same namespace
- Path must be valid URL pattern
- Ingress class must be "nginx"

**State Transitions**:
```
Defined → Applied → Controller Reconciling → Address Assigned → Accessible
                                                    ↓
                                             No Address (controller not ready)
```

---

## 6. Service Account

**Purpose**: Kubernetes identity for application pods

**Attributes**:
- `name`: Component-specific (frontend-sa, backend-sa)
- `namespace`: Deployment namespace
- `secrets[]`: Automatically mounted service account tokens
- `imagePullSecrets[]`: Registry credentials (if needed)

**Relationships**:
- Used by: Pods
- Has: Role (RBAC permissions)
- Bound via: RoleBinding

**Validation Rules**:
- One service account per component (never use "default")
- Name must be DNS-compatible
- Must exist before pod creation

**State Transitions**:
```
Created → Token Generated → Mounted in Pod → Used for API Calls
```

---

## 7. Role & RoleBinding

**Purpose**: RBAC permissions for service accounts

**Attributes (Role)**:
- `name`: Component-specific role
- `namespace`: Scoped to deployment namespace
- `rules[]`: API groups, resources, verbs allowed

**Attributes (RoleBinding)**:
- `name`: Binds role to service account
- `roleRef`: References Role
- `subjects[]`: Service accounts granted permissions

**Relationships**:
- Role grants permissions for: Specific K8s resources
- RoleBinding connects: Service Account → Role

**Validation Rules**:
- Namespace-scoped only (no ClusterRole for applications)
- Minimal permissions (principle of least privilege)
- No wildcard permissions (*) except where absolutely necessary
- No sensitive verbs: bind, escalate, impersonate

**State Transitions**:
```
Defined → Applied → Enforced → Validated (by admission controllers)
```

---

## 8. Network Policy

**Purpose**: Control traffic between pods and external endpoints

**Attributes**:
- `name`: Component or flow-specific (frontend-to-backend, deny-all)
- `namespace`: Scoped to deployment namespace
- `podSelector`: Which pods this policy applies to
- `policyTypes[]`: Ingress, Egress, or both
- `ingress[]`: Allowed incoming traffic rules
- `egress[]`: Allowed outgoing traffic rules

**Relationships**:
- Applies to: Pods (via label selector)
- Allows traffic: Between specific pods/services
- Blocks: All traffic not explicitly allowed

**Validation Rules**:
- Default deny-all must exist
- Each allow rule must have clear business justification
- Port numbers must match service definitions
- Namespace selectors must reference valid namespaces

**State Transitions**:
```
Defined → Applied → Enforced by CNI → Traffic Filtered
```

---

## 9. Kubernetes Secret

**Purpose**: Encrypted storage for sensitive data

**Attributes**:
- `name`: Secret identifier (todo-secrets)
- `namespace`: Deployment namespace
- `type`: Opaque | kubernetes.io/tls | kubernetes.io/dockerconfigjson
- `data`: Base64-encoded key-value pairs
- `stringData`: Plain text (auto-encoded on create)

**Data Keys**:
```
todo-secrets:
  - database-url: PostgreSQL connection string
  - openai-api-key: AI model API key
  - better-auth-secret: Session encryption key
```

**Relationships**:
- Mounted by: Pods (as environment variables or files)
- Referenced by: Dapr Components (via secretKeyRef)
- Protected by: RBAC (read access only to specific service accounts)

**Validation Rules**:
- Never commit to Git
- Keys must be lowercase with hyphens
- Values must be base64-encoded in `data` field
- Type must match usage (Opaque for generic secrets)

**State Transitions**:
```
Created (kubectl/Helm) → Stored in etcd → Mounted in Pod → Used by App
                                                ↓
                                          Rotated (manual process)
```

---

## 10. Dapr Component

**Purpose**: Dapr building block configuration (state store, pub/sub, etc.)

**Attributes**:
- `name`: Component identifier (statestore, pubsub)
- `namespace`: Deployment namespace
- `type`: Dapr component type (state.redis, pubsub.redis, state.postgresql)
- `version`: Component version (v1)
- `metadata[]`: Component-specific configuration
- `scopes[]`: App IDs allowed to use this component
- `secretStoreComponent`: Optional secret store reference

**Relationships**:
- Used by: Backend service (via Dapr sidecar)
- References: Secrets (via secretKeyRef in metadata)
- Managed by: Dapr control plane

**Validation Rules**:
- Type must be valid Dapr component type
- Scopes must list specific app IDs (never empty)
- All credentials via secretKeyRef (never plain text)
- Version must be specified

**State Transitions**:
```
Defined → Applied → Loaded by Dapr → Available to Scoped Apps
```

---

## 11. Dapr Configuration

**Purpose**: Global Dapr settings (mTLS, tracing, metrics)

**Attributes**:
- `name`: dapr-config
- `namespace`: Deployment namespace
- `mtls.enabled`: true (always for security)
- `mtls.workloadCertTTL`: Certificate lifetime (24h for local)
- `mtls.allowedClockSkew`: Time sync tolerance (15m)
- `tracing`: Optional distributed tracing config
- `metric`: Optional metrics collection config

**Relationships**:
- Applied to: All Dapr sidecars in namespace
- Enforces: mTLS between services

**Validation Rules**:
- mTLS must be enabled (security requirement)
- Certificate TTL must be reasonable (not too short to cause rotation issues)
- Clock skew must account for local environment drift

**State Transitions**:
```
Defined → Applied → Loaded by Sidecars → Enforced (mTLS)
```

---

## 12. Helm Release

**Purpose**: Installed instance of the application

**Attributes**:
- `name`: Release name (todo-app)
- `namespace`: Deployment namespace
- `chart`: Chart reference (./charts/todo-app)
- `version`: Release version (increments on upgrade)
- `status`: deployed | failed | pending-install | pending-upgrade
- `values`: Merged values from values.yaml + values-dev.yaml
- `manifest`: Rendered Kubernetes YAML
- `hooks[]`: Pre/post install/upgrade hooks

**Relationships**:
- Creates: All Kubernetes resources (pods, services, secrets, etc.)
- Tracked by: Helm (stored as secrets in K8s)
- Can be: Upgraded, rolled back, uninstalled

**Validation Rules**:
- Chart must pass `helm lint`
- Rendered templates must be valid YAML
- All required values must be provided
- Namespace must exist before install

**State Transitions**:
```
Undefined → Installing → Deployed → Upgrading → Deployed
                ↓                        ↓
            Failed                   Failed → Rolledback
```

---

## Entity Relationship Diagram

```
Deployment Configuration
  ├─ Application Component (frontend)
  │    ├─ Pod (replicas)
  │    │    ├─ Container (frontend app)
  │    │    └─ SecurityContext
  │    ├─ Service (frontend-svc)
  │    ├─ Ingress (todo-ingress) → NGINX Controller
  │    ├─ Service Account (frontend-sa)
  │    │    └─ RoleBinding → Role
  │    └─ Network Policy (frontend egress)
  │
  ├─ Application Component (backend)
  │    ├─ Pod (replicas)
  │    │    ├─ Container (backend app)
  │    │    ├─ Container (dapr sidecar)
  │    │    └─ SecurityContext
  │    ├─ Service (backend-svc)
  │    ├─ Service Account (backend-sa)
  │    │    └─ RoleBinding → Role
  │    ├─ Network Policy (backend ingress/egress)
  │    └─ Dapr Component References
  │         ├─ statestore (Redis)
  │         └─ Dapr Configuration (mTLS)
  │
  ├─ Kubernetes Secrets (todo-secrets)
  │    ├─ database-url
  │    ├─ openai-api-key
  │    └─ better-auth-secret
  │
  └─ Helm Release (todo-app)
       ├─ Chart Templates
       ├─ Values (merged dev + base)
       └─ Release History

External Dependencies:
  - Neon PostgreSQL (via database-url secret)
  - OpenAI API (via openai-api-key secret)
  - Minikube Cluster (runtime environment)
  - Docker Registry (Minikube internal for local images)
```

---

## Component Lifecycle

### Creation Order (Dependencies)
1. **Namespace** (todo)
2. **Secrets** (todo-secrets)
3. **Service Accounts** (frontend-sa, backend-sa)
4. **Roles & RoleBindings** (RBAC)
5. **Dapr Configuration** (mTLS settings)
6. **Dapr Components** (statestore, pubsub)
7. **Network Policies** (deny-all, then allow rules)
8. **Services** (frontend-svc, backend-svc)
9. **Deployments** (creates Pods)
10. **Ingress** (exposes frontend)

### Deletion Order (Reverse)
1. **Ingress**
2. **Deployments** (stops Pods)
3. **Services**
4. **Network Policies**
5. **Dapr Components**
6. **Dapr Configuration**
7. **Roles & RoleBindings**
8. **Service Accounts**
9. **Secrets** (careful: may break running pods)
10. **Namespace** (deletes everything)

---

## Validation Summary

All infrastructure entities must pass these checks:
- **Security**: Non-root users, no privilege escalation, resource limits defined
- **RBAC**: Dedicated service accounts, minimal permissions, namespace-scoped
- **Network**: Default deny policies, explicit allow rules only
- **Secrets**: All credentials in Secrets, never plain text
- **Dapr**: mTLS enabled, scopes defined, secretKeyRef for credentials
- **Helm**: Charts linted, templates valid, values complete

---

## Next Steps

- **Phase 1 Continuation**: Generate API contracts (Helm values schemas)
- **Phase 1 Completion**: Create quickstart.md deployment guide
