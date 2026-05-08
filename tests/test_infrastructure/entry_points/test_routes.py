import pytest

from starlette.testclient import TestClient

from mcp_server_papers.application.app import mcp
from mcp_server_papers.infrastructure.entry_points import routes

@pytest.mark.asyncio
async def test_mcp_custom_route():
    """Test the custom route for health check in MCP server."""
    routes.bind_routes(mcp)

    with TestClient(mcp.streamable_http_app()) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
