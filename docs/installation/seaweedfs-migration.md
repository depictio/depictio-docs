---
title: "Upgrading to v1.12.0: MinIO to SeaweedFS"
icon: material/swap-horizontal
description: "The bundled S3 store is SeaweedFS from v1.12.0 and starts empty. Who is affected, the renamed settings, and how to copy your data over with Docker Compose or Helm."
---

# Upgrading to v1.12.0: MinIO to SeaweedFS <small>(v1.12.0+)</small>

From v1.12.0 the S3 store bundled with Depictio is
[SeaweedFS](https://github.com/seaweedfs/seaweedfs) (`weed mini`, Apache-2.0)
instead of MinIO. MinIO's community edition stopped receiving releases in 2025
and its repository was archived in 2026, so the image Depictio pinned no longer
got security fixes.

!!! warning "The new store starts empty"
    SeaweedFS cannot read MinIO's on-disk layout. On upgrade, the bundled store
    writes to a new, empty `seaweedfs_data` volume, and your objects stay in the
    old `minio_data` volume until you copy them. Until then, dashboards show
    missing Delta tables and images. MongoDB is not touched, and object keys are
    the same on both sides, so copying the bucket is all it takes.

## Who is affected { #who-is-affected }

You need the copy below if you run the **bundled** store, with Docker Compose or
with the Helm chart, and it already holds data.

Nothing changes for you if:

- Depictio uses an **external S3** (AWS, NetApp, Ceph, your own MinIO, …), set
  with `DEPICTIO_S3_EXTERNAL_SERVICE=true` and `DEPICTIO_S3_PUBLIC_URL`, the
  `docker-compose.no-minio.yaml` file, or Helm `s3.enabled: false`. The legacy
  names `DEPICTIO_MINIO_*` and `minio.enabled: false` still work;
- this is a **fresh** install;
- you run [`depictio local up`](local.md), which used SeaweedFS from its first
  release.

## Renamed settings { #renamed-settings }

The settings are now named after S3 rather than after MinIO. **The old names
keep working**: a `DEPICTIO_MINIO_*` variable is read when its `DEPICTIO_S3_*`
counterpart is unset, the new name wins when both are set, and the server logs a
deprecation warning listing the old names it found.

| Before v1.12.0 | From v1.12.0 |
|----------------|--------------|
| `DEPICTIO_MINIO_ROOT_USER` | `DEPICTIO_S3_ROOT_USER` |
| `DEPICTIO_MINIO_ROOT_PASSWORD` | `DEPICTIO_S3_ROOT_PASSWORD` |
| `DEPICTIO_MINIO_BUCKET` | `DEPICTIO_S3_BUCKET` |
| `DEPICTIO_MINIO_PUBLIC_URL` | `DEPICTIO_S3_PUBLIC_URL` |
| `DEPICTIO_MINIO_EXTERNAL_SERVICE` | `DEPICTIO_S3_EXTERNAL_SERVICE` |
| `DEPICTIO_MINIO_VERIFY_TLS` | `DEPICTIO_S3_VERIFY_TLS` |
| `DEPICTIO_MINIO_EXTERNAL_HOST` / `_PORT` / `_PROTOCOL` | `DEPICTIO_S3_EXTERNAL_HOST` / `_PORT` / `_PROTOCOL` |
| `DEPICTIO_MINIO_SERVICE_NAME` / `_SERVICE_PORT` | `DEPICTIO_S3_SERVICE_NAME` / `_SERVICE_PORT` |
| Compose service `minio` | Compose service `s3`, with `minio` as a network alias |
| Compose port variables `MINIO_PORT` / `MINIO_CONSOLE_PORT` | `S3_PORT` / `S3_CONSOLE_PORT` |
| Helm `minio.*`, including `minio.env.DEPICTIO_MINIO_*` | Helm `s3.*`, with `s3.env.DEPICTIO_S3_*` |
| Helm `persistence.minio` | Helm `persistence.s3` |
| Helm `secrets.minioRootUser` / `secrets.minioRootPassword` | Helm `secrets.s3RootUser` / `secrets.s3RootPassword` |
| Helm `global.urlPattern.templates.minio` | Helm `global.urlPattern.templates.s3` |

- **CLI configurations** that point at `http://minio:9000` keep working, through
  the `minio` network alias of the `s3` service.
- **Helm**: a legacy `minio:` block, `persistence.minio`, `secrets.minioRoot*`
  and `global.urlPattern.templates.minio` are still merged in and render the
  same manifests, with a deprecation warning in the install and upgrade notes.
  The chart's ConfigMaps export both the `DEPICTIO_S3_*` and the
  `DEPICTIO_MINIO_*` variables, so a backend image older than v1.12.0 keeps
  working. The legacy copies will be dropped in a later release.
- **One exception, the development stack**: `docker-compose.dev.yaml` requires
  `DEPICTIO_S3_ROOT_USER` and `DEPICTIO_S3_ROOT_PASSWORD` under their new names
  in `docker-compose/.env`, since Compose cannot combine a fallback with a
  required variable.

The full list of storage settings is in the
[Environment Reference](env-reference.md#s3-storage).

## Still named `minio` on purpose { #still-named-minio }

Some names are part of live state, and renaming them would break an upgrade:

- Helm: the `<release>-minio` Deployment and Service, and their `app: minio`
  selector label. A Deployment selector cannot change, so `helm upgrade` would fail.
- Helm: the `<release>-minio-pvc` PVC. A new name would start the store on an
  empty volume.
- Helm: the `<release>-minio-ingress` and `<release>-minio-httproute` routes and
  the public host `<release>-minio.<domain>` (and `-minio.gw.`), which DNS
  records, TLS certificates and presigned URLs point at.
- Helm: the Secret keys `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD`, through which
  the chart reads back the generated password so it stays the same across upgrades.
- Compose: the backup-only `minio-backup` service, and the file names
  `docker-compose.backup-minio.yaml`, `docker-compose.no-minio.yaml` and
  `docker-compose.minio-legacy.yaml`.

## How the copy works

The old MinIO is started again next to the new store, on its untouched data, and
`scripts/migrate_minio_to_seaweedfs.py` copies the bucket from one to the other
through the S3 API. Both files are in the
[repository at `v1.12.0`](https://github.com/depictio/depictio/tree/v1.12.0), so
run the steps below from a clone of it. The script needs only `boto3`, which
`uv run` takes from the project.

| Option | Default | What it does |
|--------|---------|--------------|
| `--source-endpoint` | `http://127.0.0.1:9100` | The old MinIO: the side-car below, or a port-forward |
| `--target-endpoint` | `http://127.0.0.1:9000` | The new store |
| `--source-access-key` / `--source-secret-key` | `DEPICTIO_S3_ROOT_USER` / `DEPICTIO_S3_ROOT_PASSWORD`, else the `DEPICTIO_MINIO_ROOT_*` names | Credentials of the old store |
| `--target-access-key` / `--target-secret-key` | same | Credentials of the new store |
| `--bucket` | `DEPICTIO_S3_BUCKET`, else `depictio-bucket` | Bucket to copy; `--target-bucket` names another one on the target |
| `--dry-run` | | List what would be copied, copy nothing |
| `--skip-existing` | | Skip keys already on the target with the same size, to resume an interrupted copy |
| `--verify` | | Compare both listings after the copy |
| `--export-dir` / `--import-dir` | | Download the bucket into a directory, or upload a directory into it, instead of copying directly |

## Docker Compose { #docker-compose }

1. **Upgrade the stack.** Take the v1.12.0 `docker-compose.yaml`, pull and start
   it. The new store boots empty. `--remove-orphans` stops the old `minio`
   container, which the new file no longer declares; its volume stays.

    ```bash
    docker compose pull
    docker compose up -d --remove-orphans
    ```

2. **Start the old MinIO as a side-car** on its untouched data, published on
   `127.0.0.1:9100`:

    ```bash
    # Named-volume install (the root docker-compose.yaml)
    docker compose -f docker-compose.yaml \
      -f docker-compose/docker-compose.minio-legacy.yaml up -d minio-legacy

    # Bind-mount install (docker-compose.dev.yaml, data under ./data/minio_data)
    MINIO_LEGACY_DATA=./data/minio_data docker compose -f docker-compose.dev.yaml \
      -f docker-compose/docker-compose.minio-legacy.yaml up -d minio-legacy
    ```

    The development compose publishes the new store on `127.0.0.1:9000`. The root
    `docker-compose.yaml` does not publish it, so for that install either add a
    temporary override that maps `127.0.0.1:9000:9000` on the `s3` service, or run
    the script inside the backend container.

3. **Dry run, then copy and verify.** The credentials and the bucket are read
   from your `.env` (`docker-compose/.env` for the development stack):

    ```bash
    set -a; source .env; set +a
    uv run scripts/migrate_minio_to_seaweedfs.py --dry-run
    uv run scripts/migrate_minio_to_seaweedfs.py --verify
    ```

    If the copy is interrupted, run it again with `--skip-existing`.

4. **Check a dashboard**: its tables and images load.

5. **Remove the side-car**, then, once you are satisfied, the old data:

    ```bash
    docker compose -f docker-compose.yaml \
      -f docker-compose/docker-compose.minio-legacy.yaml rm -sf minio-legacy

    # Named volume
    docker volume rm "$(docker compose config --format json | jq -r .name)_minio_data"
    # Bind mount
    rm -rf ./data/minio_data
    ```

!!! tip "Rolling back"
    Go back to the previous release's compose files. The `minio_data` volume is
    untouched until you remove it in step 5.

## Helm { #helm }

The chart keeps the `<release>-minio` Deployment, Service and PVC names, so the
upgrade reuses the same PVC. That PVC is `ReadWriteOnce`: the old MinIO pod and
the new SeaweedFS pod cannot mount it at the same time, so the copy goes in two
hops through a local directory.

```bash
# 1. BEFORE upgrading, while MinIO still runs: export the bucket
kubectl port-forward svc/<release>-minio 9100:9000 &
uv run scripts/migrate_minio_to_seaweedfs.py \
  --source-access-key "$(kubectl get secret <release>-depictio-secrets -o jsonpath='{.data.MINIO_ROOT_USER}' | base64 -d)" \
  --source-secret-key "$(kubectl get secret <release>-depictio-secrets -o jsonpath='{.data.MINIO_ROOT_PASSWORD}' | base64 -d)" \
  --export-dir ./s3-export

# 2. Upgrade the chart: SeaweedFS starts on the same PVC and ignores MinIO's files
helm upgrade <release> ./helm-charts/depictio -f values.yaml

# 3. Import into the new store
kubectl port-forward svc/<release>-minio 9000:9000 &
uv run scripts/migrate_minio_to_seaweedfs.py \
  --target-endpoint http://127.0.0.1:9000 \
  --target-access-key "$(kubectl get secret <release>-depictio-secrets -o jsonpath='{.data.MINIO_ROOT_USER}' | base64 -d)" \
  --target-secret-key "$(kubectl get secret <release>-depictio-secrets -o jsonpath='{.data.MINIO_ROOT_PASSWORD}' | base64 -d)" \
  --import-dir ./s3-export --verify

# 4. Reclaim the space MinIO's old layout uses on the PVC
kubectl exec deploy/<release>-minio -- sh -c 'rm -rf /data/.minio.sys /data/depictio-bucket'
```

With a second bucket on an external S3, you can copy there first
(`--target-endpoint https://…`) and import from it after the upgrade, instead of
going through a local directory.

!!! tip "Rolling back"
    Keep `./s3-export` until the new store is checked: it is a full copy of the
    bucket, taken before the upgrade touched anything.

## Notes on the new store

- The S3 API stays on port 9000. WebDAV is off.
- The SeaweedFS admin UI is off in the root compose file and in the Helm chart
  (`s3.adminUI.enabled`, port `s3.service.adminPort`). The development compose
  serves it on `127.0.0.1:9001`, the former MinIO console port. Where it is on,
  it asks for the root access and secret keys.
- The root credentials are applied again from the environment at every start, so
  changing `DEPICTIO_S3_ROOT_*` and restarting rotates them, as with MinIO.
- The health check is `GET http://<host>:9000/healthz`, instead of
  `/minio/health/live`.
- For very large object counts, pass `-volume.index=leveldb` through Helm
  `s3.extraArgs` to move the volume index out of memory.
