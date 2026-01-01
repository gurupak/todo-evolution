# Tasks: Cloud-Native Kubernetes Deployment

**Feature**: Cloud-Native Kubernetes Deployment  
**Branch**: `005-phase4-k8s-deployment`  
**Date**: 2025-12-31  
**Status**: Ready for implementation

## Overview

This task list implements Phase IV: deploying the Todo AI Chatbot (from Phase 3) to local Kubernetes using Minikube, Helm charts, Dapr service mesh, and production-grade security patterns.

**Total Tasks**: 131  
**Estimated Time**: 19-27 hours  
**Test Approach**: Manual verification using quickstart.md checklist

## Task Organization

Tasks are organized by user story (P1-P5) to enable:
- **Independent Implementation**: Each story can be developed separately
- **Incremental Testing**: Test after completing each story
- **Parallel Opportunities**: [P] markers indicate parallelizable tasks
- **MVP First**: Complete User Story 1 (P1) for minimum viable deployment

## Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational - Helm + Docker)
    ↓
├─ User Story 1 (P1) - Basic Deployment ← START HERE (MVP)
│   ↓
├─ User Story 2 (P2) - Security (depends on US1)
│   ↓
├─ User Story 3 (P3) - Dapr Service Mesh (depends on US2)
│   ↓
├─ User Story 4 (P4) - Helm Packaging (depends on US3)
│   ↓
└─ User Story 5 (P5) - Database Connectivity (depends on US4)
    ↓
