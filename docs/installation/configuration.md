---
title: "Configuration"
icon: material/cog
description: "Configure Depictio with environment variables for various features and integrations."
---

# Configuration Guide

Depictio uses environment variables to configure various aspects of the application. This guide covers common configuration scenarios and use cases.

!!! tip "Complete Reference"

    For the complete list of all 160+ environment variables, see the [Environment Reference](env-reference.md) or use the `.env.complete.example` file in the repository.

## Configuration Files

The repository includes two environment file templates:

| File | Purpose |
|------|---------|
| `.env.example` | **Quick start** - Minimal configuration (just MinIO credentials) |
| `.env.complete.example` | **Complete reference** - All 160+ variables with defaults and comments |

## Quick Start Configuration

For most users, the minimal configuration is sufficient:

```bash
cp .env.example .env
```

**Minimal `.env` file:**

```bash
DEPICTIO_MINIO_ROOT_USER=minio
DEPICTIO_MINIO_ROOT_PASSWORD=minio123
```

## Advanced Configuration

For full control, use the complete configuration file:

```bash
cp .env.complete.example .env
# Then uncomment and modify the variables you need
```

All other settings use sensible defaults. The sections below cover common customization scenarios.

## Storage Configuration

Depictio can use MinIO for object storage. You can either use an external MinIO service or the built-in one.

### External MinIO Service

If you have an external MinIO service, configure it as follows:

For Docker Compose, add the following to your `.env` file:

```bash
# External MinIO service configuration
DEPICTIO_MINIO_PUBLIC_URL=http://minio.example.com
DEPICTIO_MINIO_ROOT_USER=minioadmin
DEPICTIO_MINIO_ROOT_PASSWORD=minioadmin123
DEPICTIO_MINIO_BUCKET_NAME=your-bucket-name
DEPICTIO_MINIO_EXTERNAL_SERVICE=true
```

For Kubernetes, you can set these values in your custom `values.yaml` file:

```yaml
minio:
  enabled: false  # Set to true if using built-in MinIO
  env:
    DEPICTIO_MINIO_PUBLIC_URL: "http://minio.example.com"
    DEPICTIO_MINIO_ROOT_USER: "minioadmin"
    DEPICTIO_MINIO_ROOT_PASSWORD: "minioadmin123"
    DEPICTIO_MINIO_BUCKET_NAME: "your-bucket-name"
    DEPICTIO_MINIO_EXTERNAL_SERVICE: true
```

Setting those values will disable the built-in MinIO service and use the external one instead.

## Authentication Configuration

Depictio supports four authentication modes. See [Authentication Modes](../usage/guides/authentication-modes.md) for a full comparison.

```bash
# Single-User Mode — personal instance, no login, full admin access
DEPICTIO_AUTH_SINGLE_USER_MODE=true

# Public Mode — anonymous read-only, sign in to create content
DEPICTIO_AUTH_PUBLIC_MODE=true

# Demo Mode — public mode + guided interactive tour
DEPICTIO_AUTH_PUBLIC_MODE=true
DEPICTIO_AUTH_DEMO_MODE=true

# Temporary user session duration (Public/Demo modes)
DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_HOURS=24

# Backward-compatible alias for Public Mode:
# DEPICTIO_AUTH_UNAUTHENTICATED_MODE=true
```

### Google OAuth Integration

Configure Google OAuth for user authentication:

```bash
# Enable Google OAuth authentication
DEPICTIO_AUTH_GOOGLE_OAUTH_ENABLED=true

# Google OAuth credentials (obtain from Google Cloud Console)
DEPICTIO_AUTH_GOOGLE_OAUTH_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
DEPICTIO_AUTH_GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret

# OAuth redirect URI (adjust to your domain)
DEPICTIO_AUTH_GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8058/auth/google/callback
```

#### Setting up Google OAuth

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable Google+ API**:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Google+ API" and enable it

3. **Create OAuth 2.0 Credentials**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Configure the consent screen if prompted
   - Set application type to "Web application"
   - Add authorized redirect URIs:
     - `http://localhost:8058/auth/google/callback` (for local development)
     - `https://your-domain.com/auth/google/callback` (for production)

4. **Copy the credentials** to your environment variables

### Authentication Keys

