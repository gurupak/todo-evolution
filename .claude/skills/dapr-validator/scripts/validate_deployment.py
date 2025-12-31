#!/usr/bin/env python3
"""
Dapr Deployment Validator
Validates Dapr sidecar annotations in Kubernetes deployments.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


class ValidationResult:
    def __init__(self, code: str, severity: str, message: str, location: str, fix: str):
        self.code = code
        self.severity = severity
        self.message = message
        self.location = location
        self.fix = fix


    REQUIRED_ANNOTATIONS = ["dapr.io/enabled", "dapr.io/app-id", "dapr.io/app-port"]

    RESOURCE_ANNOTATIONS = [
        "dapr.io/sidecar-cpu-request",
        "dapr.io/sidecar-memory-request",
        "dapr.io/sidecar-cpu-limit",
        "dapr.io/sidecar-memory-limit",
    ]

    def __init__(self):
        self.violations: List[ValidationResult] = []

    def validate_file(self, filepath: str) -> Tuple[bool, List[ValidationResult]]:
        """Validate a deployment file for Dapr annotations."""
        self.violations = []

        try:
            with open(filepath, "r") as f:
                docs = yaml.safe_load_all(f)
                for doc in docs:
                    if doc and isinstance(doc, dict):
                        self._validate_document(doc, filepath)
        except Exception as e:
            self.violations.append(
                ValidationResult(
                    "PARSE-001",
                    "CRITICAL",
                    f"Failed to parse YAML: {str(e)}",
                    filepath,
                    "Fix YAML syntax errors",
                )
            )
            return False, self.violations

        passed = all(v.severity != "CRITICAL" for v in self.violations)
        return passed, self.violations

    def _validate_document(self, doc: Dict[str, Any], filepath: str):
        """Validate a single Kubernetes document."""
        kind = doc.get("kind", "")

        if kind in ["Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob"]:
            self._validate_workload(doc, filepath)

    def _validate_workload(self, doc: Dict[str, Any], filepath: str):
        """Validate workload resources for Dapr annotations."""
        kind = doc.get("kind")
        spec = doc.get("spec", {})

        # Get template based on resource type
        if kind == "CronJob":
            template = spec.get("jobTemplate", {}).get("spec", {}).get("template", {})
        elif kind == "Job":
            template = spec.get("template", {})
        else:
            template = spec.get("template", {})

        template_metadata = template.get("metadata", {})
        annotations = template_metadata.get("annotations", {})

        # Check if Dapr is enabled
        dapr_enabled = annotations.get("dapr.io/enabled", "false").lower() == "true"

        if not dapr_enabled:
            # Not a Dapr-enabled deployment, skip validation
            return

        # Validate required annotations
        for annotation in self.REQUIRED_ANNOTATIONS:
            if annotation not in annotations:
                self.violations.append(
                    ValidationResult(
                        "DAPR-006" if "app-id" in annotation else "DAPR-010",
                        "CRITICAL",
                        f"Missing required Dapr annotation: {annotation}",
                        f"{filepath}:spec.template.metadata.annotations",
                        f"Add {annotation} annotation",
                    )
                )

        # Check app-id format
        app_id = annotations.get("dapr.io/app-id", "")
        if app_id:
            if not self._is_valid_app_id(app_id):
                self.violations.append(
                    ValidationResult(
                        "DAPR-006",
                        "WARNING",
                        f"Invalid app-id format: {app_id}",
                        f"{filepath}:spec.template.metadata.annotations.dapr.io/app-id",
                        "Use lowercase with hyphens (e.g., 'todo-backend')",
                    )
                )

        # Check for resource limits
        missing_resources = []
        for annotation in self.RESOURCE_ANNOTATIONS:
            if annotation not in annotations:
                missing_resources.append(annotation)

        if missing_resources:
            self.violations.append(
                ValidationResult(
                    "DAPR-007",
                    "WARNING",
                    f"Missing sidecar resource limits: {', '.join(missing_resources)}",
                    f"{filepath}:spec.template.metadata.annotations",
                    "Add sidecar CPU/memory requests and limits",
                )
            )

        # Validate app-port is numeric
        app_port = annotations.get("dapr.io/app-port", "")
        if app_port:
            try:
                port = int(app_port)
                if port < 1 or port > 65535:
                    raise ValueError()
            except ValueError:
                self.violations.append(
                    ValidationResult(
                        "DAPR-010",
                        "CRITICAL",
                        f"Invalid app-port value: {app_port}",
                        f"{filepath}:spec.template.metadata.annotations.dapr.io/app-port",
                        "Set app-port to a valid port number (1-65535)",
                    )
                )

    def _is_valid_app_id(self, app_id: str) -> bool:
        """Check if app-id follows naming convention."""
        # Should be lowercase with hyphens
        import re

        pattern = r"^[a-z][a-z0-9-]*[a-z0-9]$"
        return bool(re.match(pattern, app_id))


def print_report(passed: bool, violations: List[ValidationResult], filepath: str):
    """Print validation report."""
    print(f"\n{'=' * 80}")
    print(f"Dapr Deployment Validation Report: {filepath}")
    print(f"{'=' * 80}\n")

    critical = [v for v in violations if v.severity == "CRITICAL"]
    warnings = [v for v in violations if v.severity == "WARNING"]

    if critical:
        print("### CRITICAL (Must Fix)\n")
        for idx, v in enumerate(critical, 1):
            print(f"{idx}. [{v.code}] {v.message}")
            print(f"   - Location: {v.location}")
            print(f"   - Fix: {v.fix}\n")

    if warnings:
        print("### WARNING (Should Fix)\n")
        for idx, v in enumerate(warnings, 1):
            print(f"{idx}. [{v.code}] {v.message}")
            print(f"   - Location: {v.location}")
            print(f"   - Fix: {v.fix}\n")

    if not violations:
        print("✓ No violations found - deployment complies with Dapr best practices\n")

    status = "PASSED" if passed else "BLOCKED"
    print(f"### Status: {status}")
    print(f"{'=' * 80}\n")
    print(f"{'='*80}\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_deployment.py <deployment-file.yaml>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not Path(filepath).exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    validator = DaprDeploymentValidator()
    passed, violations = validator.validate_file(filepath)
    print_report(passed, violations, filepath)

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
