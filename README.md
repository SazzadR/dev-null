# Open WebUI with an authenticated image-generation MCP server

This project runs [Open WebUI](https://openwebui.com/) in Docker with OpenAI as
the default chat and image provider. A custom MCP server exposes an authenticated
`generate_image` tool and returns generated PNG images directly to conversations.

Ollama is available as an optional local chat provider for NVIDIA GPU machines.
It is not part of the default startup.

## Quick links

- [Quick start with OpenAI](#quick-start-with-openai)
- [How the image tool connects](#how-the-image-tool-connects)
- [Verification](#verification)
- [Optional Ollama with an NVIDIA GPU](#optional-ollama-with-an-nvidia-gpu)
- [Troubleshooting](#troubleshooting)
- [Operations and production](#operations-and-production)

## Architecture

```text
Browser
   |
   v
Open WebUI :3000 ---------------------> OpenAI API
   |
   | Authorization: Bearer <IMAGE_MCP_API_KEY>
   v
Image MCP :8000 ----------------------> OpenAI Images API

Optional NVIDIA GPU profile:
Open WebUI ---------------------------> Ollama :11434
```

Only Open WebUI is published to the host, on `127.0.0.1:3000`. The MCP server
and optional Ollama service remain on the private Docker network.

## Project structure

```text
.
├── compose.yaml              # Services, networking, volumes, and MCP registration
├── .env.example              # Credential and runtime configuration template
├── config/
│   ├── ollama.env            # Optional Ollama runtime settings
│   └── openwebui.env         # Open WebUI provider configuration
└── image-mcp/
    ├── Dockerfile
    ├── requirements.txt
    └── server.py             # Authenticated image-generation MCP server
```

## Prerequisites

- Docker Engine with the Docker Compose plugin.
- An [OpenAI API key](https://platform.openai.com/api-keys) with access to chat
  models and the configured image model.

The optional Ollama setup also requires an NVIDIA GPU, a working NVIDIA driver,
and the NVIDIA Container Toolkit.

## Quick start with OpenAI

### 1. Configure the environment

Copy the template and generate two different secrets:

```sh
cp .env.example .env
openssl rand -hex 32
openssl rand -hex 32
```

Complete every required value in `.env`:

```dotenv
WEBUI_SECRET_KEY=<first-generated-secret>
WEBUI_ADMIN_EMAIL=admin@example.com
WEBUI_ADMIN_PASSWORD=<strong-unique-admin-password>

OPENAI_API_KEY=<your-openai-api-key>
IMAGE_MCP_API_KEY=<second-generated-secret>

ENABLE_OPENAI_API=True
ENABLE_OLLAMA_API=False
OPENAI_IMAGE_MODEL=gpt-image-2.5-flare
```

Create `OPENAI_API_KEY` on the [OpenAI API key page](https://platform.openai.com/api-keys).
It enables OpenAI chat models in Open WebUI and image generation in the MCP
server. `WEBUI_SECRET_KEY` signs Open WebUI sessions; `IMAGE_MCP_API_KEY` is the
shared bearer token between Open WebUI and the MCP server.

### Initial administrator

There is no hardcoded administrator email or password. On the first startup,
Open WebUI creates the administrator from `WEBUI_ADMIN_EMAIL` and
`WEBUI_ADMIN_PASSWORD`; `admin@example.com` above is only an example. The
account is stored in `open-webui-data`, so changing `.env` later does not reset
an existing account or password.

The root `.env` file is excluded from Git. Never commit real credentials.

### 2. Start the stack

```sh
docker compose config --quiet
docker compose up -d --build
docker compose ps
```

The default startup runs `open-webui` and `image-generation-mcp`. It does not
start Ollama.

### 3. Generate an image

Open [http://localhost:3000](http://localhost:3000), sign in with the admin
credentials from `.env`, and select an OpenAI chat model. For example, ask:

```text
Generate an image of a small red sailboat under a starry sky in watercolor style.
```

The model can call the **Image Generation** tool, which returns the generated
image to the conversation. OpenAI API usage may incur charges.

## How the image tool connects

Open WebUI registers the MCP connection from `TOOL_SERVER_CONNECTIONS` in
`compose.yaml` and calls:

```text
http://image-generation-mcp:8000/mcp
```

The connection uses Streamable HTTP in stateless mode and `auth_type: bearer`.
Open WebUI sends `IMAGE_MCP_API_KEY` in the `Authorization` header; the server
compares it in constant time and returns HTTP `401` for a missing or incorrect
token. The `generate_image` tool validates the prompt, calls
`OPENAI_IMAGE_MODEL`, and returns MCP `ImageContent` with MIME type `image/png`.

Default model metadata attaches `server:mcp:image_generation` to available
models, so no manual MCP registration is needed in the Open WebUI interface.

## Verification

Follow the MCP logs while submitting an image request:

```sh
docker compose ps
docker compose logs -f image-generation-mcp
```

A successful request logs `generate_image received model=...` followed by
`Image generated with model=...`. The setup works end to end when:

1. `open-webui` and `image-generation-mcp` are healthy.
2. OpenAI chat models and the Image Generation tool are available.
3. An image request displays the returned PNG.

## Optional Ollama with an NVIDIA GPU

Use this profile to run chat models locally. Image generation still uses OpenAI
through the authenticated MCP server.

<details>
<summary><strong>Ubuntu NVIDIA Container Toolkit installation</strong></summary>

These steps assume Docker, Docker Compose, and an NVIDIA driver are installed.
First confirm that the driver works:

```sh
nvidia-smi
```

Add NVIDIA's repository and install the toolkit:

```sh
sudo apt-get update
sudo apt-get install -y --no-install-recommends ca-certificates curl gnupg2

curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list > /dev/null

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Verify container access to the GPU:

```sh
sudo docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
```

See NVIDIA's [Container Toolkit installation guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation)
for current package details.

</details>

Set `ENABLE_OLLAMA_API=True` in `.env`, then start the optional profile:

```sh
docker compose --profile local-llm up -d --build
```

Models are not downloaded automatically. Pull `llama3.2:1b` as a small example:

```sh
docker compose --profile local-llm exec ollama ollama pull llama3.2:1b
docker compose --profile local-llm exec ollama ollama list
```

Refresh Open WebUI and select `llama3.2:1b`. The model persists in the
`ollama-data` volume.

> **Small-model limitations:** `llama3.2:1b` uses little GPU memory but is less
> reliable for reasoning, complex instructions, and tool calls. It is text-only
> and cannot understand uploaded or generated images. Ollama can run compatible
> vision models when the host has enough GPU memory.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| **Open WebUI Backend Required** | Run `docker compose ps`. If the services are healthy after an image update, clear the browser's site data for `localhost:3000` and reload. |
| **No OpenAI models** | Confirm `ENABLE_OPENAI_API=True` and a valid `OPENAI_API_KEY`, then run `docker compose up -d --force-recreate open-webui`. |
| **No Ollama model** | Run the `local-llm` profile, pull `llama3.2:1b`, and refresh the model list. |
| **Image generation fails** | Check the OpenAI key, model access, API credit, and `docker compose logs --tail=100 image-generation-mcp`. |
| **MCP returns 401** | Ensure both services use the same `IMAGE_MCP_API_KEY`, then recreate `image-generation-mcp` and `open-webui`. |

## Operations and production

Update the default stack with `docker compose up -d --build`. Include
`--profile local-llm` when the deployment uses Ollama.

Stop the default stack with `docker compose down`, or stop the Ollama setup with
`docker compose --profile local-llm down`. Both commands preserve volumes. Do
not add `-v` unless you intend to delete Open WebUI data and downloaded models.

For production, pin image versions, place Open WebUI behind an HTTPS reverse
proxy, inject credentials from a managed secret store, restrict network access,
monitor the services, and back up `open-webui-data`.
