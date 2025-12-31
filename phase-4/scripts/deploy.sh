#!/bin/bash

# Phase IV - Application Deployment Script
# Deploy todo-app to Kubernetes using Helm

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="todo"
RELEASE_NAME="todo-app"
CHART_PATH="./charts/todo-app"
VALUES_FILE="./charts/todo-app/values-dev.yaml"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Helper functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}➜ $1${NC}"
}

print_deploy() {
    echo -e "${BLUE}🚀 $1${NC}"
}

print_section() {
    echo -e "${CYAN}═══ $1 ═══${NC}"
}

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Deploy todo-app to Kubernetes using Helm"
    echo ""
    echo "Options:"
    echo "  -n, --namespace NAME      Kubernetes namespace (default: todo)"
    echo "  -r, --release NAME        Helm release name (default: todo-app)"
    echo "  -f, --values FILE         Values file (default: values-dev.yaml)"
    echo "  -e, --env-file FILE       Environment file for secrets"
    echo "  --skip-redis              Skip Redis installation"
    echo "  --dry-run                 Run in dry-run mode"
    echo "  -h, --help                Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 --namespace production --values values-prod.yaml"
    echo "  $0 --env-file .env.production"
}

create_secret_from_file() {
    local env_file=$1

    if [ ! -f "$env_file" ]; then
        print_error "Environment file not found: $env_file"
        return 1
    fi

    print_info "Creating secrets from $env_file..."

    # Parse .env file and create secret
    local secret_args=""
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ $key =~ ^#.*$ ]] && continue
        [[ -z $key ]] && continue

        # Remove quotes from value
        value=$(echo "$value" | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//")

        secret_args="$secret_args --from-literal=$key=$value"
    done < "$env_file"

    # Create or update secret
    kubectl create secret generic todo-app-secrets \
        -n $NAMESPACE \
        $secret_args \
        --dry-run=client -o yaml | kubectl apply -f -

    print_success "Secrets created from $env_file"
}

prompt_for_secrets() {
    print_info "Creating secrets interactively..."

    # Prompt for required secrets
    read -p "Enter DATABASE_URL (PostgreSQL connection string): " db_url
    read -p "Enter OPENAI_API_KEY: " openai_key
    read -sp "Enter BETTER_AUTH_SECRET: " auth_secret
    echo ""
    read -p "Enter BETTER_AUTH_URL (e.g., http://todo.local): " auth_url

    # Convert DATABASE_URL for frontend (Node.js pg library)
    # Replace postgresql+asyncpg:// with postgresql://
    db_url_frontend=$(echo "$db_url" | sed 's/postgresql+asyncpg:/postgresql:/')

    # Create secret
    kubectl create secret generic todo-app-secrets \
        -n $NAMESPACE \
        --from-literal=DATABASE_URL="$db_url" \
        --from-literal=DATABASE_URL_FRONTEND="$db_url_frontend" \
        --from-literal=OPENAI_API_KEY="$openai_key" \
        --from-literal=BETTER_AUTH_SECRET="$auth_secret" \
        --from-literal=BETTER_AUTH_URL="$auth_url" \
        --dry-run=client -o yaml | kubectl apply -f -

    print_success "Secrets created interactively"
}

# Parse arguments
SKIP_REDIS=false
DRY_RUN=false
ENV_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        -r|--release)
            RELEASE_NAME="$2"
            shift 2
            ;;
        -f|--values)
            VALUES_FILE="$2"
            shift 2
            ;;
        -e|--env-file)
            ENV_FILE="$2"
            shift 2
            ;;
        --skip-redis)
            SKIP_REDIS=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

cd "$PROJECT_ROOT"

echo ""
print_section "Phase IV Application Deployment"
echo "Configuration:"
echo "  Namespace: $NAMESPACE"
echo "  Release: $RELEASE_NAME"
echo "  Chart: $CHART_PATH"
echo "  Values: $VALUES_FILE"
echo "  Dry Run: $DRY_RUN"
echo ""

# Step 1: Check prerequisites
print_info "Checking prerequisites..."

if ! command -v kubectl &> /dev/null; then
    print_error "kubectl not found"
    exit 1
fi

if ! command -v helm &> /dev/null; then
    print_error "helm not found"
    exit 1
fi

if ! minikube status &> /dev/null; then
    print_error "Minikube is not running"
    echo "Run: ./scripts/setup-minikube.sh"
    exit 1
fi

print_success "Prerequisites checked"

# Step 2: Create namespace
print_section "Creating Namespace"
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
print_success "Namespace '$NAMESPACE' ready"

# Step 3: Create secrets
print_section "Creating Secrets"

if [ -n "$ENV_FILE" ]; then
    create_secret_from_file "$ENV_FILE"
elif [ -f "$PROJECT_ROOT/.env" ]; then
    print_info "Found .env file in project root"
    read -p "Create secrets from .env? (y/n): " use_env
    if [[ $use_env == "y" ]]; then
        create_secret_from_file "$PROJECT_ROOT/.env"
    else
        prompt_for_secrets
    fi
