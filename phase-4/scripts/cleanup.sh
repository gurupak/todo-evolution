#!/bin/bash

# Phase IV - Cleanup Script
# Remove all Kubernetes resources and stop Minikube

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
REDIS_RELEASE="redis"

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

print_cleanup() {
    echo -e "${BLUE}🧹 $1${NC}"
}

print_section() {
    echo -e "${CYAN}═══ $1 ═══${NC}"
}

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Clean up Kubernetes resources and stop Minikube"
    echo ""
    echo "Options:"
    echo "  -n, --namespace NAME      Kubernetes namespace (default: todo)"
    echo "  -r, --release NAME        Helm release name (default: todo-app)"
    echo "  --keep-namespace          Keep namespace after cleanup"
    echo "  --keep-minikube           Don't stop Minikube"
    echo "  --full                    Full cleanup including Minikube deletion"
    echo "  -y, --yes                 Skip confirmation prompts"
    echo "  -h, --help                Show this help message"
    echo ""
    echo "Example:"
    echo "  $0                        # Standard cleanup with prompts"
    echo "  $0 --yes                  # Auto-confirm cleanup"
    echo "  $0 --full --yes           # Complete cleanup including Minikube"
    echo "  $0 --keep-minikube        # Clean app but keep cluster running"
}

confirm() {
    local message=$1

    if [ "$AUTO_CONFIRM" = true ]; then
        return 0
    fi

    read -p "$message (y/n): " choice
    case "$choice" in
        y|Y ) return 0;;
        n|N ) return 1;;
        * ) echo "Invalid choice"; return 1;;
    esac
}

# Parse arguments
KEEP_NAMESPACE=false
KEEP_MINIKUBE=false
FULL_CLEANUP=false
AUTO_CONFIRM=false

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
        --keep-namespace)
            KEEP_NAMESPACE=true
            shift
            ;;
        --keep-minikube)
            KEEP_MINIKUBE=true
            shift
            ;;
        --full)
            FULL_CLEANUP=true
            shift
            ;;
        -y|--yes)
            AUTO_CONFIRM=true
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

echo ""
print_section "Phase IV Cleanup"
echo "Configuration:"
echo "  Namespace: $NAMESPACE"
echo "  Release: $RELEASE_NAME"
echo "  Keep Namespace: $KEEP_NAMESPACE"
echo "  Keep Minikube: $KEEP_MINIKUBE"
echo "  Full Cleanup: $FULL_CLEANUP"
echo ""

if ! confirm "Proceed with cleanup?"; then
    print_info "Cleanup cancelled"
    exit 0
fi

# Step 1: Check if kubectl is available
print_info "Checking kubectl..."
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl not found"
    exit 1
fi
print_success "kubectl found"

# Step 2: Check if Minikube is running
print_info "Checking Minikube status..."
if ! minikube status &> /dev/null; then
    print_info "Minikube is not running"
    MINIKUBE_RUNNING=false
else
    print_success "Minikube is running"
    MINIKUBE_RUNNING=true
fi

# Step 3: Uninstall Helm releases
if [ "$MINIKUBE_RUNNING" = true ]; then
    print_section "Uninstalling Helm Releases"

    # Check if helm is available
    if command -v helm &> /dev/null; then
        # Uninstall todo-app
        if helm list -n $NAMESPACE | grep -q $RELEASE_NAME; then
            print_cleanup "Uninstalling $RELEASE_NAME..."
            helm uninstall $RELEASE_NAME -n $NAMESPACE --wait
            print_success "$RELEASE_NAME uninstalled"
        else
            print_info "$RELEASE_NAME not found"
        fi

        # Uninstall Redis
        if helm list -n $NAMESPACE | grep -q $REDIS_RELEASE; then
            print_cleanup "Uninstalling $REDIS_RELEASE..."
            helm uninstall $REDIS_RELEASE -n $NAMESPACE --wait
            print_success "$REDIS_RELEASE uninstalled"
        else
            print_info "$REDIS_RELEASE not found"
        fi
    else
        print_info "Helm not found, skipping Helm cleanup"
    fi
fi

