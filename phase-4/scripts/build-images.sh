#!/bin/bash

# Phase IV - Docker Image Build Script
# Builds backend, frontend, and mcp-server images in Minikube context

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TAG="${TAG:-1.0.0}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Image size targets (in MB)
BACKEND_TARGET=300
FRONTEND_TARGET=200
MCP_TARGET=200

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

print_build() {
    echo -e "${BLUE}🔨 $1${NC}"
}

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Build Docker images for Phase IV deployment in Minikube context"
    echo ""
    echo "Options:"
    echo "  -t, --tag TAG         Image tag (default: 1.0.0)"
    echo "  -s, --skip-verify     Skip image size verification"
    echo "  -h, --help            Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  TAG                   Override image tag"
    echo ""
    echo "Example:"
    echo "  $0 --tag 1.1.0"
    echo "  TAG=dev $0"
}

verify_size() {
    local image=$1
    local target_mb=$2

    # Get image size in MB
    local size_bytes=$(docker images --format "{{.Size}}" "$image" | head -1)

    # Convert to MB (handle different formats: MB, GB, KB)
    if [[ $size_bytes == *"GB"* ]]; then
        local size_mb=$(echo $size_bytes | sed 's/GB//' | awk '{print int($1 * 1024)}')
    elif [[ $size_bytes == *"MB"* ]]; then
        local size_mb=$(echo $size_bytes | sed 's/MB//' | awk '{print int($1)}')
    elif [[ $size_bytes == *"KB"* ]]; then
        local size_mb=$(echo $size_bytes | sed 's/KB//' | awk '{print int($1 / 1024)}')
    else
        print_error "Unable to parse image size: $size_bytes"
        return 1
    fi

    echo "  Size: ${size_mb}MB (target: <${target_mb}MB)"

    # Use awk for comparison instead of bc
    if awk "BEGIN {exit !($size_mb > $target_mb)}"; then
        print_error "Image size ${size_mb}MB exceeds target ${target_mb}MB"
        return 1
    else
        print_success "Image size within target"
        return 0
    fi
}

# Parse arguments
SKIP_VERIFY=false
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--tag)
            TAG="$2"
            shift 2
            ;;
        -s|--skip-verify)
            SKIP_VERIFY=true
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
print_info "Building Docker Images for Phase IV"
echo "Configuration:"
echo "  Tag: $TAG"
echo "  Project Root: $PROJECT_ROOT"
echo "  Skip Verification: $SKIP_VERIFY"
echo ""

# Step 1: Check if Minikube is running
print_info "Checking Minikube status..."
if ! minikube status &> /dev/null; then
    print_error "Minikube is not running. Please start it first."
    echo "Run: ./scripts/setup-minikube.sh"
    exit 1
fi
print_success "Minikube is running"

# Step 2: Set Docker environment to Minikube
print_info "Configuring Docker to use Minikube's Docker daemon..."
# Use --shell bash to ensure proper output format, and filter out non-export lines
eval "$(minikube docker-env --shell bash | grep '^export')"
print_success "Docker environment configured"

# Step 3: Build Backend Image
print_build "Building backend image (todo-backend:$TAG)..."
cd "$PROJECT_ROOT/backend"

if [ ! -f "Dockerfile" ]; then
    print_error "Backend Dockerfile not found at $PROJECT_ROOT/backend/Dockerfile"
    exit 1
fi

docker build \
    -t todo-backend:$TAG \
    -t todo-backend:latest \
    --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
    --build-arg VERSION=$TAG \
    .

if [ $? -eq 0 ]; then
    print_success "Backend image built successfully"

    if [ "$SKIP_VERIFY" = false ]; then
        verify_size "todo-backend:$TAG" $BACKEND_TARGET
    fi
else
    print_error "Failed to build backend image"
    exit 1
fi

# Step 4: Build Frontend Image
print_build "Building frontend image (todo-frontend:$TAG)..."
# Frontend is in phase-3/frontend, use Dockerfile from phase-4/frontend
FRONTEND_DOCKERFILE="$PROJECT_ROOT/frontend/Dockerfile"
FRONTEND_APP_ROOT="$(cd "$PROJECT_ROOT/../phase-3/frontend" && pwd)"

if [ ! -f "$FRONTEND_DOCKERFILE" ]; then
    print_error "Frontend Dockerfile not found at $FRONTEND_DOCKERFILE"
    exit 1
fi

if [ ! -d "$FRONTEND_APP_ROOT" ]; then
    print_error "Frontend app directory not found at $FRONTEND_APP_ROOT"
    exit 1
fi

echo "  Dockerfile: $FRONTEND_DOCKERFILE"
echo "  Build context: $FRONTEND_APP_ROOT"

cd "$FRONTEND_APP_ROOT"

docker build \
    -f "$FRONTEND_DOCKERFILE" \
    -t todo-frontend:$TAG \
    -t todo-frontend:latest \
    --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
    --build-arg VERSION=$TAG \
    .

if [ $? -eq 0 ]; then
    print_success "Frontend image built successfully"

    if [ "$SKIP_VERIFY" = false ]; then
        verify_size "todo-frontend:$TAG" $FRONTEND_TARGET
    fi
else
    print_error "Failed to build frontend image"
    exit 1
fi

# Step 5: Skip MCP Server Image (integrated into backend)
print_info "MCP Server is integrated into backend - skipping separate build"

# Step 6: List built images
echo ""
print_info "Listing built images..."
echo ""
docker images | grep -E "todo-backend|todo-frontend|REPOSITORY" | head -10

# Step 7: Verify images exist
echo ""
print_info "Verifying all images..."
IMAGES=("todo-backend:$TAG" "todo-frontend:$TAG")
ALL_EXIST=true

for image in "${IMAGES[@]}"; do
    if docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^$image$"; then
        print_success "$image exists"
    else
        print_error "$image not found"
        ALL_EXIST=false
    fi
done

# Step 8: Display summary
echo ""
if [ "$ALL_EXIST" = true ]; then
    print_success "All Docker Images Built Successfully!"
    echo ""
    echo "Built Images:"
    echo "  - todo-backend:$TAG (includes MCP server)"
    echo "  - todo-frontend:$TAG"
    echo ""
    print_info "Next Steps:"
    echo "  1. Deploy to Kubernetes: ./scripts/deploy.sh"
    echo "  2. Check deployment status: kubectl get pods -n todo"
    echo ""
    print_success "Ready for deployment!"
else
    print_error "Some images failed to build. Please check the errors above."
    exit 1
fi

# Return to project root
cd "$PROJECT_ROOT"
