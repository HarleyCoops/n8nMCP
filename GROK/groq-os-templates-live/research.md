# Build with Groq OS Templates (Live)

## Objective
Capture the requirements to showcase the live "Build with Groq OS" templates. Provide instructions for deploying, customizing, and demoing the templates end-to-end.

## Key Questions
- What templates launched with the "Build with Groq OS" program and what are their target use cases?
- How do developers access and clone the templates (GitHub, Groq console, CLI)?
- What dependencies (SDK versions, environment variables) are required before running them?
- How do we adapt templates to highlight MCP + n8n integrations?

## Research Sources
- Groq OS documentation hub and template repository.
- Launch livestream or walkthrough recordings.
- Example deployments shared by the Groq community.

## Enablement Steps
1. **Template Inventory**
   - List each available template with description, tech stack, and prerequisites.
   - Note licensing terms or usage restrictions.
2. **Environment Setup**
   - Define standard dev environment (Python/Node versions, Docker, Groq CLI).
   - Document configuration of secrets (Groq API key, MCP endpoints).
3. **Customization Playbook**
   - Show how to swap the default model for a Groq-hosted option via configuration.
   - Provide guidance for embedding templates into n8n workflows.
4. **Demo Checklist**
   - Create a step-by-step script for presenting the template, including data prep and success criteria.
   - Identify telemetry to capture (latency dashboards, cost metrics).

## Expected Artifacts
- Template catalog spreadsheet.
- Environment bootstrap scripts or `.env.example` files.
- Demo script with presenter notes.
