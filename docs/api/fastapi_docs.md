# FastAPI Documentation

Depictio uses FastAPI for its backend, which provides automatic, interactive API documentation. This page explains how to access and use this documentation.

## Accessing the API Documentation

FastAPI automatically generates two types of interactive documentation:

1. **Swagger UI** - Available at `/docs`
2. **ReDoc** - Available at `/redoc`

To access these, simply append these paths to your Depictio API base URL:

- Swagger UI: `http://<your-depictio-host>:8058/docs`
- ReDoc: `http://<your-depictio-host>:8058/redoc`
<!--

## Using Swagger UI

Swagger UI provides an interactive interface where you can:

1. **Browse Endpoints**: See all available API endpoints organized by tags
2. **Read Documentation**: View detailed descriptions, parameters, and response schemas
3. **Try Endpoints**: Execute API calls directly from the browser
4. **Authenticate**: Use the "Authorize" button to add your JWT token

### Authentication in Swagger UI

To authenticate in Swagger UI:

1. Click the "Authorize" button at the top right
2. Enter your JWT token in the format: `Bearer <your-token>`
3. Click "Authorize" and close the dialog
4. Now you can make authenticated API requests

## Using ReDoc

ReDoc provides a more readable, documentation-focused interface:

1. **Clean Layout**: Well-organized, easy-to-read documentation
2. **Search Functionality**: Quickly find endpoints or models
3. **Request/Response Examples**: See example payloads for each endpoint
4. **Schema References**: Detailed information about data models

## API Models

The documentation includes detailed schemas for all data models used in the API, including:

- User models
- Project models
- Workflow models
- File models
- Dashboard models

## Integrating with MkDocs

For a seamless documentation experience, you can integrate the FastAPI OpenAPI specification with MkDocs using the `mkdocs-swagger-ui-tag` plugin. This allows you to embed the Swagger UI directly in your MkDocs documentation.

### Installation

```bash
pip install mkdocs-swagger-ui-tag
```

### Configuration

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - swagger-ui-tag
```

### Usage

You can then embed the Swagger UI in any Markdown page using:

```markdown
<swagger-ui url="http://<your-depictio-host>:8058/openapi.json"/>
```

## Exporting OpenAPI Specification

You can download the complete OpenAPI specification in JSON format from:

```
http://<your-depictio-host>:8058/openapi.json
```

This file can be used with various API tools and generators. -->