Phase N (Polish)
```

**MVP Scope**: Phase 1 + Phase 2 + User Story 1 (P1) = **54 tasks**  
**Full Feature**: All phases = **131 tasks**

---

## Phase 1: Setup & Prerequisites

**Goal**: Initialize project structure and prepare environment  
**Independent Test**: Directory structure exists and prerequisites are verified

### Tasks

- [x] T001 Create phase-4 directory structure at hackathon-todo/phase-4/
- [x] T002 Create subdirectories: backend/, frontend/, mcp-server/, charts/todo-app/, k8s/, scripts/
- [x] T003 Create Helm templates structure: charts/todo-app/templates/{frontend,backend,mcp-server,security,dapr}/
- [x] T004 [P] Verify Docker Desktop installed and running (version 4.53+)
- [x] T005 [P] Verify Minikube installed (run `minikube version`)
- [x] T006 [P] Verify Helm installed (run `helm version`, expect 3.x)
- [x] T007 [P] Verify kubectl installed (run `kubectl version --client`)
- [x] T008 [P] Verify Dapr CLI installed (run `dapr version`, expect 1.12+)
- [x] T009 Copy phase-3/backend/ to phase-4/backend/
- [x] T010 Copy phase-3/frontend/ to phase-4/frontend/
- [x] T011 Copy phase-3/mcp-server/ to phase-4/mcp-server/

**Acceptance Criteria**:
- ✅ phase-4/ directory exists with all subdirectories (including mcp-server/)
- ✅ All prerequisite tools installed and verified
- ✅ Application code copied from phase-3 (backend, frontend, mcp-server)

---

## Phase 2: Foundational - Docker & Helm Foundation

**Goal**: Create containerization and Helm chart foundation (blocking for all user stories)  
**Independent Test**: Docker images build successfully, Helm chart structure passes lint

### Tasks

- [x] T012 [P] Create phase-4/backend/.dockerignore with common Python exclusions
- [x] T013 [P] Create phase-4/backend/Dockerfile (multi-stage: builder + runtime, python:3.13-slim, non-root user 1000) - Suggested Gordon prompt: "create optimized multi-stage Dockerfile for FastAPI with UV package manager"
- [x] T014 [P] Create phase-4/frontend/.dockerignore with common Node exclusions  
- [x] T015 [P] Create phase-4/frontend/Dockerfile (multi-stage: builder + runtime, node:20-alpine, non-root user 1000) - Suggested Gordon prompt: "create production Dockerfile for Next.js 15 App Router with output standalone"
- [x] T016 Build backend Docker image: `docker build -t todo-backend:1.0.0 ./phase-4/backend`
- [x] T017 Build frontend Docker image: `docker build -t todo-frontend:1.0.0 ./phase-4/frontend`
- [x] T018 Verify backend image size < 300MB (run `docker images | grep todo-backend`)
- [x] T019 Verify frontend image size < 200MB (run `docker images | grep todo-frontend`)
- [x] T020 [P] Create charts/todo-app/Chart.yaml with metadata (name: todo-app, version: 1.0.0, appVersion: 1.0.0)
- [x] T021 [P] Create charts/todo-app/values.yaml with production defaults
- [x] T022 [P] Create charts/todo-app/values-dev.yaml with Minikube overrides (imagePullPolicy: Never)
- [x] T023 [P] Create charts/todo-app/templates/_helpers.tpl with template helper functions
- [x] T024 Run `helm lint charts/todo-app` and verify zero errors/warnings

**Acceptance Criteria**:
- ✅ Backend, frontend, and MCP server Dockerfiles use multi-stage builds
- ✅ Images meet size targets (backend < 300MB, frontend < 200MB, mcp-server < 200MB)
- ✅ All containers run as non-root user (UID 1000)
- ✅ Helm chart structure passes lint

---

## Phase 3: User Story 1 (P1) - Basic Deployment

**Story**: Deploy Application Locally on Kubernetes  
**Goal**: Deploy frontend and backend to Minikube with basic functionality working  
**Independent Test**: Access http://todo.local and verify chat functionality works end-to-end

### Tasks

- [x] T025 [US1] Create templates/frontend/deployment.yaml with security context (runAsNonRoot: true, runAsUser: 1000, readOnlyRootFilesystem: true)
- [x] T026 [US1] Add frontend resource limits to deployment (requests: 100m CPU/128Mi memory, limits: 500m CPU/256Mi memory)
- [x] T027 [US1] Add frontend health checks to deployment (livenessProbe: /, readinessProbe: /)
- [x] T028 [US1] Create templates/frontend/service.yaml (type: ClusterIP, port: 3000)
- [x] T029 [US1] Create templates/frontend/ingress.yaml (host: todo.local, ingressClassName: nginx, backend: frontend-svc:3000)
- [x] T030 [US1] Create templates/backend/deployment.yaml with security context (same as frontend)
- [x] T031 [US1] Add backend resource limits to deployment (requests: 200m CPU/256Mi memory, limits: 1000m CPU/512Mi memory)
- [x] T032 [US1] Add backend health checks to deployment (livenessProbe: /health, readinessProbe: /health)
- [x] T033 [US1] Create templates/backend/service.yaml (type: ClusterIP, port: 8000)
- [x] T034 [P] [US1] Create phase-4/mcp-server/.dockerignore with common Python exclusions
- [x] T035 [P] [US1] Create phase-4/mcp-server/Dockerfile (multi-stage: builder + runtime, python:3.13-slim, non-root user 1000) - Suggested Gordon prompt: "create optimized multi-stage Dockerfile for FastMCP server with UV"
- [x] T036 [US1] Build MCP server Docker image: `docker build -t todo-mcp-server:1.0.0 ./phase-4/mcp-server`
- [x] T037 [US1] Verify MCP server image size < 200MB (run `docker images | grep todo-mcp-server`)
- [x] T038 [US1] Create templates/mcp-server/deployment.yaml with security context (runAsNonRoot: true, runAsUser: 1000, readOnlyRootFilesystem: true)
- [x] T039 [US1] Add MCP server resource limits to deployment (requests: 100m CPU/128Mi memory, limits: 500m CPU/256Mi memory)
- [x] T040 [US1] Add MCP server health checks to deployment (livenessProbe: /health, readinessProbe: /health)
- [x] T041 [US1] Create templates/mcp-server/service.yaml (type: ClusterIP, port: 8080)
- [x] T042 [US1] Create k8s/namespace.yaml (name: todo, labels: env=development)
- [x] T043 [US1] Start Minikube: `minikube start --cpus=4 --memory=8192 --driver=docker`
- [x] T044 [US1] Enable NGINX Ingress: `minikube addons enable ingress`
- [x] T045 [US1] Point Docker to Minikube: `eval $(minikube docker-env)`
- [x] T046 [US1] Rebuild images in Minikube's Docker daemon (frontend, backend, mcp-server)
- [x] T047 [US1] Configure local DNS: Add "$(minikube ip) todo.local" to /etc/hosts
- [x] T048 [US1] Deploy with Helm: `helm install todo-app ./charts/todo-app -f values-dev.yaml -n todo --create-namespace`
- [x] T049 [US1] Verify all pods Running/Ready: `kubectl get pods -n todo` (expect frontend 1/1, backend 1/1, mcp-server 1/1)
- [x] T050 [US1] Verify services have endpoints: `kubectl get endpoints -n todo`
- [x] T051 [US1] Verify ingress accessible: `curl -I http://todo.local` (expect HTTP 200)
- [x] T052 [US1] Access http://todo.local in browser and verify frontend loads
- [x] T053 [US1] Test end-to-end chat functionality (send message, receive AI response)
- [x] T054 [US1] Verify backend can invoke MCP server tools (check backend logs for MCP tool calls)