# Step 4: Delete namespace
if [ "$KEEP_NAMESPACE" = false ] && [ "$MINIKUBE_RUNNING" = true ]; then
    print_section "Deleting Namespace"

    if kubectl get namespace $NAMESPACE &> /dev/null; then
        print_cleanup "Deleting namespace $NAMESPACE..."
        kubectl delete namespace $NAMESPACE --wait=true --timeout=120s
        print_success "Namespace deleted"
    else
        print_info "Namespace $NAMESPACE not found"
    fi
else
    print_info "Keeping namespace $NAMESPACE"
fi

# Step 5: Remove DNS entry from hosts file
print_section "Removing DNS Entry"

# Check OS type
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    HOSTS_FILE="C:\\Windows\\System32\\drivers\\etc\\hosts"
    print_info "Detected Windows. Hosts file: $HOSTS_FILE"
    print_info "Please remove the following line from your hosts file manually (requires admin):"
    echo ""
    echo "  <minikube-ip> todo.local"
    echo ""
    print_info "Run as Administrator:"
    echo "  notepad $HOSTS_FILE"
else
    # Linux/Mac
    HOSTS_FILE="/etc/hosts"

    if grep -q "todo.local" "$HOSTS_FILE"; then
        print_cleanup "Removing todo.local from hosts file..."
        sudo sed -i.bak '/todo.local/d' "$HOSTS_FILE"
        print_success "DNS entry removed"
    else
        print_info "DNS entry not found in hosts file"
    fi
fi

# Step 6: Stop or delete Minikube
print_section "Minikube Cleanup"

if [ "$MINIKUBE_RUNNING" = true ]; then
    if [ "$FULL_CLEANUP" = true ]; then
        if confirm "Delete Minikube cluster completely?"; then
            print_cleanup "Deleting Minikube cluster..."
            minikube delete
            print_success "Minikube cluster deleted"
        fi
    elif [ "$KEEP_MINIKUBE" = false ]; then
        print_cleanup "Stopping Minikube..."
        minikube stop
        print_success "Minikube stopped"
    else
        print_info "Keeping Minikube running"
    fi
else
    print_info "Minikube is not running, skipping"
fi

# Step 7: Clean up Docker images (optional)
if [ "$FULL_CLEANUP" = true ] && [ "$MINIKUBE_RUNNING" = true ]; then
    print_section "Docker Image Cleanup"

    if confirm "Remove todo Docker images from Minikube?"; then
        # Set Docker env to Minikube
        eval $(minikube docker-env)

        print_cleanup "Removing todo Docker images..."
        docker images | grep -E "todo-backend|todo-frontend|todo-mcp-server" | awk '{print $1":"$2}' | xargs -r docker rmi -f || true
        print_success "Docker images removed"
    fi
fi

# Step 8: Display cleanup summary
print_section "Cleanup Summary"
echo ""
print_success "Cleanup Complete!"
echo ""
echo "Actions performed:"
if helm list -n $NAMESPACE &> /dev/null 2>&1; then
    echo "  ✓ Helm releases uninstalled"
fi
if [ "$KEEP_NAMESPACE" = false ]; then
    echo "  ✓ Namespace deleted"
else
    echo "  - Namespace kept"
fi
if [[ ! "$OSTYPE" == "msys" ]] && [[ ! "$OSTYPE" == "win32" ]]; then
    echo "  ✓ DNS entry removed"
else
    echo "  - DNS entry (manual removal required)"
fi
if [ "$FULL_CLEANUP" = true ]; then
    echo "  ✓ Minikube cluster deleted"
elif [ "$KEEP_MINIKUBE" = false ]; then
    echo "  ✓ Minikube stopped"
else
    echo "  - Minikube kept running"
fi
echo ""

if [ "$FULL_CLEANUP" = true ]; then
    print_info "To start fresh, run:"
    echo "  ./scripts/setup-minikube.sh"
    echo "  ./scripts/build-images.sh"
    echo "  ./scripts/deploy.sh"
elif [ "$KEEP_MINIKUBE" = true ]; then
    print_info "Minikube is still running. To redeploy:"
    echo "  ./scripts/deploy.sh"
else
    print_info "To start Minikube again:"
    echo "  minikube start"
    echo "  ./scripts/deploy.sh"
fi
echo ""
print_success "Environment cleaned!"
