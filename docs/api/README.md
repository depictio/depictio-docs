---
title: "API"
icon: material/api
description: "Interact with Depictio programmatically using the REST API."
---

# API Documentation

Depictio provides a comprehensive REST API that allows you to interact with all aspects of the platform programmatically. This section provides an overview of the API and links to detailed documentation.

## Overview

The Depictio API enables you to:

- Manage projects and workflows
- Create and configure dashboards
- Upload and retrieve data
- Manage users and permissions

All API endpoints follow RESTful principles and use JWT authentication for security.

## API Structure & Endpoints

The Depictio API is organized around the following main resources:

- **Projects** - Manage top-level entities that encapsulate production-oriented pipelines/workflows
- **Workflows** - Interact with standardized production-oriented workflows
- **Run Configurations** - Define parameters and settings for workflow runs
- **Runs** - Manage instances of workflow executions
- **Files** - Access artifacts produced by workflow runs
- **Data Collections** - Work with aggregated data from files following the same structure
- **Dashboards** - Create and manage interactive visualization dashboards
- **Users** - Handle user authentication and authorization

## Authentication

All API requests require authentication using JWT (JSON Web Tokens). To authenticate:

1. Obtain a token by sending a POST request to the `/auth/login` endpoint with your credentials
2. Include the token in the `Authorization` header of subsequent requests using the format: `Bearer <token>`

## API Versioning

The Depictio API uses versioning to ensure backward compatibility. The current version is `v1`, which is reflected in the URL path:

```bash
https://your-depictio-instance.com/depictio/api/v1/...
```

## In This Section

<!-- - [API Overview](overview.md) - Detailed information about the API structure and authentication -->
<!-- - [Endpoints](endpoints.md) - Summary of available API endpoints and their functionality -->
- [API Reference](reference.md) - Interactive API documentation generated from the OpenAPI specification
<!-- - [Integration](api_docs_integration.md) - Guide for integrating with the Depictio API -->
- [FastAPI Docs](fastapi_docs.md) - Access to the auto-generated FastAPI documentation

<!-- ## Key Concepts

- **Authentication** - All requests require a JWT token obtained from the `/auth/token` endpoint
- **Versioning** - The API uses versioning (current: v1) to ensure backward compatibility
- **Resources** - The API is organized around resources like Projects, Workflows, and Dashboards
- **JSON Format** - All requests and responses use JSON format (except file uploads/downloads)

Explore the detailed documentation to learn how to leverage the Depictio API for your specific needs. -->