**Acceptance Criteria** (from spec.md):
1. ✅ **AS-001**: All application components running in Kubernetes pods with "Running" status
2. ✅ **AS-002**: Todo AI Chatbot interface loads successfully in browser
3. ✅ **AS-003**: Messages processed and responses received (end-to-end connectivity)
4. ✅ **AS-004**: Health endpoints return successful status codes

**Independent Test**: Can be fully tested by deploying all application components to Minikube and verifying the frontend is accessible via browser at a local URL, chat functionality works end-to-end, and all services are running healthy.

---

## Phase 4: User Story 2 (P2) - Security Configuration

**Story**: Secure Container and Network Configuration  
**Goal**: Apply security best practices (RBAC, NetworkPolicies, security contexts)  
**Independent Test**: Inspect pod configurations and verify security standards (non-root, resource limits, network policies active)

**Depends On**: User Story 1 (P1) - requires working deployment

### Tasks

- [x] T055 [P] [US2] Create templates/frontend/serviceaccount.yaml (name: frontend-sa)
- [x] T056 [P] [US2] Create templates/frontend/role.yaml with minimal RBAC permissions (namespace-scoped, read ConfigMaps/Secrets)
- [x] T057 [P] [US2] Create templates/frontend/rolebinding.yaml binding frontend-sa to frontend role
- [x] T058 [P] [US2] Create templates/backend/serviceaccount.yaml (name: backend-sa)
- [x] T059 [P] [US2] Create templates/backend/role.yaml with minimal RBAC permissions (namespace-scoped, read ConfigMaps/Secrets)
- [x] T060 [P] [US2] Create templates/backend/rolebinding.yaml binding backend-sa to backend role
- [x] T061 [P] [US2] Create templates/mcp-server/serviceaccount.yaml (name: mcp-server-sa)
- [x] T062 [P] [US2] Create templates/mcp-server/role.yaml with minimal RBAC permissions (namespace-scoped, read ConfigMaps/Secrets)
- [x] T063 [P] [US2] Create templates/mcp-server/rolebinding.yaml binding mcp-server-sa to mcp-server role
- [x] T064 [US2] Update frontend/deployment.yaml to use frontend-sa service account
- [x] T065 [US2] Update backend/deployment.yaml to use backend-sa service account
- [x] T066 [US2] Update mcp-server/deployment.yaml to use mcp-server-sa service account
- [x] T067 [US2] Create templates/security/networkpolicy.yaml with default deny-all policy
- [x] T068 [US2] Add NetworkPolicy rule allowing frontend → backend:8000
- [x] T069 [US2] Add NetworkPolicy rule allowing backend → mcp-server:8080
- [x] T070 [US2] Add NetworkPolicy rule allowing backend → external (PostgreSQL)
- [x] T071 [US2] Upgrade Helm release: `helm upgrade todo-app ./charts/todo-app -f values-dev.yaml -n todo --wait`
- [x] T072 [US2] Verify security contexts: `kubectl get pod -n todo <pod-name> -o yaml | grep -A 5 securityContext`
- [x] T073 [US2] Confirm non-root: All containers show runAsUser: 1000
- [x] T074 [US2] Confirm privilege escalation disabled: allowPrivilegeEscalation: false
- [x] T075 [US2] Verify resource limits: `kubectl describe pod -n todo <pod-name> | grep -A 10 Limits`
- [x] T076 [US2] Verify service accounts: `kubectl get sa -n todo` (expect frontend-sa, backend-sa, mcp-server-sa)
- [x] T077 [US2] Verify network policies: `kubectl get networkpolicy -n todo` (expect at least deny-all)
- [x] T078 [US2] Test network isolation: Attempt unauthorized connection and verify it's blocked

