#!/bin/bash
#
# Validate All Infrastructure Code
# Runs all constitution validators on a directory
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-.}"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory not found: $TARGET_DIR"
    echo "Usage: $0 <directory>"
    exit 1
fi

echo "=========================================="
echo "Constitution Validation Suite"
echo "Target: $TARGET_DIR"
echo "=========================================="
echo ""

TOTAL_FILES=0
PASSED_FILES=0
FAILED_FILES=0

# Validate Kubernetes manifests
echo "=== Validating Kubernetes Manifests ==="
K8S_FILES=$(find "$TARGET_DIR" -type f \( -name "*.yaml" -o -name "*.yml" \) ! -path "*/charts/*" ! -path "*/templates/*" ! -name "Chart.yaml" ! -name "values.yaml" 2>/dev/null || true)

if [ -n "$K8S_FILES" ]; then
    while IFS= read -r file; do
        # Skip if it's a Dapr component
        if grep -q "apiVersion.*dapr.io" "$file" 2>/dev/null; then
            continue
        fi

        # Skip if it's a Helm file
        if grep -q "{{ .Values" "$file" 2>/dev/null; then
            continue
        fi

        TOTAL_FILES=$((TOTAL_FILES + 1))
        echo "Checking: $file"

        if python3 "$SCRIPT_DIR/validate_k8s.py" "$file"; then
            PASSED_FILES=$((PASSED_FILES + 1))
        else
            FAILED_FILES=$((FAILED_FILES + 1))
        fi
    done <<< "$K8S_FILES"
else
    echo "No Kubernetes manifests found"
fi

echo ""

# Validate Helm charts
echo "=== Validating Helm Charts ==="
HELM_CHARTS=$(find "$TARGET_DIR" -type f -name "Chart.yaml" 2>/dev/null || true)

if [ -n "$HELM_CHARTS" ]; then
    while IFS= read -r chart_yaml; do
        CHART_DIR=$(dirname "$chart_yaml")
        TOTAL_FILES=$((TOTAL_FILES + 1))
        echo "Checking: $CHART_DIR"

        if python3 "$SCRIPT_DIR/validate_helm.py" "$CHART_DIR"; then
            PASSED_FILES=$((PASSED_FILES + 1))
        else
            FAILED_FILES=$((FAILED_FILES + 1))
        fi
    done <<< "$HELM_CHARTS"
else
    echo "No Helm charts found"
fi

echo ""

# Validate Dapr components
echo "=== Validating Dapr Components ==="
DAPR_FILES=$(find "$TARGET_DIR" -type f \( -name "*.yaml" -o -name "*.yml" \) -exec grep -l "apiVersion.*dapr.io" {} \; 2>/dev/null || true)

if [ -n "$DAPR_FILES" ]; then
    while IFS= read -r file; do
        TOTAL_FILES=$((TOTAL_FILES + 1))
        echo "Checking: $file"

        if python3 "$SCRIPT_DIR/validate_dapr.py" "$file"; then
            PASSED_FILES=$((PASSED_FILES + 1))
        else
            FAILED_FILES=$((FAILED_FILES + 1))
        fi
    done <<< "$DAPR_FILES"
else
    echo "No Dapr components found"
fi

echo ""
echo "=========================================="
echo "Validation Summary"
echo "=========================================="
echo "Total files checked: $TOTAL_FILES"
echo "Passed: $PASSED_FILES"
echo "Failed: $FAILED_FILES"
echo "=========================================="

if [ $FAILED_FILES -eq 0 ]; then
    echo "✓ All validations passed"
    exit 0
else
    echo "✗ Some validations failed"
    exit 1
fi
