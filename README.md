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