**Acceptance Criteria** (from spec.md):
1. ✅ **AS-005**: All containers run as non-root users with UID/GID 1000
2. ✅ **AS-006**: Privilege escalation disabled, read-only root filesystems enforced
3. ✅ **AS-007**: Unauthorized network connections blocked per network policies
4. ✅ **AS-008**: Every container has CPU and memory requests and limits defined
5. ✅ **AS-009**: Each application has dedicated service account with minimal permissions

**Independent Test**: Can be fully tested by inspecting deployed pod configurations and verifying they meet security standards (non-root users, resource limits, network policies in place), delivering secure-by-default deployments.

---

## Phase 5: User Story 3 (P3) - Dapr Service Mesh

**Story**: Service Mesh Integration with Dapr  
**Goal**: Enable Dapr sidecars, mTLS, and state management  
**Independent Test**: Verify Dapr sidecars running, mTLS active, Redis state store functional

**Depends On**: User Story 2 (P2) - requires security configuration

### Tasks

- [x] T089 [US3] Install Dapr on cluster: `dapr init -k --wait`
- [x] T090 [US3] Verify Dapr system pods: `kubectl get pods -n dapr-system` (all Running)
- [x] T081 [P] [US3] Create templates/dapr/config.yaml with mTLS enabled (workloadCertTTL: 24h, allowedClockSkew: 15m)
- [x] T082 [P] [US3] Create templates/dapr/statestore.yaml (type: state.redis, scopes: [todo-backend], connectionString via secretKeyRef)
- [x] T088 [US3] Update backend/deployment.yaml with Dapr annotations (dapr.io/enabled: "true", dapr.io/app-id: "todo-backend", dapr.io/app-port: "8000")
- [x] T089 [US3] Add Dapr sidecar resource limits annotations (cpu-request: 100m, memory-request: 128Mi, cpu-limit: 300m, memory-limit: 256Mi)
- [x] T090 [US3] Deploy Redis for Dapr state store: `helm install redis oci://registry-1.docker.io/bitnamicharts/redis --set auth.enabled=false --set master.persistence.enabled=false -n todo` (ephemeral for local dev)
- [x] T091 [US3] Create Kubernetes secret for Redis connection string (if authentication required)
- [x] T092 [US3] Upgrade Helm release with Dapr components
- [x] T088 [US3] Verify backend pod has 2 containers: `kubectl get pod -n todo <backend-pod> -o jsonpath='{.spec.containers[*].name}'` (expect: backend, daprd)
- [x] T089 [US3] Check Dapr sidecar logs: `kubectl logs -n todo <backend-pod> -c daprd | grep mTLS`
- [x] T090 [US3] Verify mTLS enabled: `dapr status -k` (check configuration)
- [x] T091 [US3] Test state store: Use backend API to save state, verify persisted in Redis
- [x] T092 [US3] Verify Dapr components: `dapr components -k -n todo` (expect statestore with scopes)

