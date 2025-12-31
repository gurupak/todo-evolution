#!/bin/bash

# Phase IV - Docker Cleanup Script
# Removes unused images, containers, and volumes from Minikube's Docker daemon

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

print_warning() {
    echo -e "${BLUE}⚠ $1${NC}"
}

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Clean up Docker resources in Minikube context"
    echo ""
    echo "Options:"
    echo "  -a, --all             Remove all unused images (not just dangling)"
    echo "  -f, --force           Skip confirmation prompts"
    echo "  -h, --help            Show this help message"
    echo ""
    echo "Example:"
    echo "  $0                    # Interactive cleanup (dangling images only)"
    echo "  $0 --all              # Remove all unused images"
    echo "  $0 --all --force      # Remove all unused images without confirmation"
}

# Parse arguments
ALL_IMAGES=false
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--all)
            ALL_IMAGES=true
            shift
            ;;
        -f|--force)
            FORCE=true
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
print_info "Docker Cleanup for Minikube"
echo ""

# Step 1: Check if Minikube is running
print_info "Checking Minikube status..."
if ! minikube status &> /dev/null; then
    print_error "Minikube is not running. Please start it first."
    exit 1
fi
print_success "Minikube is running"

# Step 2: Set Docker environment to Minikube
print_info "Configuring Docker to use Minikube's Docker daemon..."
eval "$(minikube docker-env --shell bash | grep '^export')"
print_success "Docker environment configured"

# Step 3: Show current disk usage
echo ""
print_info "Current Docker disk usage:"
docker system df
echo ""

# Step 4: Remove stopped containers
print_info "Removing stopped containers..."
STOPPED_CONTAINERS=$(docker ps -aq -f status=exited)
if [ -z "$STOPPED_CONTAINERS" ]; then
    print_success "No stopped containers to remove"
else
    if [ "$FORCE" = true ]; then
        docker rm $STOPPED_CONTAINERS
        print_success "Removed stopped containers"
    else
        echo "Found stopped containers:"
        docker ps -a -f status=exited
        read -p "Remove these containers? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker rm $STOPPED_CONTAINERS
            print_success "Removed stopped containers"
        else
            print_warning "Skipped container removal"
        fi
    fi
fi

# Step 5: Remove dangling images
echo ""
print_info "Removing dangling images..."
DANGLING_IMAGES=$(docker images -f "dangling=true" -q)
if [ -z "$DANGLING_IMAGES" ]; then
    print_success "No dangling images to remove"
else
    if [ "$FORCE" = true ]; then
        docker rmi $DANGLING_IMAGES
        print_success "Removed dangling images"
    else
        echo "Found dangling images:"
        docker images -f "dangling=true"
        read -p "Remove these images? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker rmi $DANGLING_IMAGES
            print_success "Removed dangling images"
        else
            print_warning "Skipped dangling image removal"
        fi
    fi
fi

# Step 6: Remove all unused images (if --all flag)
if [ "$ALL_IMAGES" = true ]; then
    echo ""
    print_info "Removing all unused images..."

    if [ "$FORCE" = true ]; then
        docker image prune -a -f
        print_success "Removed all unused images"
    else
        print_warning "This will remove ALL images not used by running containers!"
        read -p "Continue? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker image prune -a -f
            print_success "Removed all unused images"
        else
            print_warning "Skipped unused image removal"
        fi
    fi
fi

# Step 7: Remove unused volumes
echo ""
print_info "Removing unused volumes..."
UNUSED_VOLUMES=$(docker volume ls -qf dangling=true)
if [ -z "$UNUSED_VOLUMES" ]; then
    print_success "No unused volumes to remove"
else
    if [ "$FORCE" = true ]; then
        docker volume prune -f
        print_success "Removed unused volumes"
    else
        echo "Found unused volumes:"
        docker volume ls -f dangling=true
        read -p "Remove these volumes? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker volume prune -f
            print_success "Removed unused volumes"
        else
            print_warning "Skipped volume removal"
        fi
    fi
fi

# Step 8: Remove unused networks
echo ""
print_info "Removing unused networks..."
if [ "$FORCE" = true ]; then
    docker network prune -f
    print_success "Removed unused networks"
else
    read -p "Remove unused networks? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker network prune -f
        print_success "Removed unused networks"
    else
        print_warning "Skipped network removal"
    fi
fi

# Step 9: Show final disk usage
echo ""
print_info "Final Docker disk usage:"
docker system df
echo ""

print_success "Docker cleanup completed!"
echo ""
print_info "To reclaim more space, you can run:"
echo "  $0 --all              # Remove all unused images"
echo "  docker system prune -a --volumes  # Nuclear option (removes everything unused)"
