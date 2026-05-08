from unittest.mock import AsyncMock, call
import pytest

from mcp.server.fastmcp import FastMCP

from mcp_server_papers.application.config.container import Container
from mcp_server_papers.application.app import mcp
from mcp_server_papers.infrastructure.entry_points import tools

@pytest.fixture(name='mock_mcp')
def setup_mock_mcp():
    """
    Fixture to create a mock MCP instance.
    """
    return AsyncMock(spec=FastMCP)

@pytest.fixture(name='container')
def setup_container():
    """
    Fixture to create a container instance.
    """
    return Container()

@pytest.fixture(name='mock_tool_usecase')
def mock_paper_usecase_fixture():
    """Mock ToolsUseCase."""
    usecase = AsyncMock()
    usecase.search_papers.return_value = ["paper1", "paper2"]
    usecase.extract_info.return_value = '{"title": "Test Paper", "authors": ["Author1"]}'
    return usecase

@pytest.mark.asyncio
async def test_bind_tools(mock_mcp):
    """
    Test the binding of tools to the MCP instance.
    """

    tools.bind_tools(mock_mcp)

    assert hasattr(mock_mcp, 'tool')
    assert callable(mock_mcp.tool)

    # Check if specific tools are registered
    assert mock_mcp.tool.__dict__["_mock_call_count"] == 2  # Two tools should be registered
    assert call("search_papers") in mock_mcp.tool.__dict__["_mock_call_args_list"]
    assert call("extract_info") in mock_mcp.tool.__dict__["_mock_call_args_list"]

@pytest.mark.asyncio
async def test_search_papers_mcp_tool(
    container,
    mock_tool_usecase):
    """Test that MCP tools are properly registered and callable."""

    with container.paper_usecase.override(mock_tool_usecase):
        container.wire(modules=[tools])
        tools.bind_tools(mcp)

        result = await mcp.call_tool("search_papers", {"topic": "test topic", "max_results": 1})
        print("RESULT:", result, type(result))

        assert isinstance(result, tuple)
        assert isinstance(result[0], list)
        assert result[0][0].text == "paper1"
        assert result[0][1].text == "paper2"

    container.reset_override()

@pytest.mark.asyncio
async def test_extract_info_mcp_tool(
    container,
    mock_tool_usecase):
    """Test that MCP tools are properly registered and callable."""

    with Container.paper_usecase.override(mock_tool_usecase):
        container.wire(modules=[tools])
        tools.bind_tools(mcp)
        result = await mcp.call_tool("extract_info", {"paper_id": "paper1"})

        assert isinstance(result, tuple)
        assert isinstance(result[0], list)
        assert result[0][0].text == '{"title": "Test Paper", "authors": ["Author1"]}'

    container.reset_override()
