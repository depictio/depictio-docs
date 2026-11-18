<!-- Hand-written, included in usage.md by scripts/cli-reference/render.py. Links are relative to usage.md. -->

## Which server a command uses { #choosing-a-server }

Every command that talks to a server takes `--server`: `local` for the server [`local up`](#local-up) runs, or a CLI configuration file. Without it, the command uses, in order:

1. `$DEPICTIO_CLI_CONFIG_PATH` (a file, or `local`);
2. `~/.depictio/CLI.yaml`, if it exists;
3. the local server, unless `DEPICTIO_CLI_TOKEN` or `DEPICTIO_CLI_API_BASE_URL` is set.

The rule never checks whether a local server runs. Each command first prints the server it reaches.

### Environment variables { #environment-variables }

| Variable | Effect |
| --- | --- |
| `DEPICTIO_CLI_CONFIG_PATH` | Configuration used without `--server` |
| `DEPICTIO_CLI_TOKEN` | Replaces the file's token |
| `DEPICTIO_CLI_API_BASE_URL` | Replaces the file's `api_base_url` |

The last two never apply to `--server local` or `migrate --to-server`.
