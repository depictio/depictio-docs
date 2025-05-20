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

Create a `.env` file in the root directory of the project. You can use the provided example as a starting point:

```bash
cp .env.example .env
```

Edit the `.env` file to customize your configuration if needed. The default values should work for most users.

### 3. Start the Services

Start all Depictio services using Docker Compose:

```bash
docker-compose -f docker-compose.yaml -f docker-compose/docker-compose.minio.yaml up -d
```

This command will:

- Pull the necessary Docker images (latest by default, can be changed in the `.env` file)
- Create and start containers for MongoDB, the Depictio backend & frontend, and MinIO
- Set up the required network connections between services

!!!**Note**: If you wish to use your own MinIO instance, you can skip the `docker-compose/docker-compose.minio.yaml` file. In this case, make sure to set the `MINIO_` variables accordingly in your `.env` file to point to your MinIO instance.

### 4. Verify the Installation

After starting the services, you can verify that everything is running correctly:

```bash
docker-compose ps
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
docker-compose stop
```

### Stopping and Removing Containers

To stop all services and remove the containers:

```bash
docker-compose down
```

### Stopping and Removing Everything

To stop all services, remove the containers, and delete all data:

```bash
docker-compose down -v
```

**Warning**: This will delete all data stored in MongoDB and MinIO.

### Viewing Logs

To view the logs from all services:

```bash
docker-compose logs
```

To view logs from a specific service:

```bash
docker-compose logs depictio-backend
```

To follow the logs in real-time:

```bash
docker-compose logs -f
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

To run Depictio using Flask/Dash/gunicorn and FastAPI/uvicorn debug mode, which enables additional debugging features:

```bash
DEV_MODE=true docker-compose up -d
```

## Troubleshooting

### Container Fails to Start

If a container fails to start, check the logs:

```bash
docker-compose logs <service_name>
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
