"""Configuration loading for the n8n MCP server."""

from __future__ import annotations

import os
from typing import Any, Dict, Tuple

from pydantic import AnyHttpUrl, Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsError(RuntimeError):
    """Raised when configuration cannot be loaded."""


class N8nSettings(BaseSettings):
    """Settings required to talk to the n8n REST API."""

    base_url: AnyHttpUrl = Field(
        default="http://localhost:5678",
        description="Root URL of the n8n instance (e.g. http://localhost:5678).",
    )
    api_key: str | None = Field(
        default=None,
        description="Optional n8n API key used for authentication.",
    )
    username: str | None = Field(
        default=None,
        description="Optional basic-auth username (used only when password is supplied).",
    )
    password: str | None = Field(
        default=None,
        description="Optional basic-auth password (used only when username is supplied).",
    )
    verify_ssl: bool = Field(
        default=True,
        description="Toggle TLS certificate verification when using HTTPS.",
    )
    timeout: float = Field(
        default=30.0,
        ge=1.0,
        le=300.0,
        description="Request timeout (seconds) for n8n API calls.",
    )
    extra_headers: Dict[str, str] = Field(
        default_factory=dict,
        description="Additional HTTP headers forwarded to the n8n API.",
    )

    model_config = SettingsConfigDict(
        env_prefix="N8N_MCP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    @property
    def auth(self) -> Tuple[str, str] | None:
        """Return an HTTP basic-auth tuple when username/password are configured."""

        if self.username and self.password:
            return self.username, self.password
        return None

    def headers(self) -> Dict[str, str]:
        """Construct default headers for requests to n8n."""

        headers: Dict[str, str] = {"Accept": "application/json"}
        if self.api_key:
            headers["X-N8N-API-KEY"] = self.api_key
        headers.update(self.extra_headers)
        return headers

    def httpx_kwargs(self) -> Dict[str, Any]:
        """Return keyword arguments commonly passed to ``httpx.AsyncClient``."""

        return {
            "base_url": str(self.base_url),
            "headers": self.headers(),
            "verify": self.verify_ssl,
            "timeout": self.timeout,
            "auth": self.auth,
        }

    @classmethod
    def load(cls) -> "N8nSettings":
        """Load settings from the environment, honouring legacy n8n variables."""

        overrides: Dict[str, Any] = {}

        # Allow reuse of existing n8n environment variables when dedicated ones are absent.
        if "N8N_MCP_API_KEY" not in os.environ:
            legacy_api_key = os.getenv("N8N_API_KEY")
            if legacy_api_key:
                overrides["api_key"] = legacy_api_key

        username_missing = "N8N_MCP_USERNAME" not in os.environ
        password_missing = "N8N_MCP_PASSWORD" not in os.environ
        if username_missing and password_missing:
            legacy_user = os.getenv("N8N_BASIC_AUTH_USER")
            legacy_password = os.getenv("N8N_BASIC_AUTH_PASSWORD")
            if legacy_user and legacy_password:
                overrides["username"] = legacy_user
                overrides["password"] = legacy_password

        try:
            return cls(**overrides)
        except ValidationError as exc:  # pragma: no cover - configuration errors are user facing
            raise SettingsError(str(exc)) from exc
