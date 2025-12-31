#!/usr/bin/env python3
"""
Kubernetes Manifest Validator
Validates K8s manifests against constitution security and governance rules.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


class ValidationResult:
    def __init__(self, code: str, severity: str, message: str, location: str, fix: str):
        self.code = code
        self.severity = severity  # CRITICAL or WARNING
        self.message = message
        self.location = location
        self.fix = fix


class K8sValidator:
    def __init__(self):
        self.violations: List[ValidationResult] = []

    def validate_file(self, filepath: str) -> Tuple[bool, List[ValidationResult]]:
        """Validate a Kubernetes manifest file."""
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
        kind = doc.get("kind", "Unknown")

        if kind in ["Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob"]:
            self._validate_workload(doc, filepath)
        elif kind == "Role":
            self._validate_role(doc, filepath)
        elif kind == "RoleBinding":
            self._validate_rolebinding(doc, filepath)
        elif kind == "ClusterRole":
            self._validate_clusterrole(doc, filepath)
        elif kind == "NetworkPolicy":
            pass  # NetworkPolicy existence is good

    def _validate_workload(self, doc: Dict[str, Any], filepath: str):
        """Validate workload resources (Deployment, StatefulSet, etc.)."""
        kind = doc.get("kind")
        metadata = doc.get("metadata", {})
        spec = doc.get("spec", {})

        # Get template based on resource type
        if kind == "CronJob":
            template = spec.get("jobTemplate", {}).get("spec", {}).get("template", {})
        elif kind == "Job":
            template = spec.get("template", {})
        else:
            template = spec.get("template", {})

        template_spec = template.get("spec", {})

        # Check ServiceAccount
        service_account = template_spec.get("serviceAccountName", "default")
        if service_account == "default":
            self.violations.append(
                ValidationResult(
                    "RBAC-001",
                    "CRITICAL",
                    "Using default ServiceAccount",
                    f"{filepath}:spec.template.spec.serviceAccountName",
                    "Create and use a dedicated ServiceAccount for this workload",
                )
            )

        # Validate containers
        containers = template_spec.get("containers", [])
        for idx, container in enumerate(containers):
            self._validate_container(container, filepath, f"containers[{idx}]")

    def _validate_container(self, container: Dict[str, Any], filepath: str, path: str):
        """Validate container security settings."""
        name = container.get("name", "unnamed")

        # Check image tag
        image = container.get("image", "")
        if ":latest" in image or ":" not in image:
            self.violations.append(
                ValidationResult(
                    "IMG-001",
                    "CRITICAL",
                    f"Container '{name}' uses 'latest' or no tag",
                    f"{filepath}:spec.template.spec.{path}.image",
                    "Use specific version tags (e.g., 'myapp:1.2.3')",
                )
            )

        # Check securityContext
        security_ctx = container.get("securityContext", {})

        if not security_ctx:
            self.violations.append(
                ValidationResult(
                    "SEC-001",
                    "CRITICAL",
                    f"Container '{name}' missing securityContext",
                    f"{filepath}:spec.template.spec.{path}.securityContext",
                    "Add securityContext with runAsNonRoot, allowPrivilegeEscalation, etc.",
                )
            )
            return

        # Check runAsNonRoot
        if not security_ctx.get("runAsNonRoot", False):
            self.violations.append(
                ValidationResult(
                    "SEC-002",
                    "CRITICAL",
                    f"Container '{name}' may run as root",
                    f"{filepath}:spec.template.spec.{path}.securityContext.runAsNonRoot",
                    "Set runAsNonRoot: true",
                )
            )

        # Check allowPrivilegeEscalation
        if security_ctx.get("allowPrivilegeEscalation", True):
            self.violations.append(
                ValidationResult(
                    "SEC-003",
                    "CRITICAL",
                    f"Container '{name}' allows privilege escalation",
                    f"{filepath}:spec.template.spec.{path}.securityContext.allowPrivilegeEscalation",
                    "Set allowPrivilegeEscalation: false",
                )
            )

        # Check readOnlyRootFilesystem
        if not security_ctx.get("readOnlyRootFilesystem", False):
            self.violations.append(
                ValidationResult(
                    "SEC-004",
                    "WARNING",
                    f"Container '{name}' has writable root filesystem",
                    f"{filepath}:spec.template.spec.{path}.securityContext.readOnlyRootFilesystem",
                    "Set readOnlyRootFilesystem: true (use emptyDir volumes for temp data)",
                )
            )

        # Check capabilities
        capabilities = security_ctx.get("capabilities", {})
        drop = capabilities.get("drop", [])
        if "ALL" not in drop:
            self.violations.append(
                ValidationResult(
                    "SEC-005",
                    "CRITICAL",
                    f"Container '{name}' does not drop all capabilities",
                    f"{filepath}:spec.template.spec.{path}.securityContext.capabilities.drop",
                    "Set capabilities.drop: [ALL]",
                )
            )

        # Check resources
        resources = container.get("resources", {})
        requests = resources.get("requests", {})
        limits = resources.get("limits", {})

        if not requests.get("cpu"):
            self.violations.append(
                ValidationResult(
                    "RES-001",
                    "CRITICAL",
                    f"Container '{name}' missing CPU request",
                    f"{filepath}:spec.template.spec.{path}.resources.requests.cpu",
                    "Add resources.requests.cpu (e.g., '100m')",
                )
            )

        if not requests.get("memory"):
            self.violations.append(
                ValidationResult(
                    "RES-003",
                    "CRITICAL",
                    f"Container '{name}' missing memory request",
                    f"{filepath}:spec.template.spec.{path}.resources.requests.memory",
                    "Add resources.requests.memory (e.g., '128Mi')",
                )
            )

        if not limits.get("cpu"):
            self.violations.append(
                ValidationResult(
                    "RES-002",
                    "CRITICAL",
                    f"Container '{name}' missing CPU limit",
                    f"{filepath}:spec.template.spec.{path}.resources.limits.cpu",
                    "Add resources.limits.cpu (e.g., '500m')",
                )
            )

        if not limits.get("memory"):
            self.violations.append(
                ValidationResult(
                    "RES-004",
                    "CRITICAL",
                    f"Container '{name}' missing memory limit",
                    f"{filepath}:spec.template.spec.{path}.resources.limits.memory",
                    "Add resources.limits.memory (e.g., '256Mi')",
                )
            )

    def _validate_role(self, doc: Dict[str, Any], filepath: str):
        """Validate Role resources."""
        rules = doc.get("rules", [])
        for idx, rule in enumerate(rules):
            self._validate_rbac_rule(rule, filepath, f"Role.rules[{idx}]")

    def _validate_clusterrole(self, doc: Dict[str, Any], filepath: str):
        """Validate ClusterRole resources."""
        metadata = doc.get("metadata", {})
        name = metadata.get("name", "")

        # Warn about ClusterRole for application workloads
        if "cluster-admin" not in name:
            self.violations.append(
                ValidationResult(
                    "RBAC-002",
                    "WARNING",
                    "ClusterRole detected - prefer namespace-scoped Role",
                    f"{filepath}:kind",
                    "Use Role instead of ClusterRole unless cluster-wide access is required",
                )
            )

        rules = doc.get("rules", [])
        for idx, rule in enumerate(rules):
            self._validate_rbac_rule(rule, filepath, f"ClusterRole.rules[{idx}]")

    def _validate_rbac_rule(self, rule: Dict[str, Any], filepath: str, path: str):
        """Validate RBAC rule."""
        verbs = rule.get("verbs", [])
        resources = rule.get("resources", [])

        # Check for wildcard permissions
        if "*" in verbs or "*" in resources:
            self.violations.append(
                ValidationResult(
                    "RBAC-003",
                    "CRITICAL",
                    "Wildcard permissions (*) detected",
                    f"{filepath}:{path}",
                    "Specify explicit verbs and resources instead of wildcards",
                )
            )

        # Check for forbidden verbs
        forbidden_verbs = {"bind", "escalate", "impersonate"}
        if any(v in forbidden_verbs for v in verbs):
            self.violations.append(
                ValidationResult(
                    "RBAC-004",
                    "CRITICAL",
                    f"Forbidden verbs detected: {forbidden_verbs & set(verbs)}",
                    f"{filepath}:{path}.verbs",
                    "Remove bind/escalate/impersonate verbs",
                )
            )

    def _validate_rolebinding(self, doc: Dict[str, Any], filepath: str):
        """Validate RoleBinding resources."""
        role_ref = doc.get("roleRef", {})
        name = role_ref.get("name", "")

        if name == "cluster-admin":
            self.violations.append(
                ValidationResult(
                    "RBAC-005",
                    "CRITICAL",
                    "Binding to cluster-admin role",
                    f"{filepath}:roleRef.name",
                    "Never bind applications to cluster-admin - create specific roles",
                )
            )


def print_report(passed: bool, violations: List[ValidationResult], filepath: str):
    """Print validation report."""
    print(f"\n{'=' * 80}")
    print(f"Constitution Violation Report: {filepath}")
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
        print("✓ No violations found - manifest complies with constitution rules\n")

    status = "PASSED" if passed else "BLOCKED"
    print(f"### Status: {status}")
    print(f"{'=' * 80}\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_k8s.py <manifest-file>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not Path(filepath).exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    validator = K8sValidator()
    passed, violations = validator.validate_file(filepath)
    print_report(passed, violations, filepath)

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
