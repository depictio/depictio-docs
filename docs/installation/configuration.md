---
title: "Configuration"
icon: material/cog
description: "Configure Depictio with environment variables for various features and integrations."
---

# Environment Variables Configuration

Depictio uses environment variables to configure various aspects of the application. This guide covers the key environment variables you can set to customize your deployment.

## Base Configuration

The base configuration is available in the [.env.example](https://github.com/depictio/depictio/blob/main/.env.example) file in the repository. Copy this file to `.env` and modify the values as needed.

### Basic Setup

```bash
# Application Context
DEPICTIO_CONTEXT=server
DEPICTIO_LOGGING_VERBOSITY_LEVEL=ERROR

# MinIO Storage Configuration
DEPICTIO_MINIO_ROOT_USER=minio
DEPICTIO_MINIO_ROOT_PASSWORD=minio123
DEPICTIO_MINIO_PUBLIC_URL=http://localhost:9000

# MongoDB Configuration
DEPICTIO_MONGODB_DB_NAME=depictioDB
DEPICTIO_MONGODB_PORT=27018
DEPICTIO_MONGODB_SERVICE_NAME=mongo
DEPICTIO_MONGODB_WIPE=false

# FastAPI Server Configuration
DEPICTIO_FASTAPI_HOST=0.0.0.0
DEPICTIO_FASTAPI_PORT=8058
DEPICTIO_FASTAPI_SERVICE_NAME=depictio-backend
DEPICTIO_FASTAPI_PUBLIC_URL=http://localhost:8058

# Dash Frontend Configuration
DEPICTIO_DASH_HOST=0.0.0.0
DEPICTIO_DASH_PORT=5080
DEPICTIO_DASH_SERVICE_NAME=depictio-frontend
```

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

### Unauthenticated Mode

Enable unauthenticated mode to allow anonymous access to your Depictio instance:

```bash
# Enable unauthenticated mode (allows anonymous access)
DEPICTIO_AUTH_UNAUTHENTICATED_MODE=true

# Anonymous user configuration
DEPICTIO_AUTH_ANONYMOUS_USER_EMAIL=anonymous@depict.io
DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_HOURS=24
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

Depictio supports asynchronous background callbacks using Celery for long-running operations. This feature significantly improves UI responsiveness when working with large datasets.

### Enabling Background Callbacks

```bash
# Enable background callbacks (async mode)
DEPICTIO_USE_BACKGROUND_CALLBACKS=true

# Configure number of Celery workers (default: 2)
DEPICTIO_CELERY_WORKERS=4
```

### How Background Callbacks Work

When enabled:

- Long-running operations (data loading, visualization rendering) execute asynchronously
- The UI remains responsive during data processing
- Redis is used as the message broker for task queuing
- A dedicated Celery worker service processes background tasks

### Supported Components

Background callbacks apply to:

- **Card components**: Initial render and filter updates
- **Figure components**: Visualization rendering and filter updates
- **Table components**: Data loading and pagination

### Performance Considerations

**Synchronous mode** (default):

- UI blocks during data operations
- Simpler architecture, easier debugging
- Suitable for small datasets and single-user deployments

**Background mode** (enabled):

- UI remains responsive during operations
- Better user experience with large datasets
- Recommended for production and multi-user environments
- Requires Redis and Celery worker service

### Docker Compose Configuration

The `depictio-celery-worker` service automatically adapts based on the environment variable:

- If `DEPICTIO_USE_BACKGROUND_CALLBACKS=true`: Worker starts and processes tasks
- If `false` or not set: Worker exits gracefully without consuming resources

No need to manually start/stop the worker service or use Docker Compose profiles.

### Kubernetes/Helm Compatibility

<!-- markdownlint-disable MD046 -->

!!! info "K8S/Helm Support Coming Soon"

    Background callbacks are currently only supported in Docker Compose deployments. Kubernetes/Helm support is **coming soon** in an upcoming release.

<!-- markdownlint-enable MD046 -->

## Development Settings

Configuration for development and testing:

```bash
# Development Mode
DEV_MODE=true
DEPICTIO_PLAYWRIGHT_DEV_MODE=true
DEPICTIO_TEST_MODE=true

# Version Information
DEPICTIO_VERSION=latest
```

## Docker/Kubernetes Configuration

For containerized deployments:

```bash
# Container Configuration
UID=502
GID=20

# Kubernetes-specific (if deploying to Kubernetes)
KUBERNETES_NAMESPACE=depictio
KUBERNETES_NODE_NAME=node-1
```

## Complete Example

Here's a complete example configuration for a production deployment with all features enabled:

```bash
# ============================================================================
# DEPICTIO PRODUCTION CONFIGURATION
# ============================================================================

# Application Context
DEPICTIO_CONTEXT=server
DEPICTIO_LOGGING_VERBOSITY_LEVEL=INFO
DEPICTIO_VERSION=latest

# MinIO Storage Configuration
DEPICTIO_MINIO_ROOT_USER=minio
DEPICTIO_MINIO_ROOT_PASSWORD=secure-minio-password
DEPICTIO_MINIO_PUBLIC_URL=https://minio.yourdomain.com

# MongoDB Configuration
DEPICTIO_MONGODB_DB_NAME=depictioDB
DEPICTIO_MONGODB_PORT=27017
DEPICTIO_MONGODB_SERVICE_NAME=mongo
DEPICTIO_MONGODB_WIPE=false

# FastAPI Server Configuration
DEPICTIO_FASTAPI_HOST=0.0.0.0
DEPICTIO_FASTAPI_PORT=8058
DEPICTIO_FASTAPI_SERVICE_NAME=depictio-backend
DEPICTIO_FASTAPI_PUBLIC_URL=https://api.yourdomain.com

# Dash Frontend Configuration
DEPICTIO_DASH_HOST=0.0.0.0
DEPICTIO_DASH_PORT=5080
DEPICTIO_DASH_SERVICE_NAME=depictio-frontend

# Authentication Configuration
DEPICTIO_AUTH_UNAUTHENTICATED_MODE=false
DEPICTIO_AUTH_KEYS_DIR=depictio/keys
DEPICTIO_AUTH_KEYS_ALGORITHM=RS256

# Google OAuth Configuration
DEPICTIO_AUTH_GOOGLE_OAUTH_ENABLED=true
DEPICTIO_AUTH_GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
DEPICTIO_AUTH_GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
DEPICTIO_AUTH_GOOGLE_OAUTH_REDIRECT_URI=https://yourdomain.com/auth/google/callback

# Backup Configuration
DEPICTIO_BACKUP_BASE_DIR=/var/backups/depictio
DEPICTIO_BACKUP_BACKUP_DIR=backups
DEPICTIO_BACKUP_S3_BACKUP_STRATEGY=s3_to_s3
DEPICTIO_BACKUP_BACKUP_S3_ENABLED=true
DEPICTIO_BACKUP_BACKUP_S3_BUCKET=depictio-backups
DEPICTIO_BACKUP_BACKUP_S3_ENDPOINT_URL=https://s3.amazonaws.com
DEPICTIO_BACKUP_BACKUP_S3_ACCESS_KEY=your-backup-access-key
DEPICTIO_BACKUP_BACKUP_S3_SECRET_KEY=your-backup-secret-key
DEPICTIO_BACKUP_BACKUP_S3_REGION=us-east-1
DEPICTIO_BACKUP_COMPRESS_LOCAL_BACKUPS=true
DEPICTIO_BACKUP_BACKUP_FILE_RETENTION_DAYS=30

# Performance Configuration
DEPICTIO_PERFORMANCE_HTTP_CLIENT_TIMEOUT=30
DEPICTIO_PERFORMANCE_API_REQUEST_TIMEOUT=60
DEPICTIO_PERFORMANCE_BROWSER_NAVIGATION_TIMEOUT=60000

# JBrowse Integration
DEPICTIO_JBROWSE_ENABLED=true

# Analytics Configuration
DEPICTIO_ANALYTICS_ENABLED=true
DEPICTIO_ANALYTICS_SESSION_TIMEOUT_MINUTES=30
DEPICTIO_ANALYTICS_CLEANUP_DAYS=90
DEPICTIO_ANALYTICS_TRACK_ANONYMOUS_USERS=false
DEPICTIO_ANALYTICS_CLEANUP_ENABLED=true

# Google Analytics Configuration
DEPICTIO_GOOGLE_ANALYTICS_ENABLED=true
DEPICTIO_GOOGLE_ANALYTICS_TRACKING_ID=G-XXXXXXXXXX

# Development Settings (set to false for production)
DEV_MODE=false
DEPICTIO_PLAYWRIGHT_DEV_MODE=false
DEPICTIO_TEST_MODE=false
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

For more detailed configuration options, refer to the [source code settings models](https://github.com/depictio/depictio/blob/main/depictio/api/v1/configs/settings_models.py).