**Acceptance Criteria** (from spec.md):
1. ✅ **AS-010**: Each pod has both application container and Dapr sidecar running
2. ✅ **AS-011**: mTLS enabled with appropriate certificate TTL settings
3. ✅ **AS-012**: All service-to-service communication encrypted via mTLS
4. ✅ **AS-013**: State persisted and retrievable through Dapr APIs
5. ✅ **AS-014**: Sidecars have defined CPU and memory limits

**Independent Test**: Can be fully tested by deploying Dapr-enabled applications and verifying sidecar containers are running alongside application containers, mTLS is active between services, and Dapr components (state store, pub/sub) are functional.

---

## Phase 6: User Story 4 (P4) - Helm Packaging

**Story**: Package Management with Helm Charts  
**Goal**: Refine Helm charts for multi-environment support and validation  
**Independent Test**: Install/upgrade with different values files, verify all resources created correctly

**Depends On**: User Story 3 (P3) - requires Dapr integration complete

### Tasks

- [x] T093 [P] [US4] Create values-prod.yaml with production settings (replicaCount: 3, stricter security, real image registry)
- [x] T094 [P] [US4] Document all Helm values in charts/todo-app/README.md
- [x] T105 [P] [US5] [US4] Add NOTES.txt template with post-install instructions
- [x] T101 [US4] Validate Chart.yaml dependencies field (if using sub-charts)
- [x] T102 [US4] Run `helm lint charts/todo-app` with all values files
- [x] T103 [US4] Test template rendering: `helm template todo-app ./charts/todo-app -f values-dev.yaml`
- [x] T104 [US4] Test template rendering: `helm template todo-app ./charts/todo-app -f values-prod.yaml`
- [x] T100 [US4] Perform dry-run install: `helm install todo-app ./charts/todo-app -f values-prod.yaml -n todo-prod --dry-run --debug`
- [x] T101 [US4] Test upgrade: Change image tag in values-dev.yaml and run `helm upgrade todo-app ./charts/todo-app -f values-dev.yaml -n todo`
- [x] T102 [US4] Verify automatic rollback: Intentionally break deployment and confirm `--atomic` flag rolls back
- [x] T103 [US4] Test rollback command: `helm rollback todo-app 1 -n todo`
- [x] T104 [US4] Verify sub-chart deployment: Check frontend, backend resources created from single install

**Acceptance Criteria** (from spec.md):
1. ✅ **AS-015**: All Kubernetes resources created successfully with development values
2. ✅ **AS-016**: Updates applied without manual manifest editing (via helm upgrade)
3. ✅ **AS-017**: Production configurations applied correctly (higher replicas, stricter security)
4. ✅ **AS-018**: No errors or warnings from `helm lint` and `helm template`
5. ✅ **AS-019**: All sub-charts deployed correctly from main chart install

**Independent Test**: Can be fully tested by installing the application using Helm commands, upgrading releases with different configuration values, and verifying all resources are created correctly, delivering production-ready packaging.

---

## Phase 7: User Story 5 (P5) - Database Connectivity

**Story**: External Database Connectivity  
**Goal**: Connect to Neon PostgreSQL with SSL, verify persistence across restarts  
**Independent Test**: Configure secrets, verify backend connects to PostgreSQL with SSL, data persists across pod restarts

**Depends On**: User Story 4 (P4) - requires Helm packaging

### Tasks

