# Example Arxiv papers MCP Server

## Overview

This is an MCP (Model Context Protocol) Server designed to provide AI assistants with access to arXiv academic papers. The server implements a clean architecture pattern with dependency injection and follows domain-driven design principles.

## Key Features

The server provides three main MCP capabilities:

🔧 Tools

* search_papers - Search for academic papers on arXiv by topic and store their metadata
* extract_info - Retrieve detailed information about specific papers by ID

📚 Resources

* papers://folders - List all available research topic directories
* papers://{topic} - Get comprehensive information about papers in a specific topic

💬 Prompts

* generate_search_prompt - Generate structured prompts for AI assistants to research academic topics

## Architecture

The project follows Clean Architecture principles with clear separation of concerns:

```ini
📁 src
├── 📁 mcp_server_papers
│   ├─ 📁 domain
│   │   ├── 📁 model
│   │   │   └── 📁 paper
│   │   │       └── 📁 gateway: Abstract repositories for tools, resources, and prompts
│   │   │           ├── 📄 paper_repository.py
│   │   │           ├── 📄 resource_repository.py
│   │   │           └── 📄 prompt_repository.py
│   │   └── 📁 usecase: Business logic for tools, resources, and prompts
│   │       ├── 📄 paper_usecase.py
│   │       ├── 📄 resource_usecase
│   │       └── 📄 prompt_usecase.py
├── 📁 infrastructure
│   ├── 📁 entry_points: MCP server bindings for tools, resources, prompts, and routes
│   │   ├── 📄 tools.py
│   │   ├── 📄 resources.py
│   │   ├── 📄 prompts.py
│   │   └── 📄 routes.py
│   ├── 📁 driven_adapters: arXiv API integration and file system operations
│   │   ├── 📁 prompts
│   │   |   └── 📄 papers.py
│   │   ├── 📁 local_files
│   │   |   └── 📄 local_papers.py
│   │   └── 📁 http_client
│   │       └── 📄 arxiv_papers.py
├── 📁 application: FastMCP server configuration with dependency injection
│    ├── 📄 app.py
│    └── 📁 config
│        ├── 📄 config.py
│        └── 📄 container.py
└─── 📄 server.py: Call app.py to start or initialize MCP server
```

## Technology Stack

* Framework: FastMCP for [MCP](https://modelcontextprotocol.io/introduction) server implementation
* Dependencies: [Dependency Injector](https://python-dependency-injector.ets-labs.org/) for IoC container
* External API: [arXiv](https://info.arxiv.org/help/api/index.html) API for paper search and retrieval
* Storage: Local JSON files in arXiv-papers/ directory
* Testing: Comprehensive test suite with pytest and async support

## Prerequisites

- Install uv from [Astral](https://docs.astral.sh/uv/getting-started/installation/) or the [GitHub README](https://github.com/astral-sh/uv#installation)
- Run: `uv python install` to install python version from file `.python-version`

## Local development

To make changes to this MCP locally and run it:

```sh
uv venv
source .venv/bin/activate
uv sync
```

If you need to add or remove a dependency run :

`uv add [OPTIONS] <PACKAGES|--requirements <REQUIREMENTS>>`

`uv remove [OPTIONS] <PACKAGES>...`

Examples:

```sh
uv add "arxiv>=2.2.0"
uv remove "arxiv==2.2.0"

```

After update dependencies, you must generate or update the `uv.lock` file. It works `package.lock` from node, where lock the dependency versions to avoid conflicts. Run the following command to generate or update lock:

```sh
uv lock
```

Run Unit Tests with Pytest

```sh
uv run pytest
```

Run Coverage with html report

```sh
uv run coverage html
```

A report will be generated into `htmlcov` folder. Open file `htmlcov/index.html` with a browser to visualize the report.

Run MCP Server

```sh
uv run mcp-server-papers
```

To test the MCP Server, run the [Inspector](https://modelcontextprotocol.io/docs/tools/inspector#inspector) tool created by Anthropic.

⚠️ Note: You must install node version 22 or newer

```sh
npx @modelcontextprotocol/inspector
```

When you run the **Inspector**, it shows something like:

```sh
Starting MCP inspector...
⚙️ Proxy server listening on 127.0.0.1:6277
🔑 Session token: e35f9b0215e837b2058eab71a0d571a7855f0bee97670f806400eac40f612062
Use this token to authenticate requests or set DANGEROUSLY_OMIT_AUTH=true to disable auth

🔗 Open inspector with token pre-filled:
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=e35f9b0215e837b2058eab71a0d571a7855f0bee97670f806400eac40f612062
   (Auto-open is disabled when authentication is enabled)

🔍 MCP Inspector is up and running at http://127.0.0.1:6274
```

To test the MCP Server using the Inspector console:

1. Open `http://127.0.0.1:6274` in your browser
2. Navigate to the **Configuration** section
3. Enter the **Session token** in the **Proxy Session Token** field