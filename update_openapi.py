#!/usr/bin/env python3
"""
Script to automatically fetch the OpenAPI specification from a running Depictio API instance
and save it to the documentation directory.

This script can be run manually or integrated into the documentation build process.
"""

import argparse
import json
import os
import sys
from urllib.error import URLError
from urllib.request import urlopen


def fetch_openapi_spec(api_url, output_path, indent=2):
    """
    Fetch the OpenAPI specification from a running API instance and save it to a file.

    Args:
        api_url: Base URL of the API (e.g., http://localhost:8058)
        output_path: Path where the OpenAPI JSON file should be saved
        indent: JSON indentation level for pretty printing

    Returns:
        bool: True if successful, False otherwise
    """
    openapi_url = f"{api_url.rstrip('/')}/openapi.json"

    print(f"Fetching OpenAPI specification from {openapi_url}...")

    try:
        with urlopen(openapi_url) as response:
            spec = json.loads(response.read().decode('utf-8'))

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Write the specification to the output file
        with open(output_path, 'w') as f:
            json.dump(spec, f, indent=indent)

        print(f"OpenAPI specification saved to {output_path}")
        return True

    except URLError as e:
        print(f"Error: Could not connect to the API at {api_url}")
        print(f"  {e}")
        return False

    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Fetch OpenAPI specification from a running Depictio API instance"
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:8058",
        help="Base URL of the API (default: http://localhost:8058)"
    )
    parser.add_argument(
        "--output",
        default="docs/api/openapi.json",
        help="Path where the OpenAPI JSON file should be saved (default: docs/api/openapi.json)"
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation level (default: 2)"
    )

    args = parser.parse_args()

    success = fetch_openapi_spec(args.api_url, args.output, args.indent)

    if not success:
        print("\nFailed to fetch OpenAPI specification.")
        print("Make sure the Depictio API is running and accessible at the specified URL.")
        sys.exit(1)


if __name__ == "__main__":
    main()
