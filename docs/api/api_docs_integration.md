# API Documentation Integration

This page explains how to integrate the Depictio API documentation with MkDocs using the OpenAPI specification.

## Automated OpenAPI Specification Export

Depictio includes a script to automatically export the OpenAPI specification from a running API instance. This ensures that your documentation always reflects the latest API changes.

### Using the Script

The script is located at `update_openapi.py` in the documentation root directory. To use it:

1. Make sure your Depictio API is running (typically at <http://localhost:8058>)
2. Run the script:

```bash
# From the depictio-docs directory
python update_openapi.py
```

This will fetch the OpenAPI specification and save it to `docs/api/openapi.json`.

### Script Options

The script supports several command-line options:

```bash
python update_openapi.py --help
```

- `--api-url`: Base URL of the API (default: <http://localhost:8058>)
- `--output`: Path where the OpenAPI JSON file should be saved (default: docs/api/openapi.json)
- `--indent`: JSON indentation level (default: 2)

### Integration with Documentation Build

You can integrate this script into your documentation build process by adding it to your build scripts or CI/CD pipeline. For example:

```bash
# Start the API server
docker-compose up -d depictio-backend

# Wait for the API to be ready
sleep 10

# Fetch the OpenAPI specification
python update_openapi.py

# Build the documentation
mkdocs build
```

## Displaying API Documentation in MkDocs

Once you have the OpenAPI specification, you can display it in your MkDocs site using the `swagger-ui-tag` plugin.

### Basic Usage

To display the API documentation on a page, add the following to your Markdown:

```markdown
<swagger-ui url="../../api/openapi.json"/>
```

The path should be relative to the current Markdown file.

### Customization Options

You can customize the Swagger UI display with additional options:

```markdown
<swagger-ui
  url="../../api/openapi.json"
  expand="all"
  theme="dark"
/>
```

Available options include:

- `expand`: Controls the default expansion setting for operations and tags. Values are "list" (default), "full", "none", or "all".
- `theme`: The theme to use. Values are "light" (default) or "dark".
- `try-it-out-enabled`: Whether to show the "Try it out" section. Values are "true" or "false".

## Example: Full API Documentation Page

Here's an example of a complete API documentation page:

```markdown
# API Reference

This page provides interactive documentation for the Depictio API.

## Authentication

To use the API, you need to authenticate using JWT tokens. See the [Authentication](#/components/securitySchemes/bearerAuth) section for details.

## Endpoints

<swagger-ui url="../../api/openapi.json"/>
```

## Fallback for Static Documentation

If you want to provide API documentation even when the OpenAPI specification hasn't been generated (e.g., for GitHub Pages), you can include a simplified static version:

```markdown
<swagger-ui url="../../api/openapi.json" fallback="true"/>
```

With the `fallback` option, if the OpenAPI specification file is not found, a message will be displayed instead of an error.

## Troubleshooting

### OpenAPI Specification Not Found

If you see an error about the OpenAPI specification not being found:

1. Make sure you've run the `update_openapi.py` script
2. Check that the path in the `url` attribute is correct relative to the current Markdown file
3. Verify that the file exists in the expected location

### Swagger UI Not Displaying

If the Swagger UI component is not displaying:

1. Make sure the `swagger-ui-tag` plugin is installed and enabled in your `mkdocs.yml`
2. Check for JavaScript errors in your browser's developer console
3. Try using a different browser
