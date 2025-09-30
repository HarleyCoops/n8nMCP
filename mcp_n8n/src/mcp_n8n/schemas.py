"""Pydantic models shared by the MCP tools."""

from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field


class WorkflowConnection(BaseModel):
    """Represents a single connection between workflow nodes."""

    model_config = ConfigDict(extra="allow")

    node: str = Field(..., description="Name of the node being connected to.")
    type: str | None = Field(
        default=None,
        description="Optional n8n connection type (usually 'main').",
    )
    index: int | None = Field(
        default=None,
        description="Optional connection index when a node exposes multiple outputs.",
    )


class WorkflowNode(BaseModel):
    """Minimal node definition required by the n8n API."""

    model_config = ConfigDict(extra="allow")

    id: str = Field(..., description="Unique node ID from the n8n editor.")
    name: str = Field(..., description="Human readable name displayed in the editor.")
    type: str = Field(..., description="Node type, e.g. 'n8n-nodes-base.httpRequest'.")
    typeVersion: float = Field(  # noqa: N815 - n8n uses camelCase
        default=1,
        description="Node version as required by n8n.",
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters field copied from the n8n JSON export.",
    )
    position: Dict[str, float] = Field(
        default_factory=dict,
        description="Canvas coordinates for the node.",
    )
    credentials: Dict[str, Any] | None = Field(
        default=None,
        description="Optional credential attachments.",
    )


class WorkflowDefinition(BaseModel):
    """Convenience wrapper for the payload expected by the n8n workflows API."""

    model_config = ConfigDict(extra="allow")

    name: str = Field(..., description="Workflow name shown in the sidebar.")
    nodes: List[WorkflowNode] = Field(
        default_factory=list,
        description="Nodes making up the workflow. Copy directly from n8n's JSON export when unsure.",
    )
    connections: Dict[str, Dict[str, List[WorkflowConnection]]] = Field(
        default_factory=dict,
        description="Connection graph describing how nodes link together.",
    )
    settings: Dict[str, Any] | None = Field(
        default=None,
        description="Optional workflow-level settings map.",
    )
    tags: List[str] | None = Field(
        default=None,
        description="Optional list of tag names to attach to the workflow.",
    )


class ListWorkflowsInput(BaseModel):
    """Input schema for listing workflows."""

    search: str | None = Field(
        default=None,
        description="Optional substring filter that matches workflow names.",
    )
    limit: int | None = Field(
        default=None,
        ge=1,
        le=250,
        description="Maximum number of workflows to return.",
    )


class GetWorkflowInput(BaseModel):
    workflow_id: int = Field(..., description="Numeric ID of the workflow to retrieve.")


class CreateWorkflowInput(WorkflowDefinition):
    activate: bool = Field(
        default=False,
        description="Immediately activate the workflow after creation.",
    )
    overwrite_by_name: bool = Field(
        default=False,
        description="If a workflow with the same name exists, update it instead of creating a duplicate.",
    )


class UpdateWorkflowInput(BaseModel):
    workflow_id: int = Field(..., description="Numeric ID of the workflow to update.")
    name: str | None = Field(
        default=None,
        description="New workflow name.",
    )
    nodes: List[WorkflowNode] | None = Field(
        default=None,
        description="Updated node list.",
    )
    connections: Dict[str, Dict[str, List[WorkflowConnection]]] | None = Field(
        default=None,
        description="Updated connection graph.",
    )
    settings: Dict[str, Any] | None = Field(
        default=None,
        description="Updated workflow settings.",
    )
    tags: List[str] | None = Field(
        default=None,
        description="Updated tags.",
    )
    activate: bool | None = Field(
        default=None,
        description="If provided, toggles the workflow active flag after the update.",
    )


class ToggleWorkflowInput(BaseModel):
    workflow_id: int = Field(..., description="Numeric ID of the workflow to toggle.")
    activate: bool = Field(..., description="True to activate, False to deactivate.")


class DeleteWorkflowInput(BaseModel):
    workflow_id: int = Field(..., description="Numeric ID of the workflow to remove.")


class WorkflowSummary(BaseModel):
    """Subset of workflow fields returned for listings."""

    model_config = ConfigDict(extra="allow")

    id: int
    name: str
    active: bool | None = None


class ListWorkflowsOutput(BaseModel):
    model_config = ConfigDict(extra="allow")

    workflows: List[WorkflowSummary]
    count: int | None = Field(
        default=None,
        description="Optional total count returned by n8n.",
    )


class WorkflowEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    workflow: Dict[str, Any]