- [x] T105 [P] [US5] [US5] Create k8s/secrets-template.yaml with structure (database-url, openai-api-key, better-auth-secret keys)
- [x] T131 [US5] Create actual Kubernetes secret: `kubectl create secret generic todo-secrets --from-literal=database-url="postgresql://..." --from-literal=openai-api-key="sk-..." --from-literal=better-auth-secret="..." -n todo`
- [x] T127 [US5] Update backend/deployment.yaml to reference secrets via secretKeyRef for DATABASE_URL
- [x] T128 [US5] Update backend/deployment.yaml to reference secrets via secretKeyRef for OPENAI_API_KEY
- [x] T129 [US5] Update backend/deployment.yaml to reference secrets via secretKeyRef for BETTER_AUTH_SECRET
- [x] T115 [US5] Verify connection string has sslmode=require
- [x] T116 [US5] Upgrade Helm release with secret references
- [x] T117 [US5] Verify backend pod starts successfully with database connection
- [x] T118 [US5] Check backend logs for successful PostgreSQL connection: `kubectl logs -n todo <backend-pod> -c backend | grep -i postgres`
- [x] T119 [US5] Test CRUD operations via chat interface (create task, update, delete)
- [x] T115 [US5] Verify data persisted in Neon PostgreSQL (query database directly or via API)
- [x] T131 [US5] Delete backend pod: `kubectl delete pod -n todo <backend-pod>`
- [x] T127 [US5] Wait for pod to restart, verify data still exists (persistence test)
- [x] T128 [US5] Test connection pooling: Send multiple concurrent requests and monitor connections
- [x] T129 [US5] Test credential rotation: Update secret, restart pods, verify new credentials used

**Acceptance Criteria** (from spec.md):
1. ✅ **AS-020**: Backend establishes connection to Neon PostgreSQL using credentials from secret
2. ✅ **AS-021**: Connection string has SSL/TLS mode set to "require"
3. ✅ **AS-022**: Data persists to PostgreSQL and survives pod restarts
4. ✅ **AS-023**: Database connections efficiently managed without exhausting limits
5. ✅ **AS-024**: New credentials used after secret update and pod restart

**Independent Test**: Can be fully tested by configuring database connection secrets, deploying the application, and verifying the backend can read/write data to Neon PostgreSQL with SSL encryption enabled.

---

## Phase 8: Polish & Automation

**Goal**: Create automation scripts and documentation  
**Independent Test**: Scripts execute successfully and documentation is complete

### Tasks

- [x] T130 [P] Create scripts/setup-minikube.sh (start Minikube, enable addons, install Dapr, configure DNS)
- [x] T131 [P] Create scripts/build-images.sh (point to Minikube Docker, build frontend and backend)
- [x] T127 [P] Create scripts/deploy.sh (create namespace, secrets, helm install with validation)
- [x] T128 [P] Create scripts/cleanup.sh (helm uninstall, delete namespace, remove DNS entry, stop Minikube)
- [x] T129 [P] Create phase-4/README.md with overview, prerequisites, quick start
- [x] T130 [P] Document troubleshooting guide in README.md (common issues from quickstart.md)
- [x] T131 Test setup-minikube.sh on clean environment
- [x] T127 Test build-images.sh and verify images appear in Minikube
- [x] T128 Test deploy.sh end-to-end (from namespace creation to verification)
- [x] T129 Test cleanup.sh and verify all resources removed
- [x] T130 Make all scripts executable: `chmod +x scripts/*.sh`
- [x] T131 Add scripts to version control: `git add scripts/`

**Acceptance Criteria**:
- ✅ All automation scripts execute successfully
- ✅ README.md provides clear quick start instructions
- ✅ Troubleshooting guide covers common issues
- ✅ Scripts are idempotent (can run multiple times safely)

---

## Parallel Execution Opportunities

### Within Each Phase

**Phase 1 (Setup)**:
- T004-T008 can run in parallel (tool verification)

**Phase 2 (Foundational)**:
- T011-T014 can run in parallel (Dockerfile creation)
- T019-T022 can run in parallel (Helm chart files)

**Phase 3 (User Story 1)**:
- After T033 (namespace creation), deployment files can be created in parallel but deployment must be sequential

