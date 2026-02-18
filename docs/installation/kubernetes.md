# Kubernetes Installation

Deploy Depictio on a Kubernetes cluster using the official Helm chart.

**Prerequisites**: Kubernetes 1.19+, Helm 3.2.0+, a PV provisioner (if persistence is enabled).

---

## :material-rocket-launch: Quick Start

### Step 1 — Clone and install

```bash
git clone https://github.com/depictio/depictio.git
cd depictio

helm install depictio helm-charts/depictio \
  -f helm-charts/depictio/values.yaml \
  -n depictio --create-namespace
```

### Step 2 — Wait for pods

```bash
kubectl get pods -n depictio --watch
```

All pods should reach `Running` status: backend, frontend, mongo, minio, redis, celery-worker.

### Step 3 — Access Depictio

By default services are `ClusterIP`. Use port-forwarding to access locally:

```bash
kubectl port-forward -n depictio service/depictio-frontend 5080:5080
```

Then open <http://localhost:5080>.

| Service | Port |
|---------|------|
| Frontend (Dash) | 5080 |
| Backend API | 8058 |
| MinIO Console | 9001 |

---

## :material-cog-outline: Advanced Configuration

### Custom values file

Create a `my-values.yaml` to override defaults and pass it at install time:

```bash
helm install depictio helm-charts/depictio \
  -f helm-charts/depictio/values.yaml \
  -f my-values.yaml \
  -n depictio --create-namespace
```

To see all configurable parameters:

```bash
helm show values helm-charts/depictio
```

### Real-world example (EMBL)

The repository includes the EMBL demo deployment values files as a reference.
They demonstrate the **layered approach**: a shared base file overlaid by
environment-specific files.

| File | Purpose |
|------|---------|
| [`values-embl-demo-base.yaml`](https://github.com/depictio/depictio/blob/main/helm-charts/depictio/values-embl-demo-base.yaml) | Shared settings (storage, resources, auth, MinIO) |
| [`values-embl-demo.yaml`](https://github.com/depictio/depictio/blob/main/helm-charts/depictio/values-embl-demo.yaml) | Demo overlay (ingress, image tags, replicas) |
| [`values-embl-demo-dev.yaml`](https://github.com/depictio/depictio/blob/main/helm-charts/depictio/values-embl-demo-dev.yaml) | Dev overlay (debug flags, reduced resources) |
| [`values-embl-auth.yaml`](https://github.com/depictio/depictio/blob/main/helm-charts/depictio/values-embl-auth.yaml) | Multi-user auth + Google OAuth |

Usage pattern:

```bash
helm install depictio helm-charts/depictio \
  -f helm-charts/depictio/values.yaml \
  -f helm-charts/depictio/values-embl-demo-base.yaml \
  -f helm-charts/depictio/values-embl-demo.yaml \
  -n depictio --create-namespace
```

!!! note "Secrets file"
    `values-embl-secrets.yaml` is gitignored — it holds MinIO passwords and OAuth
    secrets that must be created locally. See `values-embl-auth.yaml` for the
    expected key names.

### Single-user vs Multi-user mode

```yaml
# my-values.yaml
backend:
  env:
    DEPICTIO_AUTH_SINGLE_USER_MODE: "true"   # default — no login required
    # DEPICTIO_AUTH_PUBLIC_MODE: "true"        # public read-only with sign-in
```

### MinIO credentials

```yaml
# my-values.yaml
secrets:
  minioRootUser: "myadmin"
  minioRootPassword: "mysecurepassword"
```

### External S3 / Bring Your Own MinIO

```yaml
# my-values.yaml
minio:
  enabled: false   # disable bundled MinIO

backend:
  env:
    DEPICTIO_MINIO_PUBLIC_URL: "https://your-minio-host.example.com"
    DEPICTIO_MINIO_EXTERNAL_SERVICE: "true"
    DEPICTIO_MINIO_ROOT_USER: "your-access-key"
    DEPICTIO_MINIO_ROOT_PASSWORD: "your-secret-key"
```

### Ingress

```yaml
# my-values.yaml
ingress:
  enabled: true
  host: depictio.yourdomain.com
  tls:
    enabled: true
    secretName: depictio-tls
```

### Celery workers (background callbacks)

The Celery worker is included and enabled by default (`celery.enabled: true`).
Design mode always requires Celery. View mode behaviour is controlled separately:

```yaml
# my-values.yaml
celery:
  replicas: 1
  env:
    DEPICTIO_CELERY_WORKERS: "4"
    DEPICTIO_CELERY_ENABLED: "true"   # async view mode (recommended for production)
```

### Resource limits

```yaml
# my-values.yaml
backend:
  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "4Gi"
      cpu: "2"

frontend:
  resources:
    requests:
      memory: "512Mi"
      cpu: "250m"
    limits:
      memory: "2Gi"
      cpu: "1"
```

### Google Analytics

```yaml
# my-values.yaml — or use the bundled example
helm upgrade depictio helm-charts/depictio \
  -f helm-charts/depictio/values.yaml \
  -f helm-charts/depictio/examples/values-google-analytics.yaml
```

---

## :material-wrench: Managing Releases

| Action | Command |
|--------|---------|
| Upgrade | `helm upgrade depictio helm-charts/depictio -f values.yaml -n depictio` |
| Rollback | `helm rollback depictio -n depictio` |
| Uninstall | `helm uninstall depictio -n depictio` |
| Show history | `helm history depictio -n depictio` |

---

## :material-bug: Troubleshooting

```bash
# Check pod status
kubectl get pods -n depictio

# Inspect logs
kubectl logs -n depictio deployment/depictio-backend
kubectl logs -n depictio deployment/depictio-frontend

# Describe a failing pod
kubectl describe pod -n depictio <pod-name>
```

Common causes: insufficient storage class, PVC pending, image pull errors.

---

## Next Steps

- [Get started with Depictio](../usage/get_started.md)
- [Create your first dashboard](../usage/guides/dashboard_creation.md)
- [Ingest data with the CLI](../depictio-cli/usage.md)
