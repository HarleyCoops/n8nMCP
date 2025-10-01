"""MCP server definition that exposes n8n workflow management tools."""

from __future__ import annotations

import json
from contextlib import asynccontextmanager
from typing import Any, Dict, Tuple

from pydantic import BaseModel

from mcp import types
from mcp.server.lowlevel import Server

from .client import N8nClient, N8nError
from .config import N8nSettings, SettingsError
from .schemas import (
    CreateWorkflowInput,
    DeleteWorkflowInput,
    GetWorkflowInput,
    ListWorkflowsInput,
    ListWorkflowsOutput,
    ToggleWorkflowInput,
    UpdateWorkflowInput,
    WorkflowEnvelope,
    WorkflowSummary,
)


SERVER_NAME = "n8n-mcp"
SERVER_VERSION = "0.1.0"
SERVER_INSTRUCTIONS = (
    "Use these tools to inspect and manage workflows in the connected n8n instance. "
    "All tools return both human-readable text and structured JSON."
)


@asynccontextmanager
async def _lifespan(_: Server):
    """Create the shared n8n client used by every tool call."""

    try:
        settings = N8nSettings.load()
    except SettingsError as exc:  # pragma: no cover - surfaced to the client
        raise RuntimeError(f"Failed to load settings: {exc}") from exc

    async with N8nClient(settings) as client:
        yield {"client": client, "settings": settings}


def _pretty(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True)


def _text(message: str) -> types.TextContent:
    return types.TextContent(type="text", text=message)


def _tool_schema(model: type[BaseModel]) -> Dict[str, Any]:
    return model.model_json_schema()


def _unwrap_workflow(response: Dict[str, Any]) -> Dict[str, Any]:
    if "data" in response and isinstance(response["data"], dict):
        return response["data"]
    return response


def _unwrap_list(response: Dict[str, Any]) -> Tuple[list[Dict[str, Any]], int | None]:
    workflows = response.get("data")
    if not isinstance(workflows, list):
        workflows = response.get("workflows")
    if not isinstance(workflows, list):
        workflows = []
    count = response.get("count") or response.get("total")
    if isinstance(count, str) and count.isdigit():
        count = int(count)
    if count is None:
        count = len(workflows)
    return workflows, count


