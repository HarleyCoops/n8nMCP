"""Async client helpers for the n8n REST API."""

from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from .config import N8nSettings


class N8nError(RuntimeError):
    """Raised when an HTTP call to n8n fails."""


class N8nClient:
    """Lightweight async wrapper around the n8n REST API."""

    def __init__(self, settings: N8nSettings) -> None:
        self._settings = settings
        self._client = httpx.AsyncClient(**settings.httpx_kwargs())

    async def __aenter__(self) -> "N8nClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        await self.close()

    async def close(self) -> None:
        await self._client.aclose()

    async def list_workflows(
        self,
        *,
        search: str | None = None,
        limit: int | None = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if search:
            params["filter[search]"] = search
        if limit is not None:
            params["limit"] = limit
        return await self._request("GET", "/rest/workflows", params=params)

    async def get_workflow(self, workflow_id: int | str) -> Dict[str, Any]:
        return await self._request("GET", f"/rest/workflows/{workflow_id}")

    async def create_workflow(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/rest/workflows", json=payload)

    async def update_workflow(self, workflow_id: int | str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("PATCH", f"/rest/workflows/{workflow_id}", json=payload)

    async def delete_workflow(self, workflow_id: int | str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/rest/workflows/{workflow_id}")

    async def activate_workflow(self, workflow_id: int | str) -> Dict[str, Any]:
        return await self._request("POST", f"/rest/workflows/{workflow_id}/activate")

    async def deactivate_workflow(self, workflow_id: int | str) -> Dict[str, Any]:
        return await self._request("POST", f"/rest/workflows/{workflow_id}/deactivate")

    async def find_workflow_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        response = await self.list_workflows(search=name, limit=50)
        workflows = response.get("data") or response.get("workflows") or []
        for workflow in workflows:
            if isinstance(workflow, dict) and workflow.get("name") == name:
                return workflow
        return None

    async def _request(self, method: str, url: str, **kwargs: Any) -> Dict[str, Any]:
        try:
            response = await self._client.request(method, url, **kwargs)
        except httpx.HTTPError as exc:  # pragma: no cover - network failures are runtime issues
            raise N8nError(str(exc)) from exc

        if response.is_error:
            message = response.text
            try:
                error_json = response.json()
                message = error_json.get("message", message)
            except ValueError:
                pass
            raise N8nError(f"{response.status_code}: {message}")

        try:
            return response.json()
        except ValueError:
            raise N8nError("n8n returned a non-JSON response")
