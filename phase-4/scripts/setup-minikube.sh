#!/bin/bash

# Phase IV - Minikube Cluster Setup Script
# Initializes Minikube with required addons and Dapr

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
CPUS=4
MEMORY=8192
DRIVER=docker
CLUSTER_NAME=minikube

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

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Initialize Minikube cluster for Phase IV deployment"
    echo ""
    echo "Options:"
    echo "  -c, --cpus NUM        Number of CPUs (default: 4)"
    echo "  -m, --memory MB       Memory in MB (default: 8192)"
    echo "  -d, --driver DRIVER   Driver to use (default: docker)"
    echo "  -h, --help            Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 --cpus 6 --memory 12288"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--cpus)
            CPUS="$2"
            shift 2
            ;;
        -m|--memory)
            MEMORY="$2"
            shift 2
            ;;
        -d|--driver)
            DRIVER="$2"
            shift 2
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
print_info "Starting Minikube Cluster Setup"
echo "Configuration:"
echo "  CPUs: $CPUS"
echo "  Memory: ${MEMORY}MB"
echo "  Driver: $DRIVER"
echo ""

# Step 1: Check if Minikube is installed
print_info "Checking Minikube installation..."
if ! command -v minikube &> /dev/null; then
    print_error "Minikube is not installed. Please install it first."
    echo "Visit: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi
print_success "Minikube found: $(minikube version --short)"

# Step 2: Check if kubectl is installed
print_info "Checking kubectl installation..."
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed. Please install it first."
    exit 1
fi
print_success "kubectl found: $(kubectl version --client --short 2>/dev/null || kubectl version --client)"

# Step 3: Check if Dapr CLI is installed
print_info "Checking Dapr CLI installation..."
if ! command -v dapr &> /dev/null; then
    print_error "Dapr CLI is not installed. Please install it first."
    echo "Visit: https://docs.dapr.io/getting-started/install-dapr-cli/"
    exit 1
fi
print_success "Dapr CLI found: $(dapr version 2>/dev/null | grep 'CLI version' || echo 'installed')"

# Step 4: Start Minikube
print_info "Starting Minikube cluster..."
if minikube status &> /dev/null; then
    print_info "Minikube is already running. Restarting with new configuration..."
    minikube stop
fi

minikube start \
    --cpus=$CPUS \
    --memory=$MEMORY \
    --driver=$DRIVER \
    --kubernetes-version=stable

if [ $? -eq 0 ]; then
    print_success "Minikube cluster started successfully"
else
    print_error "Failed to start Minikube cluster"
    exit 1
fi

# Step 5: Enable required addons
print_info "Enabling ingress addon..."
minikube addons enable ingress
print_success "Ingress addon enabled"

print_info "Enabling metrics-server addon..."
minikube addons enable metrics-server
print_success "Metrics-server addon enabled"

# Step 6: Install Dapr
print_info "Installing Dapr on Kubernetes..."
dapr init -k --wait --timeout 300

if [ $? -eq 0 ]; then
    print_success "Dapr installed successfully"
else
    print_error "Failed to install Dapr"
    exit 1
fi

# Step 7: Verify Dapr installation
print_info "Verifying Dapr installation..."
kubectl wait --for=condition=ready pod \
    -l app=dapr-operator \
    -n dapr-system \
    --timeout=300s

kubectl wait --for=condition=ready pod \
    -l app=dapr-sidecar-injector \
    -n dapr-system \
    --timeout=300s

kubectl wait --for=condition=ready pod \
    -l app=dapr-sentry \
    -n dapr-system \
    --timeout=300s

kubectl wait --for=condition=ready pod \
    -l app=dapr-placement-server \
    -n dapr-system \
    --timeout=300s

print_success "Dapr components are ready"

# Step 8: Add DNS entry to /etc/hosts
print_info "Configuring DNS entry for todo.local..."
MINIKUBE_IP=$(minikube ip)

if [ -z "$MINIKUBE_IP" ]; then
    print_error "Failed to get Minikube IP"
    exit 1
fi

# Check OS type
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    HOSTS_FILE="C:\\Windows\\System32\\drivers\\etc\\hosts"
    print_info "Detected Windows. Hosts file: $HOSTS_FILE"
    print_info "Please add the following line to your hosts file manually (requires admin):"
    echo ""
    echo "  $MINIKUBE_IP todo.local"
    echo ""
    print_info "Run as Administrator:"
    echo "  notepad $HOSTS_FILE"
else
    # Linux/Mac
    HOSTS_FILE="/etc/hosts"

    # Remove old entry if exists
    if grep -q "todo.local" "$HOSTS_FILE"; then
        print_info "Removing old todo.local entry..."
        sudo sed -i.bak '/todo.local/d' "$HOSTS_FILE"
    fi

    # Add new entry
    echo "$MINIKUBE_IP todo.local" | sudo tee -a "$HOSTS_FILE" > /dev/null
    print_success "Added DNS entry: $MINIKUBE_IP todo.local"
fi

# Step 9: Verify cluster readiness
print_info "Verifying cluster readiness..."
kubectl cluster-info

# Wait for all system pods to be ready
kubectl wait --for=condition=ready pod --all -n kube-system --timeout=300s
print_success "All system pods are ready"

# Step 10: Display cluster information
echo ""
print_success "Minikube Cluster Setup Complete!"
echo ""
echo "Cluster Information:"
echo "  Minikube IP: $MINIKUBE_IP"
echo "  Kubernetes: $(kubectl version --short 2>/dev/null | grep Server || kubectl version -o json | grep gitVersion)"
echo "  Context: $(kubectl config current-context)"
echo "  Nodes: $(kubectl get nodes --no-headers | wc -l)"
echo ""
echo "Enabled Addons:"
minikube addons list | grep enabled
echo ""
echo "Dapr Status:"
dapr status -k
echo ""
print_info "Next Steps:"
echo "  1. Build Docker images: ./scripts/build-images.sh"
echo "  2. Deploy application: ./scripts/deploy.sh"
echo ""
print_success "Ready for deployment!"
