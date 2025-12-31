#!/bin/bash

# Script to merge phase-4 branch to main

set -e

echo "🔍 Checking current git status..."
git status

echo ""
echo "📝 Adding all changes..."
git add .

echo ""
echo "💾 Committing changes..."
git commit -m "feat: Complete Phase 4 Kubernetes deployment

- Built Docker images for backend and frontend
- Created Helm chart for todo-app deployment
- Configured Minikube cluster with ingress
- Deployed Redis for state management
- Connected to Neon PostgreSQL database
- Fixed Better Auth cookie configuration for HTTP
- Configured service mesh communication
- Added secrets management
- Tested full authentication and task management flow" || echo "No changes to commit"

echo ""
echo "📤 Pushing current branch..."
git push origin 005-phase4-k8s-deployment

echo ""
echo "🔄 Switching to main branch..."
git checkout main

echo ""
echo "⬇️  Pulling latest from main..."
git pull origin main

echo ""
echo "🔀 Merging 005-phase4-k8s-deployment into main..."
git merge 005-phase4-k8s-deployment -m "Merge Phase 4 Kubernetes deployment into main"

echo ""
echo "📤 Pushing to main..."
git push origin main

echo ""
echo "✅ Successfully merged and pushed to main!"
echo ""
echo "Current branch:"
git branch --show-current