def build_server() -> Server:
    """Instantiate and configure the MCP server."""

    server = Server(
        SERVER_NAME,
        version=SERVER_VERSION,
        instructions=SERVER_INSTRUCTIONS,
        lifespan=_lifespan,
    )

    @server.list_tools()
    async def _list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="n8n_list_workflows",
                title="List workflows",
                description="Retrieve the workflows visible to the authenticated user.",
                inputSchema=_tool_schema(ListWorkflowsInput),
                outputSchema=_tool_schema(ListWorkflowsOutput),
            ),
            types.Tool(
                name="n8n_get_workflow",
                title="Fetch workflow",
                description="Return the full JSON definition for a workflow ID.",
                inputSchema=_tool_schema(GetWorkflowInput),
                outputSchema=_tool_schema(WorkflowEnvelope),
            ),
            types.Tool(
                name="n8n_create_workflow",
                title="Create workflow",
                description="Create a new workflow, optionally activating it immediately.",
                inputSchema=_tool_schema(CreateWorkflowInput),
                outputSchema=_tool_schema(WorkflowEnvelope),
            ),
            types.Tool(
                name="n8n_update_workflow",
                title="Update workflow",
                description="Update an existing workflow by ID.",
                inputSchema=_tool_schema(UpdateWorkflowInput),
                outputSchema=_tool_schema(WorkflowEnvelope),
            ),
            types.Tool(
                name="n8n_toggle_workflow",
                title="Toggle workflow",
                description="Activate or deactivate a workflow.",
                inputSchema=_tool_schema(ToggleWorkflowInput),
                outputSchema=_tool_schema(WorkflowEnvelope),
            ),
            types.Tool(
                name="n8n_delete_workflow",
                title="Delete workflow",
                description="Remove a workflow by ID.",
                inputSchema=_tool_schema(DeleteWorkflowInput),
                outputSchema={"type": "object", "properties": {"success": {"type": "boolean"}}},
            ),
        ]

    @server.call_tool()
    async def _call_tool(tool_name: str, arguments: Dict[str, Any]):
        context = server.request_context.lifespan_context
        client: N8nClient = context["client"]

        if tool_name == "n8n_list_workflows":
            params = ListWorkflowsInput.model_validate(arguments)
            response = await client.list_workflows(search=params.search, limit=params.limit)
            workflows, count = _unwrap_list(response)
            structured = ListWorkflowsOutput(
                workflows=[WorkflowSummary.model_validate(wf) for wf in workflows],
                count=count,
            ).model_dump(exclude_none=True)
            summary_items = [
                f"- {wf.get('id')}: {wf.get('name')}"
                + (" (active)" if wf.get('active') else " (inactive)")
                for wf in workflows
            ]
            if not summary_items:
                summary_items.append('(no workflows found)')
            summary_lines = ['n8n workflows:', *summary_items]
            return ([
                _text("\n".join(summary_lines)),
                _text(_pretty(structured)),
            ], structured)

        if tool_name == "n8n_get_workflow":
            params = GetWorkflowInput.model_validate(arguments)
            response = await client.get_workflow(params.workflow_id)
            workflow = _unwrap_workflow(response)
            structured = WorkflowEnvelope(workflow=workflow).model_dump()
            return ([_text(_pretty(workflow))], structured)

        if tool_name == "n8n_create_workflow":
            params = CreateWorkflowInput.model_validate(arguments)
            payload = params.model_dump(exclude={"activate", "overwrite_by_name"}, exclude_none=True)
            updated = None

            if params.overwrite_by_name:
                existing = await client.find_workflow_by_name(params.name)
                if existing:
                    workflow_id = existing.get("id")
                    if workflow_id is None:
                        raise N8nError("Existing workflow does not expose an ID")
                    updated = await client.update_workflow(workflow_id, payload)
                    result = _unwrap_workflow(updated)
                else:
                    created = await client.create_workflow(payload)
                    result = _unwrap_workflow(created)
            else:
                created = await client.create_workflow(payload)
                result = _unwrap_workflow(created)

            workflow_id = result.get("id")
            if params.activate and workflow_id is not None:
                await client.activate_workflow(workflow_id)
                result["active"] = True

            structured = WorkflowEnvelope(workflow=result).model_dump()
            action = "updated" if updated else "created"
            message = f"Workflow {result.get('name')} ({result.get('id')}) {action}."
            return ([_text(message), _text(_pretty(result))], structured)

        if tool_name == "n8n_update_workflow":
            params = UpdateWorkflowInput.model_validate(arguments)
            payload = params.model_dump(exclude_none=True, exclude={"workflow_id", "activate"})
            if not payload:
                raise N8nError("No update fields were provided.")
            response = await client.update_workflow(params.workflow_id, payload)
            workflow = _unwrap_workflow(response)
            if params.activate is not None:
                if params.activate:
                    await client.activate_workflow(params.workflow_id)
                    workflow["active"] = True
                else:
                    await client.deactivate_workflow(params.workflow_id)
                    workflow["active"] = False
            structured = WorkflowEnvelope(workflow=workflow).model_dump()
            message = f"Workflow {params.workflow_id} updated."
            return ([_text(message), _text(_pretty(workflow))], structured)

        if tool_name == "n8n_toggle_workflow":
            params = ToggleWorkflowInput.model_validate(arguments)
            if params.activate:
                response = await client.activate_workflow(params.workflow_id)
                status = "activated"
            else:
                response = await client.deactivate_workflow(params.workflow_id)
                status = "deactivated"
            workflow = _unwrap_workflow(response)
            workflow["active"] = params.activate
            structured = WorkflowEnvelope(workflow=workflow).model_dump()
            message = f"Workflow {params.workflow_id} {status}."
            return ([_text(message), _text(_pretty(workflow))], structured)

        if tool_name == "n8n_delete_workflow":
            params = DeleteWorkflowInput.model_validate(arguments)
            await client.delete_workflow(params.workflow_id)
            structured = {"success": True, "workflow_id": params.workflow_id}
            message = f"Workflow {params.workflow_id} deleted."
            return ([_text(message)], structured)

        raise N8nError(f"Unknown tool: {tool_name}")

    return server
