#!/usr/bin/env python3
"""
Helm Chart Generator Script
Generates Helm charts from component-specific templates with constitution-compliant defaults.
"""

import argparse
import shutil
import sys
from pathlib import Path

COMPONENT_TYPES = {
    "frontend": {
        "port": 3000,
        "cpu_request": "100m",
        "cpu_limit": "500m",
        "memory_request": "128Mi",
        "memory_limit": "256Mi",
        "description": "Frontend application",
    },
    "backend": {
        "port": 8000,
        "cpu_request": "200m",
        "cpu_limit": "1000m",
        "memory_request": "256Mi",
        "memory_limit": "512Mi",
        "description": "Backend API service",
    },
    "mcp": {
        "port": 8080,
        "cpu_request": "100m",
        "cpu_limit": "500m",
        "memory_request": "128Mi",
        "memory_limit": "256Mi",
        "description": "MCP server",
    },
}


def replace_placeholders(content: str, replacements: dict) -> str:
    """Replace all placeholders in content with actual values."""
    for key, value in replacements.items():
        # Handle both {{PLACEHOLDER}} and { { PLACEHOLDER } } formats
        content = content.replace("{{" + key + "}}", str(value))
        content = content.replace("{ { " + key + " } }", str(value))
    return content


def generate_chart(
    name: str,
    component_type: str,
    namespace: str,
    output_dir: str,
    image_repo: str = None,
):
    """Generate a Helm chart from a component-specific template."""

    if component_type not in COMPONENT_TYPES:
        print(f"Error: Unknown component type '{component_type}'")
        print(f"Available types: {', '.join(COMPONENT_TYPES.keys())}")
        return False

    # Get component configuration
    config = COMPONENT_TYPES[component_type]

    # Determine paths
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    template_dir = skill_dir / "assets" / f"{component_type}-chart"

    if not template_dir.exists():
        print(f"Error: Template directory not found: {template_dir}")
        return False

    output_path = Path(output_dir) / name

    if output_path.exists():
        print(f"Error: Output directory already exists: {output_path}")
        return False

    print(f"Generating {component_type} Helm chart: {name}")
    print(f"Template: {template_dir}")
    print(f"Output: {output_path}")

    # Copy template directory
    try:
        shutil.copytree(template_dir, output_path)
    except Exception as e:
        print(f"Error copying template: {e}")
        return False

    # Prepare replacements
    replacements = {
        "CHART_NAME": name,
        "APP_NAME": name,
        "DESCRIPTION": config["description"],
        "IMAGE_REPOSITORY": image_repo or name,
        "SERVICE_PORT": config["port"],
        "CPU_REQUEST": config["cpu_request"],
        "CPU_LIMIT": config["cpu_limit"],
        "MEMORY_REQUEST": config["memory_request"],
        "MEMORY_LIMIT": config["memory_limit"],
        "PRODUCTION_HOST": f"{name}.example.com",
    }

    # Process all files in the generated chart
    for file_path in output_path.rglob("*"):
        if file_path.is_file():
            try:
                content = file_path.read_text(encoding="utf-8")
                updated_content = replace_placeholders(content, replacements)
                file_path.write_text(updated_content, encoding="utf-8")
            except Exception as e:
                print(f"Warning: Could not process {file_path}: {e}")

    print(f"\n✓ Chart generated successfully: {output_path}")
    print(f"\nNext steps:")
    print(f"1. Review and customize: {output_path}/values.yaml")
    print(f"2. Validate chart: helm lint {output_path}")
    print(
        f"3. Test template: helm template {name} {output_path} -f {output_path}/values-dev.yaml"
    )
    print(
        f"4. Install: helm install {name} {output_path} -f {output_path}/values-dev.yaml -n {namespace}"
    )

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate production-ready Helm charts from templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a frontend chart
  python generate_chart.py --name todo-frontend --type frontend --namespace todo-app

  # Generate a backend chart with custom image repository
  python generate_chart.py --name todo-backend --type backend --namespace todo-app --image myregistry/todo-backend

  # Generate an MCP server chart
  python generate_chart.py --name todo-mcp --type mcp --namespace todo-app --output ./charts
        """,
    )

    parser.add_argument(
        "--name", required=True, help="Chart name (e.g., todo-frontend)"
    )

    parser.add_argument(
        "--type",
        required=True,
        choices=list(COMPONENT_TYPES.keys()),
        help="Component type",
    )

    parser.add_argument("--namespace", required=True, help="Kubernetes namespace")

    parser.add_argument("--image", help="Image repository (defaults to chart name)")

    parser.add_argument(
        "--output", default="./charts", help="Output directory (default: ./charts)"
    )

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    Path(args.output).mkdir(parents=True, exist_ok=True)

    # Generate the chart
    success = generate_chart(
        name=args.name,
        component_type=args.type,
        namespace=args.namespace,
        output_dir=args.output,
        image_repo=args.image,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
