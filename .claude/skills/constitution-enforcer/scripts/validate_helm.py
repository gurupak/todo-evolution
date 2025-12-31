#!/usr/bin/env python3
"""
Helm Chart Validator
Validates Helm charts against constitution security and governance rules.
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


class HelmValidator:
    def __init__(self):
        self.violations: List[ValidationResult] = []

    def validate_chart(self, chart_dir: str) -> Tuple[bool, List[ValidationResult]]:
        """Validate a Helm chart directory."""
        self.violations = []
        chart_path = Path(chart_dir)

        if not chart_path.exists():
            print(f"Error: Chart directory not found: {chart_dir}")
            return False, []

        # Validate Chart.yaml
        chart_yaml = chart_path / "Chart.yaml"
        if not chart_yaml.exists():
            self.violations.append(
                ValidationResult(
                    "HELM-001",
                    "CRITICAL",
                    "Missing Chart.yaml",
                    "Create Chart.yaml with name, version, and apiVersion",
                )
            )
            return False, self.violations

        # Validate values.yaml
        values_yaml = chart_path / "values.yaml"
        if values_yaml.exists():
            self._validate_values(values_yaml)

        # Validate templates
        templates_dir = chart_path / "templates"
        if templates_dir.exists():
            for template_file in templates_dir.glob("*.yaml"):
                self._validate_template(template_file)

        passed = all(v.severity != "CRITICAL" for v in self.violations)
        return passed, self.violations

    def _validate_values(self, values_file: Path):
        """Validate values.yaml for security defaults."""
        try:
            with open(values_file, "r") as f:
                values = yaml.safe_load(f)
        except Exception as e:
            self.violations.append(
                ValidationResult(
                    "HELM-002",
                    "CRITICAL",
                    f"Failed to parse values.yaml: {str(e)}",
                    str(values_file),
                    "Fix YAML syntax errors",
                )
            )
            return

        if not values:
            return

        # Check image configuration
        image = values.get("image", {})
        if isinstance(image, dict):
            tag = image.get("tag", "")
            if tag == "latest" or not tag:
                self.violations.append(
                    ValidationResult(
                        "IMG-001",
                        "CRITICAL",
                        "values.yaml uses 'latest' or no image tag",
                        f"{values_file}:image.tag",
                        "Set a specific version tag in values.yaml",
                    )
                )

            pull_policy = image.get("pullPolicy", "")
            if pull_policy == "Always":
                self.violations.append(
                    ValidationResult(
                        "IMG-002",
                        "WARNING",
                        "imagePullPolicy set to Always",
                        f"{values_file}:image.pullPolicy",
                        "Use IfNotPresent for specific tags",
                    )
                )

        # Check securityContext defaults
        security_context = values.get("securityContext", {})
        if isinstance(security_context, dict):
            if not security_context.get("runAsNonRoot", False):
                self.violations.append(
                    ValidationResult(
                        "SEC-002",
                        "CRITICAL",
                        "values.yaml missing securityContext.runAsNonRoot: true",
                        f"{values_file}:securityContext.runAsNonRoot",
                        "Set runAsNonRoot: true in values.yaml",
                    )
                )

            if security_context.get("allowPrivilegeEscalation", True):
                self.violations.append(
                    ValidationResult(
                        "SEC-003",
                        "CRITICAL",
                        "values.yaml allows privilege escalation",
                        f"{values_file}:securityContext.allowPrivilegeEscalation",
                        "Set allowPrivilegeEscalation: false",
                    )
                )

        # Check resources defaults
        resources = values.get("resources", {})
        if isinstance(resources, dict):
            requests = resources.get("requests", {})
            limits = resources.get("limits", {})

            if not requests:
                self.violations.append(
                    ValidationResult(
                        "RES-001",
                        "WARNING",
                        "values.yaml missing resource requests",
                        f"{values_file}:resources.requests",
                        "Add default CPU and memory requests",
                    )
                )

            if not limits:
                self.violations.append(
                    ValidationResult(
                        "RES-002",
                        "WARNING",
                        "values.yaml missing resource limits",
                        f"{values_file}:resources.limits",
                        "Add default CPU and memory limits",
                    )
                )

        # Check serviceAccount
        service_account = values.get("serviceAccount", {})
        if isinstance(service_account, dict):
            create = service_account.get("create", False)
            name = service_account.get("name", "")

            if not create and not name:
                self.violations.append(
                    ValidationResult(
                        "RBAC-001",
                        "WARNING",
                        "values.yaml may use default ServiceAccount",
                        f"{values_file}:serviceAccount",
                        "Set serviceAccount.create: true or provide a name",
                    )
                )

    def _validate_template(self, template_file: Path):
        """Validate template files for hardcoded values."""
        try:
            content = template_file.read_text()

            # Check for hardcoded secrets
            sensitive_keywords = ["password", "secret", "token", "key", "credential"]
            for keyword in sensitive_keywords:
                if (
                    f"{keyword}:" in content.lower()
                    and "{{"
                    not in content[
                        content.lower().index(f"{keyword}:") : content.lower().index(
                            f"{keyword}:"
                        )
                        + 50
                    ]
                ):
                    self.violations.append(
                        ValidationResult(
                            "DB-002",
                            "CRITICAL",
                            f"Potential hardcoded {keyword} in template",
                            str(template_file),
                            f"Use Helm values or Kubernetes Secrets for {keyword}",
                        )
                    )
                    break

            # Check for 'latest' tag in templates
            if ":latest" in content:
                self.violations.append(
                    ValidationResult(
                        "IMG-001",
                        "CRITICAL",
                        "Hardcoded 'latest' tag in template",
                        str(template_file),
                        "Use {{ .Values.image.tag }} instead of hardcoded tags",
                    )
                )

        except Exception as e:
            self.violations.append(
                ValidationResult(
                    "HELM-003",
                    "WARNING",
                    f"Failed to read template {template_file.name}: {str(e)}",
                    str(template_file),
                    "Check file permissions and encoding",
                )
            )


def print_report(passed: bool, violations: List[ValidationResult], chart_dir: str):
    """Print validation report."""
    print(f"\n{'=' * 80}")
    print(f"Helm Chart Violation Report: {chart_dir}")
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
        print("✓ No violations found - chart complies with constitution rules\n")

    status = "PASSED" if passed else "BLOCKED"
    print(f"### Status: {status}")
    print(f"{'=' * 80}\n")
    print(f"{'='*80}\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_helm.py <chart-directory>")
        sys.exit(1)

    chart_dir = sys.argv[1]

    validator = HelmValidator()
    passed, violations = validator.validate_chart(chart_dir)
    print_report(passed, violations, chart_dir)

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
