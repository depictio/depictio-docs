---
title: "Environment Variables Reference"
icon: material/cog-outline
description: "Complete reference for all Depictio environment variables. Auto-generated on 2026-01-22."
---

# Environment Variables Reference

This page contains the complete reference for all configurable environment variables in Depictio.

!!! info "Auto-generated Documentation"

    This documentation is auto-generated from the [settings_models.py](https://github.com/depictio/depictio/blob/main/depictio/api/v1/configs/settings_models.py) source file to ensure accuracy.

## Quick Start

For most deployments, you only need to configure a few variables. See the [Quick Start Guide](docker.md) for the minimal configuration.

```bash
# Minimal required configuration
DEPICTIO_MINIO_ROOT_USER=minio
DEPICTIO_MINIO_ROOT_PASSWORD=minio123
```

!!! tip "Complete Environment File"

    For a ready-to-use file with all variables, copy `.env.complete.example` to `.env` and uncomment the variables you need.

## Variable Reference by Category

### Quick Navigation

- [FastAPI Backend](#fastapi-backend)
- [Dash Frontend](#dash-frontend)
- [MongoDB Database](#mongodb-database)
- [MinIO/S3 Storage](#minios3-storage)
- [Authentication](#authentication)
- [Redis Cache](#redis-cache)
- [Celery Task Queue](#celery-task-queue)
- [Performance & Timeouts](#performance-timeouts)
- [Backup & Restore](#backup-restore)
- [Internal Analytics](#internal-analytics)
- [Google Analytics](#google-analytics)
- [Logging](#logging)
<!-- - [JBrowse Integration](#jbrowse-integration) -->
- [S3 File Cache](#s3-file-cache)
- [Application Profiling](#application-profiling)
- [Dashboard YAML Sync](#dashboard-yaml-sync)
- [Global Settings](#global-settings)
- [ServiceConfig](#serviceconfig)

---

## FastAPI Backend

**Config Class:** `FastAPIConfig`
**Environment Prefix:** `DEPICTIO_FASTAPI_`

Base class for service configurations with internal/external URL handling.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_FASTAPI_SERVICE_NAME` | `depictio-backend` | - |
| `DEPICTIO_FASTAPI_SERVICE_PORT` | `8058` | - |
| `DEPICTIO_FASTAPI_EXTERNAL_HOST` | `localhost` | - |
| `DEPICTIO_FASTAPI_EXTERNAL_PORT` | `8058` | - |
| `DEPICTIO_FASTAPI_EXTERNAL_PROTOCOL` | `http` | - |
| `DEPICTIO_FASTAPI_PUBLIC_URL` | - | - |
| `DEPICTIO_FASTAPI_EXTERNAL_SERVICE` | `false` | - |
| `DEPICTIO_FASTAPI_HOST` | `0.0.0.0` | - |
| `DEPICTIO_FASTAPI_WORKERS` | `4` | - |
| `DEPICTIO_FASTAPI_SSL` | `false` | - |
| `DEPICTIO_FASTAPI_LOGGING_LEVEL` | `INFO` | - |

---

## Dash Frontend

**Config Class:** `DashConfig`
**Environment Prefix:** `DEPICTIO_DASH_`

Base class for service configurations with internal/external URL handling.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_DASH_SERVICE_NAME` | `depictio-frontend` | - |
| `DEPICTIO_DASH_SERVICE_PORT` | `5080` | - |
| `DEPICTIO_DASH_EXTERNAL_HOST` | `localhost` | - |
| `DEPICTIO_DASH_EXTERNAL_PORT` | `5080` | - |
| `DEPICTIO_DASH_EXTERNAL_PROTOCOL` | `http` | - |
| `DEPICTIO_DASH_PUBLIC_URL` | - | - |
| `DEPICTIO_DASH_EXTERNAL_SERVICE` | `false` | - |
| `DEPICTIO_DASH_HOST` | `0.0.0.0` | - |
| `DEPICTIO_DASH_WORKERS` | `4` | - |
| `DEPICTIO_DASH_DEBUG` | `true` | - |
| `DEPICTIO_DASH_AUTO_GENERATE_FIGURES` | `false` | Enable automatic figure generation in UI mode |

---

## MongoDB Database

**Config Class:** `MongoDBConfig`
**Environment Prefix:** `DEPICTIO_MONGODB_`

Base class for service configurations with internal/external URL handling.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_MONGODB_SERVICE_NAME` | `mongo` | - |
| `DEPICTIO_MONGODB_SERVICE_PORT` | `27018` | - |
| `DEPICTIO_MONGODB_EXTERNAL_HOST` | `localhost` | - |
| `DEPICTIO_MONGODB_EXTERNAL_PORT` | `27018` | - |
| `DEPICTIO_MONGODB_EXTERNAL_PROTOCOL` | `http` | - |
| `DEPICTIO_MONGODB_PUBLIC_URL` | - | - |
| `DEPICTIO_MONGODB_EXTERNAL_SERVICE` | `false` | - |
| `DEPICTIO_MONGODB_DB_NAME` | `depictioDB` | - |
| `DEPICTIO_MONGODB_WIPE` | `false` | - |

---

## MinIO/S3 Storage

**Config Class:** `S3DepictioCLIConfig`
**Environment Prefix:** `DEPICTIO_MINIO_`

S3 configuration inheriting service URL management.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_MINIO_SERVICE_NAME` | `minio` | - |
| `DEPICTIO_MINIO_SERVICE_PORT` | `9000` | - |
| `DEPICTIO_MINIO_EXTERNAL_HOST` | `localhost` | - |
| `DEPICTIO_MINIO_EXTERNAL_PORT` | `9000` | - |
| `DEPICTIO_MINIO_EXTERNAL_PROTOCOL` | `http` | - |
| `DEPICTIO_MINIO_PUBLIC_URL` | - | - |
| `DEPICTIO_MINIO_EXTERNAL_SERVICE` | `false` | - |
| `DEPICTIO_MINIO_ROOT_USER` | `minio` | - |
| `DEPICTIO_MINIO_ROOT_PASSWORD` | `minio123` | - |
| `DEPICTIO_MINIO_BUCKET` | `depictio-bucket` | - |

---

## Authentication

**Config Class:** `AuthConfig`
**Environment Prefix:** `DEPICTIO_AUTH_`

Authentication and authorization settings including JWT configuration, unauthenticated mode, and Google OAuth integration.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_AUTH_KEYS_DIR` | `PydanticUndefined` | - |
| `DEPICTIO_AUTH_KEYS_ALGORITHM` | `RS256` | - |
| `DEPICTIO_AUTH_CLI_CONFIG_DIR` | `PydanticUndefined` | - |
| `DEPICTIO_AUTH_INTERNAL_API_KEY_ENV` | - | - |
| `DEPICTIO_AUTH_UNAUTHENTICATED_MODE` | `false` | Enable unauthenticated mode |
| `DEPICTIO_AUTH_ANONYMOUS_USER_EMAIL` | `anonymous@depict.io` | Default anonymous user email |
| `DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_HOURS` | `24` | Number of hours until temporary users expire |
| `DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_MINUTES` | `0` | Number of minutes until temporary users expire |
| `DEPICTIO_AUTH_GOOGLE_OAUTH_ENABLED` | `false` | Enable Google OAuth authentication |
| `DEPICTIO_AUTH_GOOGLE_OAUTH_CLIENT_ID` | - | Google OAuth client ID |
| `DEPICTIO_AUTH_GOOGLE_OAUTH_CLIENT_SECRET` | - | Google OAuth client secret |
| `DEPICTIO_AUTH_GOOGLE_OAUTH_REDIRECT_URI` | - | Google OAuth redirect URI |

---

## Redis Cache

**Config Class:** `CacheConfig`
**Environment Prefix:** `DEPICTIO_CACHE_`

Redis cache configuration settings.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_CACHE_REDIS_HOST` | `redis` | Redis server hostname |
| `DEPICTIO_CACHE_REDIS_PORT` | `6379` | Redis server port |
| `DEPICTIO_CACHE_REDIS_PASSWORD` | - | Redis password |
| `DEPICTIO_CACHE_REDIS_DB` | `0` | Redis database number |
| `DEPICTIO_CACHE_REDIS_SSL` | `false` | Use SSL for Redis connection |
| `DEPICTIO_CACHE_ENABLE_REDIS_CACHE` | `true` | Enable Redis caching for DataFrames |
| `DEPICTIO_CACHE_FALLBACK_TO_MEMORY` | `true` | Fallback to in-memory cache if Redis fails |
| `DEPICTIO_CACHE_DEFAULT_TTL` | `3600` | Default cache TTL in seconds (1 hour) |
| `DEPICTIO_CACHE_DATAFRAME_TTL` | `1800` | DataFrame cache TTL in seconds (30 minutes) |
| `DEPICTIO_CACHE_MAX_DATAFRAME_SIZE_MB` | `100` | Maximum DataFrame size to cache (MB) |
| `DEPICTIO_CACHE_REDIS_MAX_MEMORY_MB` | `1024` | Redis max memory limit (MB) |
| `DEPICTIO_CACHE_CACHE_KEY_PREFIX` | `depictio:df:` | Prefix for cache keys |
| `DEPICTIO_CACHE_CACHE_VERSION` | `v1` | Cache version for key namespacing |

---

## Celery Task Queue

**Config Class:** `CeleryConfig`
**Environment Prefix:** `DEPICTIO_CELERY_`

Celery task queue configuration for background processing.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_CELERY_BROKER_HOST` | `redis` | Redis broker hostname |
| `DEPICTIO_CELERY_BROKER_PORT` | `6379` | Redis broker port |
| `DEPICTIO_CELERY_BROKER_PASSWORD` | - | Redis broker password |
| `DEPICTIO_CELERY_BROKER_DB` | `1` | Redis database for Celery broker |
| `DEPICTIO_CELERY_RESULT_BACKEND_HOST` | `redis` | Redis result backend hostname |
| `DEPICTIO_CELERY_RESULT_BACKEND_PORT` | `6379` | Redis result backend port |
| `DEPICTIO_CELERY_RESULT_BACKEND_PASSWORD` | - | Redis result backend password |
| `DEPICTIO_CELERY_RESULT_BACKEND_DB` | `2` | Redis database for Celery results |
| `DEPICTIO_CELERY_WORKER_CONCURRENCY` | `2` | Number of concurrent worker processes |
| `DEPICTIO_CELERY_WORKER_POOL` | `threads` | Worker pool type (threads, processes) |
| `DEPICTIO_CELERY_WORKER_PREFETCH_MULTIPLIER` | `1` | Worker prefetch multiplier |
| `DEPICTIO_CELERY_WORKER_MAX_TASKS_PER_CHILD` | `50` | Max tasks per worker before restart |
| `DEPICTIO_CELERY_TASK_SOFT_TIME_LIMIT` | `300` | Task soft time limit in seconds (5min) |
| `DEPICTIO_CELERY_TASK_TIME_LIMIT` | `600` | Task hard time limit in seconds (10min) |
| `DEPICTIO_CELERY_RESULT_EXPIRES` | `3600` | Task result expiration in seconds (1hr) |
| `DEPICTIO_CELERY_DEFAULT_QUEUE` | `dashboard_tasks` | Default task queue name |
| `DEPICTIO_CELERY_WORKER_SEND_TASK_EVENTS` | `true` | Enable task event monitoring |
| `DEPICTIO_CELERY_TASK_SEND_SENT_EVENT` | `true` | Send task sent events |

---

## Performance & Timeouts

**Config Class:** `PerformanceConfig`
**Environment Prefix:** `DEPICTIO_PERFORMANCE_`

Performance and timeout settings that can be tuned per environment.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_PERFORMANCE_HTTP_CLIENT_TIMEOUT` | `30` | - |
| `DEPICTIO_PERFORMANCE_API_REQUEST_TIMEOUT` | `60` | - |
| `DEPICTIO_PERFORMANCE_BROWSER_NAVIGATION_TIMEOUT` | `60000` | - |
| `DEPICTIO_PERFORMANCE_BROWSER_PAGE_LOAD_TIMEOUT` | `90000` | - |
| `DEPICTIO_PERFORMANCE_BROWSER_ELEMENT_TIMEOUT` | `30000` | - |
| `DEPICTIO_PERFORMANCE_SCREENSHOT_NAVIGATION_TIMEOUT` | `45000` | - |
| `DEPICTIO_PERFORMANCE_SCREENSHOT_CONTENT_WAIT` | `15000` | - |
| `DEPICTIO_PERFORMANCE_SCREENSHOT_STABILIZATION_WAIT` | `5000` | - |
| `DEPICTIO_PERFORMANCE_SCREENSHOT_CAPTURE_TIMEOUT` | `90000` | - |
| `DEPICTIO_PERFORMANCE_SCREENSHOT_API_TIMEOUT` | `300` | - |
| `DEPICTIO_PERFORMANCE_SERVICE_READINESS_RETRIES` | `5` | - |
| `DEPICTIO_PERFORMANCE_SERVICE_READINESS_DELAY` | `3` | - |
| `DEPICTIO_PERFORMANCE_SERVICE_READINESS_TIMEOUT` | `10` | - |
| `DEPICTIO_PERFORMANCE_DNS_CACHE_TTL` | `300` | - |
| `DEPICTIO_PERFORMANCE_CONNECTION_POOL_SIZE` | `10` | - |
| `DEPICTIO_PERFORMANCE_MAX_KEEPALIVE_CONNECTIONS` | `5` | - |
| `DEPICTIO_PERFORMANCE_DISABLE_LOADING_SPINNERS` | `true` | Disable all loading spinners for maximum performance |
| `DEPICTIO_PERFORMANCE_DISABLE_ANIMATIONS` | `true` | Disable SVG and CSS animations for maximum performance |
| `DEPICTIO_PERFORMANCE_DISABLE_THEME_ANIMATIONS` | `true` | Disable theme CSS injection and complex theme operations |

---

## Backup & Restore

**Config Class:** `BackupConfig`
**Environment Prefix:** `DEPICTIO_BACKUP_`

Backup and restore configuration settings.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_BACKUP_BASE_DIR` | `PydanticUndefined` | - |
| `DEPICTIO_BACKUP_BACKUP_DIR` | `backups` | - |
| `DEPICTIO_BACKUP_S3_BACKUP_STRATEGY` | `s3_to_s3` | Strategy for S3 data backup: 's3_to_s3', 'local', or 'both' |
| `DEPICTIO_BACKUP_S3_LOCAL_BACKUP_DIR` | `backups/s3_data_backups` | - |
| `DEPICTIO_BACKUP_BACKUP_S3_ENABLED` | `false` | Enable separate backup S3 bucket |
| `DEPICTIO_BACKUP_BACKUP_S3_BUCKET` | `depictio-backups` | Backup S3 bucket name |
| `DEPICTIO_BACKUP_BACKUP_S3_ENDPOINT_URL` | - | Backup S3 endpoint URL |
| `DEPICTIO_BACKUP_BACKUP_S3_ACCESS_KEY` | - | Backup S3 access key |
| `DEPICTIO_BACKUP_BACKUP_S3_SECRET_KEY` | - | Backup S3 secret key |
| `DEPICTIO_BACKUP_BACKUP_S3_REGION` | `us-east-1` | Backup S3 region |
| `DEPICTIO_BACKUP_COMPRESS_LOCAL_BACKUPS` | `true` | Compress local S3 data backups |
| `DEPICTIO_BACKUP_BACKUP_FILE_RETENTION_DAYS` | `30` | Days to retain backup files |

---

## Internal Analytics

**Config Class:** `AnalyticsConfig`
**Environment Prefix:** `DEPICTIO_ANALYTICS_`

Configuration for analytics tracking.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_ANALYTICS_ENABLED` | `false` | Enable analytics tracking |
| `DEPICTIO_ANALYTICS_SESSION_TIMEOUT_MINUTES` | `30` | Session timeout in minutes |
| `DEPICTIO_ANALYTICS_CLEANUP_DAYS` | `90` | Days to retain analytics data |
| `DEPICTIO_ANALYTICS_TRACK_ANONYMOUS_USERS` | `true` | Track anonymous user sessions |
| `DEPICTIO_ANALYTICS_CLEANUP_ENABLED` | `true` | Enable automatic cleanup of old analytics data |

---

## Google Analytics

**Config Class:** `GoogleAnalyticsConfig`
**Environment Prefix:** `DEPICTIO_GOOGLE_ANALYTICS_`

Configuration for Google Analytics tracking.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_GOOGLE_ANALYTICS_ENABLED` | `false` | Enable Google Analytics tracking |
| `DEPICTIO_GOOGLE_ANALYTICS_TRACKING_ID` | - | Google Analytics tracking ID (GA4 measurement ID) |

---

## Logging

**Config Class:** `LoggingConfig`
**Environment Prefix:** `DEPICTIO_LOGGING_`

Logging verbosity and output configuration.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_LOGGING_VERBOSITY_LEVEL` | `ERROR` | - |

---

<!-- ## JBrowse Integration (Coming Soon - see Roadmap)

**Config Class:** `JBrowseConfig`
**Environment Prefix:** `DEPICTIO_JBROWSE_`

JBrowse genome browser integration settings.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_JBROWSE_ENABLED` | `false` | - |

--- -->

## S3 File Cache

**Config Class:** `S3CacheConfig`
**Environment Prefix:** `DEPICTIO_S3_`

S3 file caching configuration for MultiQC and other S3 operations.

The cache directory stores downloaded S3 files locally to avoid repeated downloads.
Default location is ~/.depictio/s3_cache (persistent across restarts).

Environment variable: DEPICTIO_S3_CACHE_DIR
Example: export DEPICTIO_S3_CACHE_DIR=/data/depictio_s3_cache

Note: The previous default /tmp/depictio_s3_cache was ephemeral and caused
repeated downloads after system restarts.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_S3_CACHE_DIR` | `~/.depictio/s3_cache` | Local directory for S3 file cache. Use DEPICTIO_S3_CACHE_DIR to override. |
| `DEPICTIO_S3_MOUNT_POINTS` | `""` | Comma-separated S3 FUSE mount points |

---

## Application Profiling

**Config Class:** `ProfilingConfig`
**Environment Prefix:** `DEPICTIO_PROFILING_`

Configuration for application profiling.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_PROFILING_ENABLED` | `false` | Enable application profiling |
| `DEPICTIO_PROFILING_PROFILE_DIR` | `./prof_files` | Directory to save profile files |
| `DEPICTIO_PROFILING_SORT_BY` | `cumtime,tottime` | Profile sorting criteria |
| `DEPICTIO_PROFILING_RESTRICTIONS` | `50` | Number of top functions to show in reports |
| `DEPICTIO_PROFILING_MEMORY_PROFILING` | `false` | Enable memory usage profiling |
| `DEPICTIO_PROFILING_WERKZEUG_ENABLED` | `true` | Enable Werkzeug request profiling |
| `DEPICTIO_PROFILING_WERKZEUG_STREAM` | `false` | Stream profiling output to terminal |
| `DEPICTIO_PROFILING_WERKZEUG_SAFE_MODE` | `true` | Enable safe mode to prevent profiler conflicts |
| `DEPICTIO_PROFILING_PROFILE_CALLBACKS` | `false` | Enable automatic callback profiling |
| `DEPICTIO_PROFILING_PROFILE_SLOW_CALLBACKS_ONLY` | `true` | Only profile callbacks slower than threshold |
| `DEPICTIO_PROFILING_SLOW_CALLBACK_THRESHOLD` | `0.1` | Threshold in seconds for slow callbacks |

---

## Dashboard YAML Sync

**Config Class:** `DashboardYAMLConfig`
**Environment Prefix:** `DEPICTIO_DASHBOARD_YAML_`

Configuration for YAML-based dashboard management.

Enables file-based dashboard editing where users can read/write YAML files
directly from a designated directory for version control and IaC workflows.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_DASHBOARD_YAML_ENABLED` | `true` | Enable YAML-based dashboard management |
| `DEPICTIO_DASHBOARD_YAML_LOCAL_DIR` | `PydanticUndefined` | Directory for instance-specific dashboard YAML files (auto-synced) |
| `DEPICTIO_DASHBOARD_YAML_TEMPLATES_DIR` | `PydanticUndefined` | Directory for template dashboard YAML files (version control) |
| `DEPICTIO_DASHBOARD_YAML_BASE_DIR` | - | DEPRECATED: Use local_dir instead. Base directory for dashboard YAML files |
| `DEPICTIO_DASHBOARD_YAML_ORGANIZE_BY_PROJECT` | `true` | Organize YAML files in subdirectories by project name |
| `DEPICTIO_DASHBOARD_YAML_USE_DASHBOARD_TITLE` | `true` | Use dashboard title in filename (vs just ID) |
| `DEPICTIO_DASHBOARD_YAML_INCLUDE_EXPORT_METADATA` | `true` | Include export timestamp and version in YAML files |
| `DEPICTIO_DASHBOARD_YAML_COMPACT_MODE` | `true` | Use compact YAML format with references (75-80% smaller files) |
| `DEPICTIO_DASHBOARD_YAML_MVP_MODE` | `true` | Use MVP minimal YAML format (60-80 lines, human-readable IDs, no layout) |
| `DEPICTIO_DASHBOARD_YAML_REGENERATE_STATS` | `true` | Regenerate column statistics on import instead of storing in YAML |
| `DEPICTIO_DASHBOARD_YAML_AUTO_LAYOUT` | `false` | Auto-generate component layout on import if missing |
| `DEPICTIO_DASHBOARD_YAML_AUTO_EXPORT_ON_SAVE` | `true` | Automatically export to YAML when dashboard is saved |
| `DEPICTIO_DASHBOARD_YAML_AUTO_IMPORT_ON_CHANGE` | `true` | Automatically import from YAML when files change (requires watcher) |
| `DEPICTIO_DASHBOARD_YAML_WATCHER_DEBOUNCE_SECONDS` | `2.0` | Seconds to wait after file change before syncing |
| `DEPICTIO_DASHBOARD_YAML_WATCHER_AUTO_START` | `true` | Automatically start the file watcher on API startup |
| `DEPICTIO_DASHBOARD_YAML_WATCH_LOCAL_DIR` | `true` | Watch and auto-sync local dashboards directory |
| `DEPICTIO_DASHBOARD_YAML_WATCH_TEMPLATES_DIR` | `false` | Watch and auto-sync templates directory (useful for template development) |
| `DEPICTIO_DASHBOARD_YAML_ENABLE_VALIDATION` | `true` | Enable validation gate before syncing YAML to MongoDB |
| `DEPICTIO_DASHBOARD_YAML_BLOCK_ON_VALIDATION_ERRORS` | `true` | Block sync if validation fails (set False to only warn) |
| `DEPICTIO_DASHBOARD_YAML_VALIDATE_COLUMN_NAMES` | `true` | Validate that column names exist in data collection schema |
| `DEPICTIO_DASHBOARD_YAML_VALIDATE_COMPONENT_TYPES` | `true` | Validate chart types, aggregation functions, and filter types |

---

## Global Settings

**Config Class:** `Settings`
**Environment Prefix:** `DEPICTIO_`

Top-level application settings including context configuration.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_CONTEXT` | `server` | - |

---

## ServiceConfig

**Config Class:** `ServiceConfig`
**Environment Prefix:** `DEPICTIO_`

Base class for service configurations with internal/external URL handling.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_SERVICE_NAME` | `PydanticUndefined` | - |
| `DEPICTIO_SERVICE_PORT` | `PydanticUndefined` | - |
| `DEPICTIO_EXTERNAL_HOST` | `localhost` | - |
| `DEPICTIO_EXTERNAL_PORT` | `PydanticUndefined` | - |
| `DEPICTIO_EXTERNAL_PROTOCOL` | `http` | - |
| `DEPICTIO_PUBLIC_URL` | - | - |
| `DEPICTIO_EXTERNAL_SERVICE` | `false` | - |

---

## See Also

- [Quick Start with Docker](docker.md)
- [Configuration Guide](configuration.md)
- [Kubernetes Installation](kubernetes.md)
