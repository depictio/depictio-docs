# Kubernetes Installation

Deploy Depictio on a Kubernetes cluster using the official Helm chart.

**Prerequisites**: Kubernetes 1.19+, Helm 3.2.0+, a PV provisioner (if persistence is enabled).

______________________________________________________________________

## Quick Start

### Step 1 — Clone and install

```
git clone https://github.com/depictio/depictio.git
cd depictio

helm install depictio helm-charts/depictio \
  -f helm-charts/depictio/values.yaml \
  -n depictio --create-namespace
```

### Step 2 — Wait for pods

```
kubectl get pods -n depictio --watch
```

All pods should reach `Running` status: backend, viewer, mongo, minio, redis, celery-worker. The `minio` pod runs the S3 store, SeaweedFS since v1.12.0; it keeps its name so that an upgrade reuses the same volume.

Upgrading a release from before v1.12.0?

The bundled store starts empty after the upgrade: export the bucket **before** running `helm upgrade`. See [Upgrading to v1.12.0: MinIO → SeaweedFS](https://depictio.github.io/depictio-docs/latest/installation/upgrade/v1.12.0-seaweedfs/#helm).

### Step 3 — Access Depictio

By default services are `ClusterIP`. Use port-forwarding to access locally:

```
kubectl port-forward -n depictio service/depictio-viewer 5080:5080
```

Then open <http://localhost:5080>.

| Service                 | Port |
| ----------------------- | ---- |
| Frontend (React viewer) | 5080 |
| Backend API             | 8058 |
| S3 API (SeaweedFS)      | 9000 |

The SeaweedFS admin UI is off by default. `s3.adminUI.enabled: true` serves it on `s3.service.adminPort` (`23646`), behind the S3 root credentials.

______________________________________________________________________

## Advanced Configuration

### Custom values file

Create a `my-values.yaml` to override defaults and pass it at install time:

```
helm install depictio helm-charts/depictio \
  -f helm-charts/depictio/values.yaml \
  -f my-values.yaml \
  -n depictio --create-namespace
```

To see all configurable parameters:

```
helm show values helm-charts/depictio
```

### Real-world example (EMBL)

The repository includes the EMBL demo deployment values files as a reference. They demonstrate the **layered approach**: a shared base file overlaid by environment-specific files.

| File                                                                                                                           | Purpose                                        |
| ------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- |
| [`values-embl-demo-base.yaml`](https://github.com/depictio/depictio/blob/main/helm-charts/depictio/values-embl-demo-base.yaml) | Shared settings (storage, resources, auth, S3) |
| [`values-embl-demo.yaml`](https://github.com/depictio/depictio/blob/main/helm-charts/depictio/values-embl-demo.yaml)           | Demo overlay (ingress, image tags, replicas)   |
| [`values-embl-demo-dev.yaml`](https://github.com/depictio/depictio/blob/main/helm-charts/depictio/values-embl-demo-dev.yaml)   | Dev overlay (debug flags, reduced resources)   |
| [`values-embl-auth.yaml`](https://github.com/depictio/depictio/blob/main/helm-charts/depictio/values-embl-auth.yaml)           | Multi-user auth + Google OAuth                 |

Usage pattern:

```
helm install depictio helm-charts/depictio \
  -f helm-charts/depictio/values.yaml \
  -f helm-charts/depictio/values-embl-demo-base.yaml \
  -f helm-charts/depictio/values-embl-demo.yaml \
  -n depictio --create-namespace
```

Secrets file

`values-embl-secrets.yaml` is gitignored — it holds the S3 passwords and OAuth secrets that must be created locally. See `values-embl-auth.yaml` for the expected key names.

### Single-user vs Multi-user mode

The chart starts in multi-user mode (sign-in required), unlike the root `docker-compose.yaml`.

```
# my-values.yaml
backend:
  env:
    # DEPICTIO_AUTH_SINGLE_USER_MODE: "true"   # no login, every visitor is the admin
    # DEPICTIO_AUTH_PUBLIC_MODE: "true"        # public read-only with sign-in
```

### SciLifeLab Serve

On [SciLifeLab Serve](https://serve.scilifelab.se/), the app's permission picks the mode: a **private** or **project** app runs in single-user mode (Serve's own sign-in protects it, and every visitor reaching it is the admin), a **public** or **link only** app runs in public mode (anonymous, read-only). Serve passes no extra values, so no bootstrap admin is declared.

Create the app **private first**, then switch it to public:

1. Create the app as private (or project). The first boot seeds the instance admin.
1. Open the app, copy the CLI configuration from your profile, and ingest your projects and build the dashboards with it.
1. Change the app's permission to public (or link only). The admin, its token and your content stay in place: visitors browse read-only, and the CLI keeps ingesting with the token from step 2.

An app created public has no usable admin

A public app started on an empty database seeds an admin with a random password that nobody knows, so nobody can sign in to manage it. Before v1.22.1 it did not start at all (every API call answered 504). Switch it back to private to work on it, then to public again.

### S3 credentials

```
# my-values.yaml
secrets:
  s3RootUser: "myadmin"                      # generated when empty
  s3RootPassword: "mysecurepassword"
  bootstrapAdminEmail: "admin@example.org"   # first admin, read on an empty database
  bootstrapAdminPassword: "change-me"
```

These keys were `secrets.minioRootUser` and `secrets.minioRootPassword` before v1.12.0. The old keys, and a `minio:` values block, still work and print a deprecation warning in the upgrade notes. See [Renamed settings](https://depictio.github.io/depictio-docs/latest/installation/upgrade/v1.12.0-seaweedfs/#renamed-settings).

Upgrading from pre-v1.0.0-b1 — rotate the S3 credentials

From **v1.0.0-b1** onwards the S3 root credentials are stored exclusively in a Kubernetes `Secret`. Earlier releases stored them in the `ConfigMap`, which was readable via `kubectl describe` and stored in etcd as plain text.

If you are upgrading from an older release, **rotate your S3 root credentials** after the upgrade:

1. Update `secrets.s3RootUser` and `secrets.s3RootPassword` in your values file (or a sealed secret / external-secrets source).
1. Run `helm upgrade` to apply the new Secret.
1. Restart the store's pod so it picks up the new credentials: `kubectl rollout restart deployment/depictio-minio -n depictio`

### External S3

```
# my-values.yaml
s3:
  enabled: false   # no bundled store (minio.enabled before v1.12.0)

backend:
  env:
    DEPICTIO_S3_PUBLIC_URL: "https://your-s3-host.example.com"
    DEPICTIO_S3_EXTERNAL_SERVICE: "true"
    DEPICTIO_S3_ROOT_USER: "your-access-key"
    DEPICTIO_S3_ROOT_PASSWORD: "your-secret-key"
```

An external S3 is not affected by the move from MinIO to SeaweedFS, and the `DEPICTIO_MINIO_*` names of earlier values files still work.

The bucket does not have to exist

From **v1.6.0** the backend creates `DEPICTIO_S3_BUCKET` at startup when it is missing, then verifies it; an existing bucket is left untouched. See [Required S3 permissions](https://depictio.github.io/depictio-docs/latest/installation/env-reference/#required-s3-permissions).

### Browser access to indexed files (v1.22.0+)

3D structures and file-backed genome tracks are read by the browser. `s3.browserAccess` sets [`DEPICTIO_S3_BROWSER_ACCESS`](https://depictio.github.io/depictio-docs/latest/installation/env-reference/#s3-browser-access) on the backend and the worker:

| Value          | Mode                                                                                                                                                                                                                        |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `""` (default) | Picked by the chart: `presigned` when it routes the bundled store (`ingress.enabled` or `gateway.enabled`, with `global.domain` set), or when an external store has `DEPICTIO_S3_PUBLIC_URL` in `s3.env`; `proxy` otherwise |
| `presigned`    | Browsers read S3 directly, through presigned URLs                                                                                                                                                                           |
| `proxy`        | The API streams the files: for an S3 store with no public route                                                                                                                                                             |

```
# my-values.yaml
s3:
  browserAccess: proxy   # any other value than "", presigned or proxy fails the install
```

The automatic choice reads `s3.env`, not `backend.env`. With the URL in `backend.env`, as in [External S3](#external-s3) above, it picks `proxy`: set `browserAccess: presigned`, or move `DEPICTIO_S3_PUBLIC_URL` to `s3.env`, if browsers reach the store.

### Backups (v1.22.1+)

A backup taken from *Administration* › *Backups* is written inside the backend container, and lost on its next restart, unless the chart puts a volume behind the backup directory. The `backups` values block does that, schedules the backups, and copies them off the cluster every night. All of it is off by default: a snapshot is the size of the whole database, so size the volume before the schedule starts filling it.

**Volume.** `backups.persistence.enabled: true` creates the PVC `<release>-depictio-backups-pvc` and mounts it on the backend at `/app/depictio/backups`. `size` defaults to `5Gi`, `accessMode` to `ReadWriteMany`. The PVC carries `helm.sh/resource-policy: keep`, so it survives a `helm uninstall`: it holds the only copy of the backups.

**Schedule.** `backups.schedule` sets the schedule's starting defaults: `intervalHours` and `timeOfDay` (a `HH:MM` UTC anchor, empty for a rolling interval), then `retentionDays`, `weeklyWeeks` and `monthlyMonths` for [retention](https://depictio.github.io/depictio-docs/latest/usage/administration/backup/#retention). A change saved in *Administration* › *Backups* overrides them from then on. Enabling the schedule without the volume fails the install.

**Off-cluster copy.** `backups.offsite.enabled: true` adds a CronJob that runs rclone, at 04:00 UTC by default, after the backup above. It copies the backup files from the volume to `<bucket>/<prefix>/mongo/` and keeps them there `mongo.retentionDays` days, independently of the volume's retention: a backup pruned on the volume stays in the bucket. With `data.enabled` it also syncs the instance's S3 data bucket to `<prefix>/s3-data/current/`, moving every file it overwrites or deletes to `s3-data/archive/<date>/`, kept `data.archiveDays` days. The MongoDB backups hold the pointers, the data copy what they point at: restore both from about the same night.

| Key                   | Default                                                            |
| --------------------- | ------------------------------------------------------------------ |
| `schedule`            | `0 4 * * *` (UTC)                                                  |
| `endpoint`, `bucket`  | empty, both required                                               |
| `prefix`              | the release name                                                   |
| `region`              | `us-east-1`                                                        |
| `image`               | `rclone/rclone:1.68.2`                                             |
| `mongo.retentionDays` | `365`                                                              |
| `data.enabled`        | `true`                                                             |
| `data.sourceEndpoint` | the backend's `DEPICTIO_S3_PUBLIC_URL`; set it for a bundled store |
| `data.archiveDays`    | `90`                                                               |

The destination credentials come from `existingSecret` (a Secret with the keys `ACCESS_KEY_ID` and `SECRET_ACCESS_KEY`), or from `secrets.backupS3AccessKey` and `secrets.backupS3SecretKey`, which the chart renders into the Secret `<release>-depictio-backup-s3`. The pod reuses the backend's pod labels and security contexts, pulls with `imagePullPolicy: Always` and carries a CPU limit (`resources`), as quota-enforced namespaces require. The copy needs the volume, `endpoint` and `bucket`, and one of the two credential routes: the install fails otherwise, saying which one is missing.

```
# my-values.yaml
backups:
  persistence:
    enabled: true
    size: 50Gi
  schedule:
    enabled: true
    intervalHours: 24
    timeOfDay: "03:00"     # HH:MM UTC anchor; empty means a rolling interval
    retentionDays: 30
    weeklyWeeks: 4         # on top of retentionDays, one backup per ISO week...
    monthlyMonths: 12      # ...and one per calendar month
  offsite:
    enabled: true
    endpoint: https://<your-remote>
    bucket: <your-backup-bucket>
    mongo:
      retentionDays: 365   # in the bucket, independent of the volume
    data:
      enabled: true
      archiveDays: 90

secrets:
  backupS3AccessKey: "<access-key>"
  backupS3SecretKey: "<secret-key>"
```

Restoring the S3 data from the bucket is a manual rclone copy back; the chart has no path for it.

### Ingress

Depictio's Helm chart supports three ingress topologies. Pick based on how your cluster's auth and TLS termination work.

| Topology                       | Toggle                                | When to use                                                                                                                                                                             |
| ------------------------------ | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Single ingress** (default)   | `ingress.enabled: true` only          | Viewer, backend API, and S3 store all share one ingress + annotation set. Right for small/dev clusters or when one OIDC layer covers everything.                                        |
| **Viewer + dedicated backend** | `backend.ingress.separateRoute: true` | Apply different auth annotations (or no auth) on the API. Useful when the API needs a different OIDC scope, or when programmatic clients hit `/depictio/api/*` with mTLS or API tokens. |
| **Viewer + dedicated S3**      | `s3.ingress.separateRoute: true`      | Same idea for the S3 store — typically when it is exposed for direct S3 access from CI runners and shouldn't sit behind the user-facing OIDC.                                           |

You can combine the toggles to get all three ingresses separate.

#### Per-route annotations

Each ingress has its own `annotations` block, applied in isolation:

```
# my-values.yaml
ingress:
  enabled: true
  host: depictio.yourdomain.com
  tls:
    enabled: true
    secretName: depictio-tls
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "100m"
    # OIDC annotations applied to the viewer ingress only

backend:
  ingress:
    separateRoute: true
    inheritDefaultAnnotations: false   # don't copy ingress.annotations
    annotations:
      nginx.ingress.kubernetes.io/auth-method: "BASIC"   # different auth
      nginx.ingress.kubernetes.io/proxy-body-size: "200m"

s3:
  ingress:
    separateRoute: true
    inheritDefaultAnnotations: false
    annotations: {}                     # no auth — restrict at network policy
```

`inheritDefaultAnnotations` controls whether `ingress.annotations` are merged into the per-route ingress. Set `false` when the per-route ingress needs a fundamentally different auth chain.

Network restrictions on dedicated routes

A dedicated S3 or backend ingress with `annotations: {}` is **unauthenticated at the ingress layer**. Restrict access via Kubernetes NetworkPolicies, ingress controller IP whitelisting, or a dedicated private DNS — don't rely on obscurity.

#### Gateway API instead of Ingress (v1.1.4+)

On clusters that have moved to the [Gateway API](https://gateway-api.sigs.k8s.io/), `gateway.enabled: true` emits `HTTPRoute` resources instead of Ingress objects: one for the viewer, one for the API, one for the S3 store. `parentRefs` is the only required key; per-route filters live under `backend.httpRoute` and `s3.httpRoute`, and `gateway.filters` applies to the viewer route alone.

```
# my-values.yaml
ingress:
  enabled: false
gateway:
  enabled: true
  parentRefs:
    - name: nginx-gateway
      namespace: nginx-gateway
```

Gateway API has no equivalent of the `nginx.ingress.kubernetes.io/*` annotations, so raw nginx config goes through `gateway.snippetsFilter`. Setting `enabled: true` with a list of `snippets` emits a `SnippetsFilter` and wires it into the viewer route. Both keys are ignored while `gateway.enabled` is `false`.

### Init container image pull policy

All init containers must use `pullPolicy: Always`. Capsule and Pod Security Admission (PSA) webhooks on restricted namespaces reject pods whose init containers use `IfNotPresent`, which can leave the release stuck in `Pending`.

```
# my-values.yaml
initContainerImage:
  pullPolicy: Always   # required on clusters with Capsule/PSA admission webhooks

curlInitContainerImage:
  pullPolicy: Always   # same requirement for the curl-based readiness init container
```

These keys map directly to the `initContainerImage.pullPolicy` and `curlInitContainerImage.pullPolicy` fields in `values.yaml`.

### Service link environment variables

Kubernetes injects a block of legacy Docker-link environment variables (`<SVC>_SERVICE_HOST`, `<SVC>_PORT_<port>_TCP_ADDR`, and several more) into every pod, once per service in the namespace. On a busy namespace that set grows large enough to overflow the process argument limit, and the viewer crashloops with `envsubst: Argument list too long` before nginx ever starts.

Since **v1.4.0** the chart sets `enableServiceLinks: false` on every pod it owns, which is the opposite of Kubernetes' own default ([#946](https://github.com/depictio/depictio/pull/946)):

```
# my-values.yaml
enableServiceLinks: false   # chart default; Kubernetes itself defaults to true
```

Depictio's own services address each other by DNS name, so nothing in the application reads those variables. Set it back to `true` only if something else in your deployment does.

What stays injected

`KUBERNETES_SERVICE_HOST` and `KUBERNETES_SERVICE_PORT` are injected by the kubelet regardless of this setting, so in-cluster API clients are unaffected. Pods created by the Percona MongoDB operator are also untouched, since the operator owns those pod specs.

### Celery workers

The Celery worker is enabled by default (`celery.enabled: true`): editor previews, large renders and thumbnails run on it. `DEPICTIO_CELERY_WORKERS` sets its processes (the chart sets `2`); each holds its own data, so size it with the pod's memory limit:

```
# my-values.yaml
celery:
  replicas: 1
  env:
    DEPICTIO_CELERY_WORKERS: "4"
```

No ingestion worker in the chart (v1.15.0)

The chart's worker reads only the default `celery` queue, and the chart has no [ingestion worker](https://depictio.github.io/depictio-docs/latest/installation/docker/#ingestion-worker) to read the `ingestion` queue. Leave `DEPICTIO_INGESTION_ASYNC_DELTATABLE_UPSERT` and `DEPICTIO_INGESTION_BROWSER_TRIGGER` off on Kubernetes: with either on, the jobs they create are never picked up.

### Pod labels and internet egress (v1.22.0+)

`backend.podLabels` and `celery.podLabels` add labels to the backend and worker pods (the pod template only, never the selector). Both default to the label SciLifeLab Serve reads to allow outbound traffic, which it denies by default:

```
# values.yaml defaults
backend:
  podLabels:
    networking/allow-internet-egress: "true"
celery:
  podLabels:
    networking/allow-internet-egress: "true"
```

The backend dials out for the UCSC track catalogue and genome files, remote tracks, structure lookups, OIDC and migration targets; the worker for remote data at ingestion. The label does nothing on clusters without that policy. To keep a pod off the internet on Serve, set the label to `"false"`: an empty map in an override file does not remove it, since Helm merges maps.

### Resource limits

```
# my-values.yaml
backend:
  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "4Gi"
      cpu: "2"

viewer:
  resources:
    requests:
      memory: "512Mi"
      cpu: "250m"
    limits:
      memory: "2Gi"
      cpu: "1"
```

### Google Analytics

```
# my-values.yaml — or use the bundled example
helm upgrade depictio helm-charts/depictio \
  -f helm-charts/depictio/values.yaml \
  -f helm-charts/depictio/examples/values-google-analytics.yaml
```

______________________________________________________________________

## Managing Releases

| Action       | Command                                                                 |
| ------------ | ----------------------------------------------------------------------- |
| Upgrade      | `helm upgrade depictio helm-charts/depictio -f values.yaml -n depictio` |
| Rollback     | `helm rollback depictio -n depictio`                                    |
| Uninstall    | `helm uninstall depictio -n depictio`                                   |
| Show history | `helm history depictio -n depictio`                                     |

______________________________________________________________________

## Troubleshooting

```
# Check pod status
kubectl get pods -n depictio

# Inspect logs
kubectl logs -n depictio deployment/depictio-backend
kubectl logs -n depictio deployment/depictio-viewer

# Describe a failing pod
kubectl describe pod -n depictio <pod-name>
```

Common causes: insufficient storage class, PVC pending, image pull errors.

______________________________________________________________________

## Next Steps

- [Get started with Depictio](https://depictio.github.io/depictio-docs/latest/usage/get_started/index.md)
- [Create your first dashboard](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard_creation/index.md)
- [Ingest data with the CLI](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/index.md)