**Phase 4 (User Story 2)**:
- T045-T050 can run in parallel (ServiceAccount, Role, RoleBinding creation)

**Phase 5 (User Story 3)**:
- T066-T067 can run in parallel (Dapr config files)

**Phase 6 (User Story 4)**:
- T078-T080 can run in parallel (documentation tasks)

**Phase 7 (User Story 5)**:
- T090 can run in parallel with other file creation tasks

**Phase 8 (Polish)**:
- T105-T110 can run in parallel (script and documentation creation)

### Across User Stories

**Cannot Parallelize**:
- User stories have sequential dependencies (P1 → P2 → P3 → P4 → P5)
- Each story builds on the previous one's infrastructure

**Can Parallelize** (within each story phase):
- File creation tasks marked with [P]
- Documentation tasks marked with [P]

---

## Success Criteria Mapping

**From Specification (12 Success Criteria)**:

1. **SC-001**: All pods Running/Ready within 5 minutes → Verified in T040
2. **SC-002**: Frontend page load < 3 seconds → Verified in T043
3. **SC-003**: End-to-end chat < 10 seconds → Verified in T044
4. **SC-004**: Health checks return 200 → Verified in T042
5. **SC-005**: Zero security violations → Verified in T057-T063
6. **SC-006**: Dapr mTLS 100% established → Verified in T074-T075
7. **SC-007**: Helm install succeeds (dev + prod) → Verified in T082-T085
8. **SC-008**: Data persists across restarts → Verified in T100-T102
9. **SC-009**: Database uses SSL → Verified in T095, T098
10. **SC-010**: 80% first-attempt success → Validated by quickstart.md testing
11. **SC-011**: Images meet size targets → Verified in T017-T018
12. **SC-012**: Automatic recovery → Verified in T101-T102

---

## MVP Recommendation

**Minimum Viable Product** (deploy and access application):
- Phase 1: Setup (10 tasks)
- Phase 2: Foundational (13 tasks)
- Phase 3: User Story 1 - Basic Deployment (21 tasks)

**Total MVP**: 44 tasks  
**Estimated Time**: 4-6 hours

**MVP Deliverables**:
- ✅ Application deployed to Minikube
- ✅ Frontend accessible at http://todo.local
- ✅ Chat functionality working end-to-end
- ✅ All pods running healthy

**Beyond MVP** (add security, Dapr, Helm polish, database):
- Phase 4-7: User Stories 2-5 (61 additional tasks)
- Phase 8: Polish (12 tasks)

---

## Implementation Strategy

1. **Start with MVP** (Phases 1-3): Get application deployed and working
2. **Add Security** (Phase 4): Harden deployment with RBAC and NetworkPolicies
3. **Enable Service Mesh** (Phase 5): Add Dapr for mTLS and state management
4. **Polish Packaging** (Phase 6): Refine Helm charts for production readiness
5. **Connect Database** (Phase 7): Enable full persistence
6. **Automate** (Phase 8): Create scripts for repeatable deployment

---

## Task Format Validation

✅ **All tasks follow required format**:
- Checkbox: `- [ ]`
- Task ID: T001-T116 (sequential)
- [P] marker: 31 parallelizable tasks identified
- [Story] label: All user story tasks labeled (US1-US5)
- File paths: Included where applicable
- Clear descriptions: Actionable and specific

---

## Notes

- **No automated tests**: Specification does not require TDD approach, using manual verification via quickstart.md checklist instead
- **AI Tool Integration**: Tasks reference Gordon, kubectl-ai, kagent but don't require them (optional productivity enhancers)
- **Validation Gates**: Each phase includes verification tasks based on pre/post-deployment gates from plan.md
- **Independent Stories**: Each user story (P1-P5) can be independently tested per spec requirements

---

**Ready for Implementation** - Start with T001 and proceed sequentially within each phase. Parallelize tasks marked with [P] where possible.