Configure JWT authentication keys:

```bash
# Authentication key configuration
DEPICTIO_AUTH_KEYS_DIR=depictio/keys
DEPICTIO_AUTH_KEYS_ALGORITHM=RS256
DEPICTIO_AUTH_CLI_CONFIG_DIR=depictio/.depictio
DEPICTIO_AUTH_INTERNAL_API_KEY=your-internal-api-key
```

### Custom Internal API Key

If you want to use your own internal API key instead of the auto-generated one:

```bash
# Set your custom internal API key
DEPICTIO_AUTH_INTERNAL_API_KEY=your-custom-internal-api-key-here
```

**Generating a secure API key:**

```bash
# Generate a secure random API key (Linux/macOS)
openssl rand -hex 32

# Or use Python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Custom Public/Private Key Pairs

By default, Depictio generates RS256 key pairs automatically. To use your own custom keys:

#### 1. Generate Your Own Key Pair

```bash
# Generate private key
openssl genrsa -out private_key.pem 2048

# Generate public key from private key
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

#### 2. Configure Key Directory

```bash
# Set custom keys directory
DEPICTIO_AUTH_KEYS_DIR=/path/to/your/custom/keys

# Ensure the directory contains:
# - private_key.pem
# - public_key.pem
```

#### 3. File Structure

Your custom keys directory should contain:

```text
/path/to/your/custom/keys/
├── private_key.pem    # Your private key
└── public_key.pem     # Your public key
```

#### 4. Security Considerations for Custom Keys

- **Secure Storage**: Store keys in a secure location with proper file permissions
- **Key Rotation**: Regularly rotate your keys for security
- **Backup**: Securely backup your keys
- **Access Control**: Limit access to key files

```bash
# Set proper permissions for key files
chmod 600 /path/to/your/custom/keys/private_key.pem
chmod 644 /path/to/your/custom/keys/public_key.pem
```

#### 5. Docker/Kubernetes Deployment with Custom Keys

**Docker Compose:**

```yaml
version: '3.8'
services:
  depictio-backend:
    image: depictio/depictio:latest
    volumes:
      - /path/to/your/custom/keys:/app/depictio/keys:ro
    environment:
      - DEPICTIO_AUTH_KEYS_DIR=/app/depictio/keys
```

**Kubernetes Secret:**

```bash
# Create secret from your key files
kubectl create secret generic depictio-keys \
  --from-file=private_key.pem=/path/to/your/custom/keys/private_key.pem \
  --from-file=public_key.pem=/path/to/your/custom/keys/public_key.pem

# Mount secret in your deployment
apiVersion: v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: depictio-backend
        volumeMounts:
        - name: depictio-keys
          mountPath: /app/depictio/keys
          readOnly: true
        env:
        - name: DEPICTIO_AUTH_KEYS_DIR
          value: /app/depictio/keys
      volumes:
      - name: depictio-keys
        secret:
          secretName: depictio-keys
```

## Backup and Restore Configuration

Configure backup and restore functionality:

```bash
# Backup Configuration
DEPICTIO_BACKUP_BASE_DIR=/path/to/backup/base
DEPICTIO_BACKUP_BACKUP_DIR=backups
DEPICTIO_BACKUP_S3_BACKUP_STRATEGY=s3_to_s3
DEPICTIO_BACKUP_S3_LOCAL_BACKUP_DIR=backups/s3_data_backups
DEPICTIO_BACKUP_COMPRESS_LOCAL_BACKUPS=true
DEPICTIO_BACKUP_BACKUP_FILE_RETENTION_DAYS=30
```

### Backup to Separate S3 Bucket

For production deployments, it's recommended to backup to a separate S3 bucket:

```bash
# Enable backup to separate S3 bucket
DEPICTIO_BACKUP_BACKUP_S3_ENABLED=true
DEPICTIO_BACKUP_BACKUP_S3_BUCKET=depictio-backups
DEPICTIO_BACKUP_BACKUP_S3_ENDPOINT_URL=https://s3.amazonaws.com
DEPICTIO_BACKUP_BACKUP_S3_ACCESS_KEY=your-backup-s3-access-key
DEPICTIO_BACKUP_BACKUP_S3_SECRET_KEY=your-backup-s3-secret-key
DEPICTIO_BACKUP_BACKUP_S3_REGION=us-east-1
```

