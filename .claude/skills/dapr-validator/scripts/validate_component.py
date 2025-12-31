#!/usr/bin/env python3
"""
Dapr Component Validator
Validates Dapr component files against security and best practice rules.
"""

import re
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


class DaprComponentValidator:
    def __init__(self):
        self.violations: List[ValidationResult] = []

    def validate_file(self, filepath: str) -> Tuple[bool, List[ValidationResult]]:
        """Validate a Dapr component file."""
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
        """Validate a single Dapr document."""
        api_version = doc.get("apiVersion", "")
        kind = doc.get("kind", "")

        if "dapr.io" not in api_version:
            self.violations.append(
                ValidationResult(
                    "DAPR-008",
                    "CRITICAL",
                    "Not a valid Dapr component (missing dapr.io apiVersion)",
                    f"{filepath}:apiVersion",
                    "Set apiVersion: dapr.io/v1alpha1",
                )
            )
            return

        if kind == "Component":
            self._validate_component(doc, filepath)
        elif kind == "Configuration":
            self._validate_configuration(doc, filepath)
        elif kind == "Subscription":
            self._validate_subscription(doc, filepath)

    def _validate_component(self, doc: Dict[str, Any], filepath: str):
        """Validate Dapr Component resources."""
        metadata = doc.get("metadata", {})
        spec = doc.get("spec", {})

        # Check namespace
        namespace = metadata.get("namespace", "")
        if not namespace:
            self.violations.append(
                ValidationResult(
                    "DAPR-001",
                    "CRITICAL",
                    "Component missing namespace",
                    f"{filepath}:metadata.namespace",
                    "Add explicit namespace (never rely on default)",
                )
            )
        elif namespace == "default":
            self.violations.append(
                ValidationResult(
                    "DAPR-002",
                    "CRITICAL",
                    "Component uses 'default' namespace",
                    f"{filepath}:metadata.namespace",
                    "Use a specific namespace (e.g., 'todo-app')",
                )
            )

        # Check scopes
        scopes = spec.get("scopes", [])
        if not scopes:
            self.violations.append(
                ValidationResult(
                    "DAPR-004",
                    "CRITICAL",
                    "Component has no scopes defined",
                    f"{filepath}:spec.scopes",
                    "Add scopes to limit which apps can use this component",
                )
            )

        # Check metadata for inline credentials
        component_metadata = spec.get("metadata", [])
        self._check_credentials(component_metadata, filepath)

        # Component-specific validation
        component_type = spec.get("type", "")
        if "postgres" in component_type.lower() or "sql" in component_type.lower():
            self._validate_database_component(spec, filepath)
        elif "kafka" in component_type.lower():
            self._validate_kafka_component(spec, filepath)

    def _validate_configuration(self, doc: Dict[str, Any], filepath: str):
        """Validate Dapr Configuration resources."""
        spec = doc.get("spec", {})
        mtls = spec.get("mtls", {})

        if not mtls:
            self.violations.append(
                ValidationResult(
                    "DAPR-005",
                    "CRITICAL",
                    "Configuration missing mTLS settings",
                    f"{filepath}:spec.mtls",
                    "Add mtls.enabled: true to Configuration",
                )
            )
        elif not mtls.get("enabled", False):
            self.violations.append(
                ValidationResult(
                    "DAPR-005",
                    "CRITICAL",
                    "mTLS not enabled in Configuration",
                    f"{filepath}:spec.mtls.enabled",
                    "Set mtls.enabled: true",
                )
            )

    def _validate_subscription(self, doc: Dict[str, Any], filepath: str):
        """Validate Dapr Subscription resources."""
        spec = doc.get("spec", {})
        topic = spec.get("topic", "")

        # Validate topic naming convention
        if topic and not self._is_valid_topic_name(topic):
            self.violations.append(
                ValidationResult(
                    "KAFKA-001",
                    "WARNING",
                    f"Topic '{topic}' doesn't follow naming convention",
                    f"{filepath}:spec.topic",
                    "Use format: <domain>.<entity>.<event> (e.g., 'todo.task.created')",
                )
            )

    def _check_credentials(self, metadata: List[Dict[str, Any]], filepath: str):
        """Check for inline credentials in metadata."""
        sensitive_keys = [
            "password",
            "connectionstring",
            "apikey",
            "secret",
            "token",
            "key",
        ]

        for item in metadata:
            if not isinstance(item, dict):
                continue

            name = item.get("name", "").lower()
            value = item.get("value", "")
            secret_key_ref = item.get("secretKeyRef", {})

            # Check if sensitive key has inline value
            if any(sens in name for sens in sensitive_keys):
                if value and not secret_key_ref:
                    self.violations.append(
                        ValidationResult(
                            "DAPR-003",
                            "CRITICAL",
                            f"Inline credential detected: {item.get('name')}",
                            f"{filepath}:spec.metadata",
                            "Use secretKeyRef instead of inline values for credentials",
                        )
                    )
                elif not secret_key_ref:
                    self.violations.append(
                        ValidationResult(
                            "DAPR-003",
                            "WARNING",
                            f"Sensitive metadata '{item.get('name')}' should use secretKeyRef",
                            f"{filepath}:spec.metadata",
                            "Add secretKeyRef for credential references",
                        )
                    )

    def _validate_database_component(self, spec: Dict[str, Any], filepath: str):
        """Validate database-specific component settings."""
        metadata = spec.get("metadata", [])

        # Check for SSL/TLS
        has_ssl = False
        for item in metadata:
            if isinstance(item, dict):
                name = item.get("name", "").lower()
                if "ssl" in name or "tls" in name:
                    has_ssl = True
                    break

        if not has_ssl:
            self.violations.append(
                ValidationResult(
                    "DB-001",
                    "WARNING",
                    "Database component should use SSL/TLS",
                    f"{filepath}:spec.metadata",
                    "Add sslmode or SSL configuration to metadata",
                )
            )

    def _validate_kafka_component(self, spec: Dict[str, Any], filepath: str):
        """Validate Kafka-specific component settings."""
        metadata = spec.get("metadata", [])

        # Check for auth configuration
        has_auth = False
        for item in metadata:
            if isinstance(item, dict):
                name = item.get("name", "").lower()
                if "sasl" in name or "auth" in name:
                    has_auth = True
                    break

        if not has_auth:
            self.violations.append(
                ValidationResult(
                    "KAFKA-002",
                    "WARNING",
                    "Kafka component missing authentication configuration",
                    f"{filepath}:spec.metadata",
                    "Add SASL authentication for production Kafka",
                )
            )

    def _is_valid_topic_name(self, topic: str) -> bool:
        """Check if topic name follows convention: domain.entity.event"""
        pattern = r"^[a-z][a-z0-9-]*\.[a-z][a-z0-9-]*\.[a-z][a-z0-9-]*$"
        return bool(re.match(pattern, topic))


def print_report(passed: bool, violations: List[ValidationResult], filepath: str):
    """Print validation report."""
    print(f"\n{'=' * 80}")
    print(f"Dapr Component Validation Report: {filepath}")
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
        print("✓ No violations found - component complies with Dapr best practices\n")

    status = "PASSED" if passed else "BLOCKED"
    print(f"### Status: {status}")
    print(f"{'=' * 80}\n")
    print(f"{'=' * 80}\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_component.py <component-file.yaml>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not Path(filepath).exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    validator = DaprComponentValidator()
    passed, violations = validator.validate_file(filepath)
    print_report(passed, violations, filepath)

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