else
    prompt_for_secrets
fi

# Step 4: Deploy Redis
if [ "$SKIP_REDIS" = false ]; then
    print_section "Deploying Redis"

    # Add bitnami repo if not exists
    if ! helm repo list | grep -q bitnami; then
        print_info "Adding Bitnami Helm repository..."
        helm repo add bitnami https://charts.bitnami.com/bitnami
    fi

    helm repo update

    # Deploy Redis
    print_info "Installing Redis with Helm..."
    helm upgrade --install redis bitnami/redis \
        --namespace $NAMESPACE \
        --set auth.enabled=false \
        --set master.persistence.enabled=false \
        --set replica.persistence.enabled=false \
        --set replica.replicaCount=0 \
        --wait \
        --timeout 5m

    print_success "Redis deployed successfully"
else
    print_info "Skipping Redis installation"
fi

# Step 5: Lint Helm chart
print_section "Linting Helm Chart"
helm lint $CHART_PATH

if [ $? -eq 0 ]; then
    print_success "Chart lint passed"
else
    print_error "Chart lint failed"
    exit 1
fi

# Step 6: Deploy application
print_section "Deploying Application"

HELM_CMD="helm upgrade --install $RELEASE_NAME $CHART_PATH \
    --namespace $NAMESPACE \
    --values $VALUES_FILE \
    --wait \
    --atomic \
    --timeout 10m"

if [ "$DRY_RUN" = true ]; then
    HELM_CMD="$HELM_CMD --dry-run --debug"
    print_info "Running in dry-run mode..."
fi

print_deploy "Deploying $RELEASE_NAME..."
eval $HELM_CMD

if [ $? -eq 0 ]; then
    print_success "Application deployed successfully"
else
    print_error "Deployment failed"
    echo ""
    print_info "Checking pod status..."
    kubectl get pods -n $NAMESPACE
    exit 1
fi

# Step 7: Get deployment status
print_section "Deployment Status"

echo ""
print_info "Pods:"
kubectl get pods -n $NAMESPACE -o wide

echo ""
print_info "Services:"
kubectl get svc -n $NAMESPACE

echo ""
print_info "Ingress:"
kubectl get ingress -n $NAMESPACE

# Step 8: Show Dapr status
print_section "Dapr Status"
kubectl get pods -n $NAMESPACE -l "dapr.io/enabled=true" -o custom-columns=\
NAME:.metadata.name,\
READY:.status.containerStatuses[*].ready,\
DAPR:.metadata.annotations.dapr\\.io/enabled

# Step 9: Wait for pods to be ready
if [ "$DRY_RUN" = false ]; then
    print_section "Waiting for Pods"

    print_info "Waiting for backend pods..."
    kubectl wait --for=condition=ready pod \
        -l app.kubernetes.io/name=todo-backend \
        -n $NAMESPACE \
        --timeout=300s || true

    print_info "Waiting for frontend pods..."
    kubectl wait --for=condition=ready pod \
        -l app.kubernetes.io/name=todo-frontend \
        -n $NAMESPACE \
        --timeout=300s || true

    print_info "Waiting for mcp-server pods..."
    kubectl wait --for=condition=ready pod \
        -l app.kubernetes.io/name=todo-mcp-server \
        -n $NAMESPACE \
        --timeout=300s || true

    print_success "All pods are ready"
fi

# Step 10: Display access information
print_section "Access Information"

MINIKUBE_IP=$(minikube ip)
echo ""
print_success "Deployment Complete!"
echo ""
echo "Access the application:"
echo "  Frontend: http://todo.local"
echo "  Backend API: http://todo.local/api"
echo "  Minikube IP: $MINIKUBE_IP"
echo ""
echo "Useful Commands:"
echo "  View logs (backend):    kubectl logs -f -l app.kubernetes.io/name=todo-backend -n $NAMESPACE"
echo "  View logs (frontend):   kubectl logs -f -l app.kubernetes.io/name=todo-frontend -n $NAMESPACE"
echo "  View logs (mcp-server): kubectl logs -f -l app.kubernetes.io/name=todo-mcp-server -n $NAMESPACE"
echo "  Port forward (backend): kubectl port-forward -n $NAMESPACE svc/todo-backend 8000:8000"
echo "  Describe pods:          kubectl describe pods -n $NAMESPACE"
echo "  Get all resources:      kubectl get all -n $NAMESPACE"
echo ""
echo "Helm Commands:"
echo "  Status:    helm status $RELEASE_NAME -n $NAMESPACE"
echo "  Values:    helm get values $RELEASE_NAME -n $NAMESPACE"
echo "  Upgrade:   helm upgrade $RELEASE_NAME $CHART_PATH -n $NAMESPACE"
echo "  Rollback:  helm rollback $RELEASE_NAME -n $NAMESPACE"
echo ""
print_info "Note: Make sure 'todo.local' is in your /etc/hosts file pointing to $MINIKUBE_IP"
echo ""
print_success "Happy deploying!"
