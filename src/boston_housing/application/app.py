import logging
from contextlib import asynccontextmanager

from mcp.server import FastMCP

from boston_housing.application.config.container import Container
from boston_housing.infrastructure.entry_points import (
    routes,
    prompts,
    resources,
    tools
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(fastmcp: FastMCP):
    """
    Context manager to manage IoC and lifespan of the application.
    """
    container = Container()
    container.wire(modules=[
        tools,
        resources,
        prompts
        ]
    )

    tools.bind_tools(fastmcp)
    resources.bind_resources(fastmcp)
    prompts.bind_prompts(fastmcp)

    yield

def start_server() -> int:
    print("Starting MCP server...")
    routes.bind_routes(mcp)
    logger.info("MCP server starting...")
    try:
        mcp.run(transport='streamable-http', mount_path="/mcp")
    except Exception as e:
        print("Exception in mcp.run():", e)
    return 0

mcp = FastMCP("research", lifespan=lifespan)
#app = mcp