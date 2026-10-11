# Service configuration

- `openwebui.env`: provider connections, image MCP registration, model capabilities, and the default system prompt.
- `ollama.env`: Ollama runtime settings.
- Root `.env`: private credentials and local options listed in `.env.example`.

Compose loads the service files through `env_file`. It reads the root `.env` for
`${...}` substitutions in `compose.yaml`; only explicitly referenced values are
passed to containers. Variables in a service's `environment` section take
precedence over its `env_file` values.

Keep secrets out of this directory: these files are committed to Git. Use
single-quoted multiline strings for JSON settings. Escape an embedded single
quote as `\'`.

From the repository root, validate and apply changes:

```sh
docker compose config --quiet
docker compose up -d
```

Recreate containers with `up -d` after editing these files; a plain `restart`
does not reload container environment variables. Open WebUI's
`ENABLE_PERSISTENT_CONFIG=False` makes these settings authoritative over saved
UI settings.

## Applying the system prompt

This Open WebUI version does not insert `DEFAULT_MODEL_PARAMS.system` into
outgoing messages. Save the system prompt on each model instead:

1. Open **Settings > Admin > Models** and edit the model.
2. Under **Model Params**, edit **System Prompt**.
3. Click **Save & Update**, refresh the browser, and start a new chat.

Saved model settings persist in `open-webui-data`. No container restart is
needed after saving a model prompt.