### Backup Strategies

Choose from different backup strategies:

- **`s3_to_s3`**: Direct S3 to S3 backup (recommended for production)
- **`local`**: Local file system backup
- **`both`**: Both local and S3 backup

## Performance Configuration

Configure timeouts and performance settings:

```bash
# HTTP and API Timeouts
DEPICTIO_PERFORMANCE_HTTP_CLIENT_TIMEOUT=30
DEPICTIO_PERFORMANCE_API_REQUEST_TIMEOUT=60

# Browser/Screenshot Timeouts
DEPICTIO_PERFORMANCE_BROWSER_NAVIGATION_TIMEOUT=60000
DEPICTIO_PERFORMANCE_BROWSER_PAGE_LOAD_TIMEOUT=90000
DEPICTIO_PERFORMANCE_SCREENSHOT_CAPTURE_TIMEOUT=90000

# Service Readiness Configuration
DEPICTIO_PERFORMANCE_SERVICE_READINESS_RETRIES=5
DEPICTIO_PERFORMANCE_SERVICE_READINESS_DELAY=3
DEPICTIO_PERFORMANCE_SERVICE_READINESS_TIMEOUT=10
```

## Background Callbacks Configuration

Depictio uses Celery for asynchronous background processing. **Celery is required** for the dashboard editor (design mode) to function properly, as it enables non-blocking figure preview rendering during component creation.

### Required Setup

```bash
# Celery is ALWAYS enabled in the application
# The Celery worker service is always started with docker-compose
# This setting controls whether view mode also uses background callbacks
DEPICTIO_CELERY_ENABLED=true

# Configure number of Celery workers (default: 2)
DEPICTIO_CELERY_WORKERS=4
```

### How Background Callbacks Work

Celery provides asynchronous task processing for:

- **Design Mode** (Dashboard Editor): Always uses background callbacks (required)
  - Figure preview rendering during component creation
  - Real-time parameter updates without UI blocking
  - Essential for responsive dashboard building experience

- **View Mode** (Dashboard Viewing): Optionally uses background callbacks (controlled by env var)
  - When `DEPICTIO_CELERY_ENABLED=true`: Data loading executes asynchronously
  - When `false`: Data loading runs synchronously (UI may block during long operations)

Technical implementation:

- Redis is used as the message broker for task queuing
- A dedicated Celery worker service processes background tasks
- All imports are done inside callback functions for proper serialization

### Supported Components

Background callbacks can apply to:

- **Card components**: Initial render and filter updates (view mode only)
- **Figure components**: Visualization rendering and filter updates (both design and view mode)
- **Table components**: Data loading and pagination (view mode only)

### Performance Considerations

**Design Mode**:

- Always uses background callbacks (not configurable)
- UI remains responsive during figure preview generation
- Required for stepper workflow to function

**View Mode with Background Callbacks** (`DEPICTIO_CELERY_ENABLED=true`):

- UI remains responsive during data operations
- Better user experience with large datasets
- Recommended for production and multi-user environments
- Requires Redis and Celery worker service (always running)

**View Mode Synchronous** (`DEPICTIO_CELERY_ENABLED=false`):

- Only view mode operations run synchronously
- Design mode still requires Celery (always uses background)
- UI may block during long data operations
- Simpler for debugging view mode issues

### Docker Compose Configuration

The `depictio-celery-worker` service is always started and running:

```bash
# Start all services (Celery worker included by default)
docker compose up

# The worker is always running - required for design mode
# No need for profiles or conditional startup
```

## Development Settings

Enable debug logging and hot-reload:

```bash
# Enable development mode (hot-reload, verbose logging)
DEPICTIO_DEV_MODE=true

# Enable Playwright debug mode (browser automation diagnostics)
DEPICTIO_PLAYWRIGHT_DEV_MODE=true

# Pin a specific version (default: latest)
DEPICTIO_VERSION=0.7.3-b7
```

## Analytics Configuration

Depictio provides comprehensive analytics capabilities to track user interactions and system usage. You can configure both internal analytics and external Google Analytics integration.

### Internal Analytics System

Configure Depictio's built-in analytics tracking system:

