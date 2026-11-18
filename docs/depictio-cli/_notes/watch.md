<!-- Hand-written, included in usage.md by scripts/cli-reference/render.py. Links are relative to usage.md. -->

A lock under `~/.depictio/state/` (`DEPICTIO_CLI_STATE_DIR`) allows one watcher or ingestion per project. Watchers show in the [Watchers pane](../usage/administration/monitoring.md#watchers). File events need the `watch` extra; without it, it only polls. An `s3://` `DATA_DIR` is ingested once, then the watcher exits 1: refresh remote data [from the server](../usage/projects/remote-data.md#refreshing-the-data).

### Running a watcher as a service { #running-a-watcher-as-a-service }

The repository ships [`deploy/depictio-watch@.service`](https://github.com/depictio/depictio/blob/main/deploy/depictio-watch@.service), a systemd unit reading `/etc/depictio/<project>.env`, and [`deploy/docker-compose.watcher.yaml`](https://github.com/depictio/depictio/blob/main/deploy/docker-compose.watcher.yaml), configured from [`deploy/.env.example`](https://github.com/depictio/depictio/blob/main/deploy/.env.example). Both need `DEPICTIO_CLI_CONFIG` and `DEPICTIO_PROJECT_CONFIG` (Compose also `DEPICTIO_DATA_ROOT`); `DEPICTIO_WATCH_*` variables set the options.

```bash
sudo systemctl enable --now depictio-watch@myproject
docker compose -f deploy/docker-compose.watcher.yaml up -d
```
