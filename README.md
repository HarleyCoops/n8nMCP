# n8n Docker Installation on Windows 11

This guide provides steps to install and run n8n locally using Docker Desktop on Windows 11, based on the provided transcript.

## Prerequisites

*   **Windows 11:** These instructions are tailored for Windows 11.
*   **Docker Desktop:** You need Docker Desktop installed and running.

## Installation Steps

1.  **Install Docker Desktop:**
    *   Go to the [official Docker website](https://www.docker.com/products/docker-desktop/).
    *   Download the Docker Desktop installer for Windows.
    *   Run the installer. It might require enabling WSL 2 (Windows Subsystem for Linux) or Hyper-V features. Follow the prompts during installation.
    *   Restart your computer if prompted.
    *   Launch Docker Desktop from the Start Menu and wait for it to show the "Docker Desktop is running" status in the system tray.

2.  **Pull the n8n Docker Image:**
    *   Open Docker Desktop.
    *   In the search bar at the top, type `n8n`.
    *   Find the official `docker.io/n8nio/n8n` image and click on it.
    *   Click the "Pull" button and select the `latest` tag (or a specific version if needed).
    *   Wait for the image download to complete.

3.  **Create and Run the n8n Container:**
    *   Navigate to the "Images" section in Docker Desktop (usually on the left sidebar).
    *   Locate the `n8nio/n8n` image you just pulled.
    *   Click the "Run" button next to the image.
    *   **Optional Settings (Click to expand):**
        *   **Container Name:** Give your container a recognizable name, e.g., `n8n-instance`.
        *   **Ports:**
            *   Set the **Host Port** to `5678`. This is the port you'll use to access n8n in your browser.
            *   The **Container Port** should automatically be `5678`.
        *   **Volumes (Crucial for Data Persistence):**
            *   Click on "Volumes".
            *   **Host Path:** Choose a folder on your Windows machine where n8n data (workflows, credentials) will be saved. For example: `C:\Users\YourUsername\Documents\n8n-data`. Create this folder if it doesn't exist.
            *   **Container Path:** Enter `/home/node/.n8n`. This is the standard path inside the container where n8n stores its data.
        *   **Environment Variables:**
            *   Click on "Environment Variables".
            *   If you plan to use Community Nodes or specific features mentioned in the transcript (like MCP), you might need to add variables. See the `.env.example` file or the n8n documentation for common variables. For example, to allow external command execution (use with caution):
                *   Variable: `NODE_FUNCTION_ALLOW_EXTERNAL`
                *   Value: `n8n-nodes-base.executeCommand,n8n-nodes-base.httpRequest`
            *   You can also manage environment variables using a `.env` file (see below).

    *   Click the "Run" button to create and start the container.

4.  **Verify Installation and Access n8n:**
    *   Go to the "Containers" section in Docker Desktop. You should see your `n8n-instance` container running.
    *   Wait a minute for n8n to initialize.
    *   Open your web browser (like Chrome, Edge, or Firefox).
    *   Navigate to `http://localhost:5678`.
    *   You should see the n8n "Set up owner" screen.
    *   Create your owner account by providing a username, email, and password.
    *   Follow the on-screen prompts to complete the setup.

You now have a local n8n instance running on Docker!

## Using `.env` for Configuration (Recommended)

Instead of setting environment variables directly in Docker Desktop, you can use a `.env` file placed in your project directory (`C:\Users\chris\N8Nmcp`).

1.  Create a file named `.env` in your project root.
2.  Add environment variables like:
    ```dotenv
    # .env file
    # See https://docs.n8n.io/hosting/environment-variables/
    
    # Example: Set timezone
    GENERIC_TIMEZONE=America/New_York 
    
    # Example: Allow specific community node external access (use with caution)
    # NODE_FUNCTION_ALLOW_EXTERNAL=n8n-nodes-base.executeCommand
    
    # Example: Brave Search API Key (if using the MCP Brave Search node)
    # BRAVE_API_KEY=YOUR_BRAVE_API_KEY_HERE 
    ```
3.  When running the container from the command line (using `docker run`), you can pass the `.env` file using the `--env-file` flag:
    ```bash
    docker run -d --name n8n-instance -p 5678:5678 -v C:\Users\YourUsername\Documents\n8n-data:/home/node/.n8n --env-file .env n8nio/n8n
    ```
    *(Replace the volume path with your chosen host path)*

    *Note: Docker Desktop's UI might not directly support `--env-file` in the simple "Run" interface. Using the command line offers more flexibility.*

## Stopping and Starting

*   **Stop:** In Docker Desktop > Containers, click the stop icon next to your `n8n-instance`.
*   **Start:** In Docker Desktop > Containers, click the start icon next to your `n8n-instance`. Your data will persist because of the volume mapping.

---

## Advanced: Integrate MCP and AI Agents in n8n

This section explains how to supercharge your n8n workflows with AI agents and the Model Context Protocol (MCP), enabling dynamic tool use and powerful automation.

### 1. Enable Community Nodes

- When configuring your container, add an environment variable:
  - **Name:** `N8N_COMMUNITY_NODES_ENABLED`
  - **Value:** `true`
- This allows installing community-contributed nodes like MCP.

### 2. Access n8n and Create an Account

- Open `http://localhost:5678` in your browser.
- Sign up with your email and password.
- Log in to access the n8n editor.

### 3. Install MCP Community Nodes

- In n8n, navigate to **Settings** > **Community Nodes**.
- Search for:
  - `n8n-nodes-mcp` (or similar MCP-related nodes).
- Click **Install** and wait for installation to complete.

### 4. Create a New Workflow

- Click **New Workflow**.
- Name it, e.g., `MCP Server Agent`.

### 5. Add a Chat Trigger Node

- Add the **Chat Trigger** node to start the workflow based on user input.

### 6. Add an AI Agent Node

- Add the **AI Agent** node connected after the Chat Trigger.
- Configure it to use **OpenAI Chat** model:
  - Create a new credential with your OpenAI API key.
  - Select model (e.g., `gpt-4o-mini`).
- Optionally, add a **Simple Memory** node to maintain conversation context.

### 7. Integrate MCP Client Nodes

- Add an **MCP Client** node.
- Use it to **list available tools** from an MCP server.
- Provide necessary credentials or command-line arguments to connect to your MCP server.
- Example: Connect to a Brave Search MCP server (requires Brave API key).

### 8. Obtain and Configure API Keys

- For Brave Search:
  - Sign up at Brave Search API portal.
  - Generate an API key.
  - Add it to your MCP server credentials or environment variables.

### 9. Connect MCP Nodes to AI Agent

- Add another **MCP Client** node to **execute** a selected tool.
- Configure the AI Agent node to dynamically select and use these tools.
- Set the operation to **Execute Tool** and specify the tool name or let the AI choose.

### 10. Define System Message

- In the AI Agent node, add a system prompt like:
  > You are a helpful assistant utilizing Brave Search to perform web queries.

### 11. Connect All Nodes

- Ensure Chat Trigger → AI Agent → MCP Client(s) → AI Agent (response) are properly connected for smooth data flow.

### 12. Test Your Workflow

- Open the chat interface.
- Ask questions like "Find Italian restaurants nearby."
- The AI agent will decide which tool to use, perform the search, and return results.

### 13. How It Works (Summary)

- User sends a message.
- AI agent interprets and decides which tool (via MCP) to use.
- MCP client connects to external APIs (e.g., Brave Search).
- Results are fetched and passed back to the AI agent.
- AI agent formulates a user-friendly response.

---

By following these steps, you can build advanced AI-powered workflows in n8n that dynamically leverage external tools via MCP, enabling powerful automation with minimal manual coding.

## n8n MCP Server

A standalone MCP server for managing n8n workflows from Claude Code lives in [`mcp_n8n/`](mcp_n8n/).
The directory contains exhaustive setup instructions, configuration samples, and Python source code for
the server. Follow that guide after your Docker instance is running to register the tool with Claude Code.
