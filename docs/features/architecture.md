# Architecture

Depictio is built on a modern microservices architecture that provides flexibility, scalability, and maintainability. This page describes the overall architecture and how the different components interact.

<p align="center">
  <img src="../../images/modularity/main.png" alt="Depictio architecture" width=800>
</p>

## Microservices Overview

Depictio's architecture consists of four main components:

1. **FastAPI Backend** - RESTful API service that handles metadata processing, authentication, and business logic
2. **MongoDB Database** - Document database for storing metadata, user information, and dashboard configurations
3. **MinIO S3 Storage** - Object storage for managing data files and assets
4. **Plotly Dash Frontend** - Interactive web interface for creating and using dashboards

### FastAPI Backend

The backend service is built with FastAPI, a modern, high-performance web framework for building APIs with Python. Key features include:

- RESTful API endpoints for all platform functionality
- JWT-based authentication and authorization
- Asynchronous request handling for improved performance
- Pydantic models for data validation and serialization
- Beanie ODM for MongoDB integration

### MongoDB Database

MongoDB serves as the primary database for Depictio, storing:

- User accounts and authentication information
- Project metadata and configurations
- Workflow definitions and run information
- Dashboard layouts, structure and content
- Data collection metadata

### MinIO S3 Storage (Optional)

MinIO provides S3-compatible object storage for:

- Processed data ready for visualization (Delta lake, genome-browser compatible data, etc.)

### Plotly Dash Frontend

The frontend is built with Plotly Dash (React), a framework for building analytical web applications. Features include:

- Interactive data visualization components
- Real-time data updates
- Draggagle and customizable dashboard layouts
- Integration with the backend API for data retrieval and processing

## Security

Depictio implements several security measures:

- JWT-based authentication for API access
- Role-based access control for resources (owner, editor, viewer)
- Secure communication between services
- Data encryption for sensitive information (e.g., passwords)
