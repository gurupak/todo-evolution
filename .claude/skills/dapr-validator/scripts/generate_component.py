#!/usr/bin/env python3
"""
Dapr Component Generator
Generates Dapr component manifests from templates.
"""

import argparse
import sys
from pathlib import Path

COMPONENT_TYPES = {
    "statestore-postgres": {
        "template": "statestore-postgres.yaml",
        "description": "PostgreSQL state store",
        "default_secret": "postgres-secrets",
    },
    "statestore-redis": {
        "template": "statestore-redis.yaml",
        "description": "Redis state store",
        "default_secret": "redis-secrets",
        "requires": ["REDIS_HOST"],
    },
    "pubsub-kafka": {
        "template": "pubsub-kafka.yaml",
        "description": "Kafka pub/sub",
        "default_secret": "kafka-secrets",
        "requires": ["KAFKA_BROKERS"],
    },
    "pubsub-redis": {
        "template": "pubsub-redis.yaml",
        "description": "Redis pub/sub",
        "default_secret": "redis-secrets",
        "requires": ["REDIS_HOST"],
    },
    "configuration": {
        "template": "configuration.yaml",
        "description": "Dapr Configuration with mTLS",
    },
}


def replace_placeholders(content: str, replacements: dict) -> str:
    """Replace all placeholders in content with actual values."""
    for key, value in replacements.items():
        # Handle both {{PLACEHOLDER}} and { { PLACEHOLDER } } formats
        content = content.replace("{{" + key + "}}", str(value))
        content = content.replace("{ { " + key + " } }", str(value))
    return content


def generate_component(
    component_type: str,
    name: str,
    namespace: str,
    app_id: str = None,
    secret_name: str = None,
    output_file: str = None,
    **kwargs,
):
    """Generate a Dapr component from a template."""

    if component_type not in COMPONENT_TYPES:
        print(f"Error: Unknown component type '{component_type}'")
        print(f"Available types: {', '.join(COMPONENT_TYPES.keys())}")
        return False

    config = COMPONENT_TYPES[component_type]

    # Check required parameters
    required = config.get("requires", [])
    for req in required:
        if req not in kwargs or not kwargs[req]:
            print(
                f"Error: Missing required parameter for {component_type}: --{req.lower().replace('_', '-')}"
            )
            return False

    # Determine paths
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    template_path = skill_dir / "assets" / config["template"]

    if not template_path.exists():
        print(f"Error: Template not found: {template_path}")
        return False

    # Read template
    try:
        content = template_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading template: {e}")
        return False

    # Prepare replacements
    replacements = {
        "COMPONENT_NAME": name,
        "NAMESPACE": namespace,
        "APP_ID": app_id or name,
        "SECRET_NAME": secret_name or config.get("default_secret", f"{name}-secrets"),
    }

    # Add additional parameters
    for key, value in kwargs.items():
        if value:
            replacements[key] = value

    # Replace placeholders
    output_content = replace_placeholders(content, replacements)

    # Determine output file
    if not output_file:
        output_file = f"{name}.yaml"

    output_path = Path(output_file)

    # Write output
    try:
        output_path.write_text(output_content, encoding="utf-8")
    except Exception as e:
        print(f"Error writing output file: {e}")
        return False

    print(f"\n✓ Dapr component generated successfully: {output_path}")
    print(f"  Type: {config['description']}")
    print(f"  Name: {name}")
    print(f"  Namespace: {namespace}")
    print(f"\nNext steps:")
    print(f"1. Review and customize: {output_path}")
    print(
        f"2. Create Kubernetes Secret: kubectl create secret generic {replacements['SECRET_NAME']} -n {namespace}"
    )
    print(f"3. Validate: python scripts/validate_component.py {output_path}")
    print(f"4. Apply: kubectl apply -f {output_path}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate Dapr component manifests from templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate PostgreSQL state store
  python generate_component.py --type statestore-postgres --name mystore --namespace todo-app --app-id todo-backend

  # Generate Kafka pub/sub
  python generate_component.py --type pubsub-kafka --name mypubsub --namespace todo-app --app-id todo-backend --kafka-brokers kafka:9092

  # Generate Redis state store
  python generate_component.py --type statestore-redis --name mystore --namespace todo-app --app-id todo-backend --redis-host redis-master

  # Generate Dapr configuration
  python generate_component.py --type configuration --name dapr-config --namespace todo-app --output config.yaml
        """,
    )

    parser.add_argument(
        "--type",
        required=True,
        choices=list(COMPONENT_TYPES.keys()),
        help="Component type",
    )

    parser.add_argument("--name", required=True, help="Component name")

    parser.add_argument("--namespace", required=True, help="Kubernetes namespace")

    parser.add_argument(
        "--app-id", help="Dapr app ID for scopes (defaults to component name)"
    )

    parser.add_argument(
        "--secret-name",
        help="Kubernetes Secret name (defaults based on component type)",
    )

    parser.add_argument(
        "--redis-host", help="Redis host (required for Redis components)"
    )

    parser.add_argument(
        "--kafka-brokers", help="Kafka broker addresses (required for Kafka components)"
    )

    parser.add_argument("--output", help="Output file path (default: <name>.yaml)")

    args = parser.parse_args()

    # Generate the component
    success = generate_component(
        component_type=args.type,
        name=args.name,
        namespace=args.namespace,
        app_id=args.app_id,
        secret_name=args.secret_name,
        output_file=args.output,
        REDIS_HOST=args.redis_host,
        KAFKA_BROKERS=args.kafka_brokers,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
