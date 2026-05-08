from unittest.mock import AsyncMock, call
from typing import List
import pytest

from mcp.server.fastmcp import FastMCP
from mcp.server.lowlevel.helper_types import ReadResourceContents

from mcp_server_papers.application.config.container import Container
from mcp_server_papers.application.app import mcp
from mcp_server_papers.infrastructure.entry_points import resources

@pytest.fixture(name='mock_mcp')
def setup_mock_mcp():
    """
    Fixture to create a mock MCP instance.
    """
    return AsyncMock(spec=FastMCP)

@pytest.fixture(name='mock_resource_usecase')
def mock_resource_usecase_fixture():
    """Mock ResourceUseCase."""
    usecase = AsyncMock()
    usecase.get_available_folders.return_value = ["ai", "ml", "nlp"]
    usecase.get_topic_papers.return_value = "Paper details"
    return usecase

@pytest.mark.asyncio
async def test_bind_resources(mock_mcp):
    """
    Test the binding of resources to the MCP instance.
    """

    resources.bind_resources(mock_mcp)

    # Verify that the resource methods are bound correctly
    assert hasattr(mock_mcp, 'resource')
    assert callable(mock_mcp.resource)

    # Check if specific resource are registered
    # Two resources should be registered
    assert mock_mcp.resource.__dict__["_mock_call_count"] == 2
    assert call("papers://folders") in mock_mcp.resource.__dict__["_mock_call_args_list"]
    assert call("papers://{topic}") in mock_mcp.resource.__dict__["_mock_call_args_list"]

@pytest.mark.asyncio
async def test_get_available_folders_mcp_resource(
    mock_resource_usecase):
    """Test that MCP resources are properly registered and callable."""
    container = Container()

    with container.resource_usecase.override(mock_resource_usecase):
        container.wire(modules=[resources])
        resources.bind_resources(mcp)

        result: List[ReadResourceContents] = await mcp.read_resource("papers://folders")

        assert isinstance(result, list)
        assert "ai" in result[0].content

@pytest.mark.asyncio
async def test_get_topic_papers_mcp_resource(
    mock_resource_usecase):
    """Test that MCP resources are properly registered and callable."""
    container = Container()

    with container.resource_usecase.override(mock_resource_usecase):
        container.wire(modules=[resources])
        resources.bind_resources(mcp)

        result: List[ReadResourceContents] = await mcp.read_resource("papers://ai")

        assert isinstance(result, list)
        assert "Paper details" in result[0].content
