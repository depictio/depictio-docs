# Docker Compose Installation

This guide will walk you through installing and running Depictio using Docker Compose, which is the simplest way to get started with Depictio.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/) (version 20.10.0 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0.0 or higher)
- Git (optional, for cloning the repository)

## Installation Steps

### 1. Clone the Repository (Optional)

If you want to use the latest development version, you can clone the repository:

```bash
git clone https://github.com/depictio/depictio.git
cd depictio
```

Alternatively, you can download a release version from the [GitHub releases page](https://github.com/depictio/depictio/releases).

### 2. Configure Environment Variables

Create a `.env` file in the root directory of the project:

```bash
cp .env.example .env
```

The minimal configuration only requires MinIO credentials:

```bash
# .env - Minimal required configuration
DEPICTIO_MINIO_ROOT_USER=minio
DEPICTIO_MINIO_ROOT_PASSWORD=minio123
```

The default values work for most users. For advanced configuration:

- **Complete env file**: `.env.complete.example` - All 160+ variables with defaults (copy and uncomment as needed)
- **Configuration Guide**: [Configuration](configuration.md) - Common use cases and setup guides
- **Complete Reference**: [Environment Reference](env-reference.md) - Searchable documentation for all variables

### 3. Start the Services (including MinIO)

Start all Depictio services using Docker Compose:

```bash
docker compose -f docker-compose.yaml \
               -f docker-compose/docker-compose.minio.yaml \
               up -d
```

This command will:

- Pull the necessary Docker images (latest by default, can be changed in the `.env` file)
- Create and start containers for MongoDB, the Depictio backend & frontend, and MinIO
- Set up the required network connections between services


### Using an Existing MinIO Instance

If you already have a MinIO server running, you can skip the bundled MinIO container and configure Depictio to connect to your existing instance.

**Skip the bundled MinIO container:**

```bash
# Start without the MinIO compose file
docker compose -f docker-compose.yaml up -d
```

**Configure your `.env` file to point to your existing MinIO:**

```bash
# Connect to an existing MinIO server
DEPICTIO_MINIO_SERVICE_NAME=your-minio-host.example.com
DEPICTIO_MINIO_SERVICE_PORT=9000
DEPICTIO_MINIO_EXTERNAL_HOST=your-minio-host.example.com
DEPICTIO_MINIO_EXTERNAL_PORT=9000
DEPICTIO_MINIO_ROOT_USER=your-access-key
DEPICTIO_MINIO_ROOT_PASSWORD=your-secret-key
DEPICTIO_MINIO_BUCKET=depictio-bucket

# Set to true if MinIO is outside Docker network
DEPICTIO_MINIO_EXTERNAL_SERVICE=true

# Use https if your MinIO uses TLS
DEPICTIO_MINIO_EXTERNAL_PROTOCOL=https
```

!!! tip "Bucket Creation"

    Depictio will automatically create the bucket specified in `DEPICTIO_MINIO_BUCKET` if it doesn't exist, provided the credentials have sufficient permissions.

!!! note "Network Configuration"

    Set `DEPICTIO_MINIO_EXTERNAL_SERVICE=true` when your MinIO server is not part of the Docker Compose network. This tells Depictio to use the external host/port for connections instead of Docker's internal service discovery.

!!! info "S3-Compatible Storage"

    Depictio uses the MinIO client library which implements the S3 API. Other S3-compatible services (AWS S3, DigitalOcean Spaces, Backblaze B2, etc.) may work but have not been tested. If you try these configurations, please share your feedback!

### 4. Verify the Installation

After starting the services, you can verify that everything is running correctly:

```bash
docker compose ps
```

You should see all services in the "Up" state.

## Accessing Depictio

Once the services are running, you can access:

- **Frontend (Dash)**: <http://localhost:5080>
- **Backend API**: <http://localhost:8058>
- **API Documentation**: <http://localhost:8058/docs>
- **Minio UI**: <http://localhost:9001>

Default credentials are:

- **Depictio Admin credentials**: login: `admin@example.com` / password: `changeme`
- **MinIO credentials**: login: `minio` / password: `minio123`

## Managing the Services

### Stopping the Services

To stop all services while preserving data:

```bash
docker compose stop
```

### Stopping and Removing Containers

To stop all services and remove the containers:

```bash
docker compose down
```

### Stopping and Removing Everything

To stop all services, remove the containers, and delete all data:

```bash
docker compose down -v
```

**Warning**: This will delete all data stored in MongoDB and MinIO.

### Viewing Logs

To view the logs from all services:

```bash
docker compose logs
```

To view logs from a specific service:

```bash
docker compose logs depictio-backend
```

To follow the logs in real-time:

```bash
docker compose logs -f
```

## Configuration Options

### Ports

By default, Depictio uses the following ports:

- **5080**: Frontend (Dash)
- **8058**: Backend API
- **27018**: MongoDB
- **9000**: MinIO API
- **9001**: MinIO UI

If you need to change these ports, edit the `.env` file.

### Development Mode

To run Depictio using Flask/Dash/gunicorn and FastAPI/uvicorn debug mode, which enables additional debugging features, modify the `.env` file:

```env
DEV_MODE=true
```

and then start the services:

```bash
docker compose up -d
```

Or:

```bash
DEV_MODE=true docker compose up -d
```

### Background Callbacks with Celery

Depictio uses Celery for asynchronous background processing. **Celery is required** for the dashboard editor (design mode) to function properly, as it enables non-blocking figure preview rendering during component creation.

#### Architecture

The Celery worker container (`depictio-celery-worker`) is always started with docker-compose:

- **Design Mode** (Dashboard Editor): Always requires Celery for responsive figure preview
- **View Mode** (Dashboard Viewing): Optionally uses Celery based on configuration
- Redis is used as the message broker for task queuing

#### Configuration

Configure background callback behavior in your `.env` file:

```env
# REQUIRED: Set to true for design mode to work
# Also enables background callbacks for view mode (optional)
DEPICTIO_CELERY_ENABLED=true

# Configure number of Celery workers (default: 2)
DEPICTIO_CELERY_WORKERS=4
```

#### How It Works

**Design Mode (Dashboard Editor)**:

- Always uses background callbacks (not configurable)
- The Celery worker processes figure preview rendering
- UI remains responsive during component creation
- Required for the stepper workflow to function

**View Mode (Dashboard Viewing)**:

- When `DEPICTIO_CELERY_ENABLED=true`: Data loading executes asynchronously
- When `false`: Data loading runs synchronously (design mode still requires Celery)
- Background processing applies to:
  - Card components (initial render and filter updates)
  - Figure components (visualization rendering and filter updates)
  - Table components (data loading and pagination)

#### Performance Impact

**Design Mode**:

- Always asynchronous (required)
- UI never blocks during figure preview generation
- Essential for responsive dashboard building

**View Mode with Background Callbacks** (`DEPICTIO_CELERY_ENABLED=true`):

- UI remains responsive during data operations
- Operations execute in parallel
- Recommended for production, large datasets, multiple concurrent users

**View Mode Synchronous** (`DEPICTIO_CELERY_ENABLED=false`):

- Only view mode runs synchronously
- Design mode still uses Celery (required)
- UI may block during long data operations
- Simpler for debugging view mode issues

#### Service Management

The Celery worker is always running:

```bash
# Start all services (Celery worker included by default)
docker compose up -d

# Check Celery worker status
docker compose logs depictio-celery-worker

# The worker is always running - no need for conditional startup
```

#### Compatibility Notes


!!! info "Kubernetes/Helm Support"

    Background callbacks are currently only supported in Docker Compose deployments. Kubernetes/Helm support is **coming soon** in an upcoming release.


## Troubleshooting

### Container Fails to Start

If a container fails to start, check the logs:

```bash
docker compose logs <service_name>
```

Common issues include:

- Port conflicts (another application is using the same port)
- Insufficient permissions for mounted volumes
- MongoDB connection issues

### Cannot Connect to Services

If you cannot connect to the services, check:

1. That the containers are running: `docker-compose ps`
2. That you're using the correct ports
3. That there are no firewall rules blocking the connections

### Data Persistence Issues

By default, MongoDB data is stored in the `./depictioDB` directory. Make sure this directory has the correct permissions.

## Next Steps

Now that you have Depictio running, you can:

- [Get started with using Depictio](../usage/get_started.md)
- [Learn how to create dashboards](../usage/guides/dashboard_creation.md)
- [Configure the CLI for data ingestion](../depictio-cli/usage.md)
