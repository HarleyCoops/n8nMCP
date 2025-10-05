# Remote MCP on Eight Groq Models

## Objective
Document how to configure and demonstrate Groq's remote Model Context Protocol (MCP) gateway against eight distinct Groq-hosted models. Deliver a repeatable integration plan for our n8n MCP server.

## Key Questions
- Which Groq-hosted models currently expose MCP-compatible endpoints? (Target a representative mix of reasoning and instruction-tuned models.)
- What authentication flow does the Groq remote MCP use (API key vs OAuth)?
- How do we select the target model in the MCP session negotiation?
- Are there per-model throughput or token limits that impact demos?
- How do streaming responses behave across different models?

## Research Sources
- Groq developer changelog and model availability matrix.
- Official MCP specification and Groq's remote MCP announcement blog post.
- Groq API reference (especially sections covering MCP adapter configuration).
- Community forums or Discord updates that highlight production caveats.

## Setup & Demo Steps
1. **Provision access**
   - Request or verify Groq API credentials with MCP permissions.
   - Enable remote MCP in the Groq dashboard if toggles exist per workspace.
2. **Collect model identifiers**
   - List the eight target model IDs and confirm pricing/limits.
   - Record default context windows, supported modalities, and notable features.
3. **Configure n8n MCP server**
   - Update the MCP connector config to allow dynamic model selection (e.g., environment variable `GROQ_MODEL` with fallback).
   - Generate per-model test flows that call the Groq MCP endpoint.
4. **Run validation matrix**
   - For each model, send a standardized prompt and capture latency, output quality, and token usage.
   - Store results in a shared spreadsheet or Notion page to highlight differences.
5. **Demo preparation**
   - Create a short screen recording that shows swapping models from the MCP client UI.
   - Prepare talking points on when to choose each model (latency vs intelligence trade-offs).

## Expected Artifacts
- Model comparison table (CSV/Sheets).
- n8n MCP configuration snippets (JSON/YAML).
- Demo recording and annotated slides.