```bash
# Enable internal analytics tracking
DEPICTIO_ANALYTICS_ENABLED=true

# Session timeout configuration (in minutes, range: 5-1440)
DEPICTIO_ANALYTICS_SESSION_TIMEOUT_MINUTES=30

# Data retention period (in days, range: 1-365)
DEPICTIO_ANALYTICS_CLEANUP_DAYS=90

# Enable automatic cleanup of old analytics data
DEPICTIO_ANALYTICS_CLEANUP_ENABLED=true
```

### Google Analytics Integration

Configure Google Analytics 4 (GA4) for additional web analytics:

```bash
# Enable Google Analytics tracking
DEPICTIO_GOOGLE_ANALYTICS_ENABLED=true

# GA4 Measurement ID (obtain from Google Analytics dashboard)
DEPICTIO_GOOGLE_ANALYTICS_TRACKING_ID=G-XXXXXXXXXX
```

#### Setting up Google Analytics 4

1. **Create Google Analytics Account**:
   - Go to [Google Analytics](https://analytics.google.com)
   - Create a new GA4 property for your domain

2. **Configure Data Stream**:
   - Navigate to Admin → Property → Data Streams
   - Create or select a web stream for your Depictio instance
   - Set your domain as the website URL

3. **Get Measurement ID**:
   - Copy the Measurement ID (starts with `G-`)
   - Replace `G-XXXXXXXXXX` with your actual ID

4. **Configure Environment Variables**:
   - Set both `DEPICTIO_GOOGLE_ANALYTICS_ENABLED=true` and your tracking ID
   - Ensure the same tracking ID is used for both backend and frontend services

#### Analytics Features

When analytics are enabled, the system tracks:

**Internal Analytics**:

- User session management and duration
- Dashboard interactions and component usage
- API endpoint usage patterns
- User types (authenticated, anonymous, temporary)
- Custom events and user flows

**Google Analytics** (when enabled):

- Page views and navigation events
- Session duration and engagement metrics
- User demographics and behavior flow
- Custom events for dashboard interactions
- Real-time analytics and reporting

#### Kubernetes Configuration Example

For Kubernetes deployments, use the provided example configuration:

```yaml
# Use the Google Analytics values file
helm upgrade depictio ./helm-charts/depictio \
  -f values.yaml \
  -f examples/values-google-analytics.yaml

# Or set values directly
helm upgrade depictio ./helm-charts/depictio \
  --set backend.env.DEPICTIO_GOOGLE_ANALYTICS_ENABLED=true \
  --set backend.env.DEPICTIO_GOOGLE_ANALYTICS_TRACKING_ID=G-XXXXXXXXXX \
  --set frontend.env.DEPICTIO_GOOGLE_ANALYTICS_ENABLED=true \
  --set frontend.env.DEPICTIO_GOOGLE_ANALYTICS_TRACKING_ID=G-XXXXXXXXXX
```

#### Privacy Considerations

- **GDPR Compliance**: Ensure compliance with data protection regulations
- **User Consent**: Consider implementing user consent mechanisms for analytics
- **Data Retention**: Configure appropriate `DEPICTIO_ANALYTICS_CLEANUP_DAYS` based on your data retention policies

## Security Considerations

- **Never commit sensitive credentials** to version control
- **Use strong passwords** for MinIO and other services
- **Enable HTTPS** in production environments
- **Regularly rotate API keys** and OAuth credentials
- **Set appropriate backup retention policies**
- **Use separate S3 buckets** for primary data and backups
- **Enable authentication** in production (disable unauthenticated mode)
- **Review analytics data collection** and ensure compliance with privacy regulations

## Environment Variable Validation

Depictio validates environment variables on startup. Check the logs for any configuration errors:

```bash
# Check application logs for configuration validation
docker compose logs depictio-backend
docker compose logs depictio-frontend
```

## Complete Reference

For the complete list of all environment variables with their defaults and descriptions:

- **`.env.complete.example`** - Complete env file with all 160+ variables (copy and uncomment)
- **[Environment Reference](env-reference.md)** - Searchable documentation for all variables
- **[Source Code](https://github.com/depictio/depictio/blob/main/depictio/api/v1/configs/settings_models.py)** - Pydantic settings models (source of truth)
