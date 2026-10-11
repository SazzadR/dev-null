"""MCP server that generates images through OpenAI's Images API."""

import logging
import os
import secrets

from mcp import types
from mcp.server import MCPServer
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from mcp.server.mcpserver.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings
from openai import OpenAI
from openai import OpenAIError
from pydantic import AnyHttpUrl


logger = logging.getLogger("image-generation-mcp")
logger.setLevel(logging.INFO)
MODEL = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2.5-flare")
RESOURCE_URL = "http://image-generation-mcp:8000/mcp"
AUTH_TOKEN = os.environ["IMAGE_MCP_API_KEY"]


class SharedSecretVerifier(TokenVerifier):
    """Authenticate the Open WebUI MCP client with a shared bearer token."""

    async def verify_token(self, token: str) -> AccessToken | None:
        if not secrets.compare_digest(token, AUTH_TOKEN):
            return None

        return AccessToken(
            token=token,
            client_id="open-webui",
            scopes=["image:generate"],
            resource=RESOURCE_URL,
        )


mcp = MCPServer(
    "Image Generation",
    instructions="Use the generate_image tool whenever the user asks to create, draw, generate, or edit an image.",
    token_verifier=SharedSecretVerifier(),
    auth=AuthSettings(
        issuer_url=AnyHttpUrl("http://image-generation-mcp:8000"),
        resource_server_url=AnyHttpUrl(RESOURCE_URL),
        required_scopes=["image:generate"],
        validate_token_resource=True,
    ),
)


@mcp.tool(name="generate_image", description="Generate an image from a text prompt.")
def generate_image(prompt: str) -> list[types.TextContent | types.ImageContent]:
    """Generate an image and return it as a displayable MCP image result."""
    logger.info("generate_image received model=%s prompt=%r", MODEL, prompt)

    if not prompt.strip():
        raise ToolError("The image prompt must not be empty.")
    if len(prompt) > 32000:
        raise ToolError("The image prompt must be 32,000 characters or fewer.")

    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ToolError("OPENAI_API_KEY is not configured for the image-generation service.")

    try:
        result = OpenAI(api_key=api_key).images.generate(
            model=MODEL,
            prompt=prompt,
            size="1024x1024",
            quality="medium",
            n=1,
        )
    except OpenAIError as error:
        logger.error("Image generation failed (%s).", type(error).__name__)
        raise ToolError(f"Image generation failed ({type(error).__name__}).") from error

    image_data = result.data[0].b64_json if result.data else None
    if not image_data:
        raise ToolError("Image generation returned no image data.")

    logger.info("Image generated with model=%s.", MODEL)

    return [
        types.TextContent(text="Generated image."),
        types.ImageContent(data=image_data, mimeType="image/png"),
    ]


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    security = TransportSecuritySettings(
        allowed_hosts=["image-generation-mcp", "image-generation-mcp:*"],
        allowed_origins=[],
    )
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
        stateless_http=True,
        json_response=True,
        transport_security=security,
    )
