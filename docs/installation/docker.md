# Docker Compose Installation

## :material-rocket-launch: Quick Start

**Prerequisites**: [Docker](https://docs.docker.com/get-docker/) 20.10+ and [Docker Compose](https://docs.docker.com/compose/install/) V2.

### Step 1 — Download the compose file

```bash
curl -LO https://raw.githubusercontent.com/depictio/depictio/main/docker-compose.yaml
```

### Step 2 — Set credentials

Generate strong passwords, then write your `.env`:

=== "bash / openssl"

    ```bash
    # Generate two passwords
    ADMIN_PWD=$(openssl rand -base64 24)
    MINIO_PWD=$(openssl rand -base64 24)

    cat > .env << EOF
    DEPICTIO_BOOTSTRAP_ADMIN_EMAIL=admin@example.com
    DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD=${ADMIN_PWD}
    DEPICTIO_MINIO_ROOT_PASSWORD=${MINIO_PWD}
    EOF

    echo "Admin password : ${ADMIN_PWD}"
    echo "MinIO password : ${MINIO_PWD}"
    ```

=== "Python"

    ```python
    import secrets, pathlib

    admin_pwd = secrets.token_urlsafe(24)
    minio_pwd = secrets.token_urlsafe(24)

    pathlib.Path(".env").write_text(
        f"DEPICTIO_BOOTSTRAP_ADMIN_EMAIL=admin@example.com\n"
        f"DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD={admin_pwd}\n"
        f"DEPICTIO_MINIO_ROOT_PASSWORD={minio_pwd}\n"
    )

    print(f"Admin password : {admin_pwd}")
    print(f"MinIO password : {minio_pwd}")
    ```

!!! warning "Required before first start"
    The server refuses to start if `DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD` or `DEPICTIO_MINIO_ROOT_PASSWORD` are absent or too short (< 16 chars).

!!! tip "Save your passwords"
    Note them down — the bootstrap is idempotent so the admin password cannot be recovered from the env var after first boot.

### Step 3 — Start

```bash
docker compose up -d
```

All services start automatically: MongoDB, Redis, MinIO, backend, viewer, and Celery worker.

### Step 4 — Open

| Service | URL | Credentials |
|---------|-----|-------------|
| Depictio | <http://localhost:5080> | _(single-user mode, no login)_ |
| API docs | <http://localhost:8058/docs> | — |
| MinIO console | <http://localhost:9001> | `minio` / your `.env` password |

!!! success "That's it!"
    Depictio starts in **single-user mode** by default — no login required to use the UI.

---

## :material-cog-outline: Advanced Configuration

Everything in this section is **optional**. The Quick Start defaults work for most users.

### Single-user vs Multi-user mode

Depictio ships in **single-user mode** by default: no login, no accounts, one admin user.

| Mode | `DEPICTIO_AUTH_SINGLE_USER_MODE` | `DEPICTIO_AUTH_PUBLIC_MODE` | Use case |
|------|----------------------------------|-----------------------------|---------:|
| **Single-user** _(default)_ | `true` | `false` | Local development, personal use |
| **Multi-user** | `false` | `false` | Team deployment with login |
| **Public (read-only)** | `false` | `true` | Shared dashboards, no auth required |

Switch to multi-user mode in your `.env`:

```bash
DEPICTIO_AUTH_SINGLE_USER_MODE=false
```

Users can then register accounts and log in via the Depictio UI.

!!! warning "Expose to the network?"
    If making Depictio accessible beyond `localhost`, disable single-user mode and change the MinIO credentials.

### Custom Credentials (.env file)

To change MinIO credentials or pin a specific version, copy the example file:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
# Application version (default: latest)
DEPICTIO_VERSION=latest

# Admin account — REQUIRED on first boot (all modes)
DEPICTIO_BOOTSTRAP_ADMIN_EMAIL=admin@example.com
DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD=change-me-strong-password-here

# MinIO credentials — REQUIRED, ≥16 chars (enforced at startup from v1.0.0-b1)
DEPICTIO_MINIO_ROOT_USER=myadmin
DEPICTIO_MINIO_ROOT_PASSWORD=change-me-strong-password-here
```

!!! info "Bootstrap is idempotent"
    The admin account is created only on first boot (when no non-anonymous admin exists in MongoDB). Restarting the container or changing the bootstrap vars afterwards has no effect — use the admin UI to manage credentials.

!!! tip "Full reference"
    - **Complete env file**: `.env.complete.example` — all 160+ variables with defaults
    - **Configuration Guide**: [Configuration](configuration.md) — common use cases
    - **Full Reference**: [Environment Reference](env-reference.md) — all variables

### External S3 / Bring Your Own MinIO

If you already have a MinIO server or S3-compatible storage, use the dedicated no-minio compose file:

```bash
docker compose -f docker-compose/docker-compose.no-minio.yaml up -d
```

Configure your `.env` to point to your existing instance:

```bash
DEPICTIO_MINIO_ROOT_USER=your-access-key
DEPICTIO_MINIO_ROOT_PASSWORD=your-secret-key
DEPICTIO_MINIO_PUBLIC_URL=https://your-minio-host.example.com
DEPICTIO_MINIO_EXTERNAL_SERVICE=true
# Optional overrides
DEPICTIO_MINIO_EXTERNAL_HOST=your-minio-host.example.com
DEPICTIO_MINIO_EXTERNAL_PORT=9000
DEPICTIO_MINIO_EXTERNAL_PROTOCOL=https
```

!!! note "Network Configuration"
    Set `DEPICTIO_MINIO_EXTERNAL_SERVICE=true` when MinIO is outside the Docker Compose network.

!!! info "S3-Compatible Storage"
    Depictio uses the MinIO client library (S3 API compatible). AWS S3, DigitalOcean Spaces, Backblaze B2, and others may work but have not been officially tested.

### Port Configuration

Override default ports in `.env`:

```bash
MINIO_PORT=9000
MINIO_CONSOLE_PORT=9001
```

All default ports:

| Service | Default port |
|---------|-------------|
| Frontend (React viewer) | 5080 |
| Backend API | 8058 |
| MongoDB | 27018 |
| MinIO API | 9000 |
| MinIO UI | 9001 |

### Development Mode

Enable debug logging and hot-reload:

```bash
DEPICTIO_DEV_MODE=true docker compose up -d
```

Or set `DEPICTIO_DEV_MODE=true` in your `.env` file.

### Background Callbacks (Celery)

Depictio uses Celery for asynchronous processing. The `depictio-celery-worker` container always starts automatically — it is **required** for the dashboard editor (design mode).

```bash
# Configure view-mode behaviour in .env
DEPICTIO_CELERY_ENABLED=true   # false = synchronous view mode (simpler for debugging)
```

| Mode | `DEPICTIO_CELERY_ENABLED` | Behaviour |
|------|--------------------------|-----------|
| Design mode (editor) | always on | Non-blocking figure preview — required |
| View mode | `true` | Async data loading — recommended for production |
| View mode | `false` | Synchronous — simpler for development |

!!! info "Kubernetes/Helm"
    Background callbacks are also supported in Kubernetes via the Helm chart (`celery.enabled: true` by default). See the [Kubernetes installation guide](kubernetes/).

---

## :material-wrench: Managing Services

| Action | Command |
|--------|---------|
| Stop (preserve data) | `docker compose stop` |
| Stop and remove containers | `docker compose down` |
| Stop, remove containers **and data** | `docker compose down -v` |
| View all logs | `docker compose logs -f` |
| View one service | `docker compose logs -f depictio-backend` |
| Check status | `docker compose ps` |

---

## :material-bug: Troubleshooting

### A container fails to start

```bash
docker compose logs <service_name>
```

Common causes: port conflict, volume permission error, MongoDB connection failure.

### Cannot connect to services

1. Check containers are running: `docker compose ps`
2. Confirm you are using the correct ports
3. Check for firewall rules blocking the connection

### Data persistence

MongoDB data is stored in `./depictioDB` (bind-mount). MinIO data is stored in a named Docker volume (`minio_data`). Both persist across `docker compose down` restarts.

---

## Next Steps

- [Get started with Depictio](../usage/get_started.md)
- [Create your first dashboard](../usage/guides/dashboard_creation.md)
- [Ingest data with the CLI](../depictio-cli/usage.md)
