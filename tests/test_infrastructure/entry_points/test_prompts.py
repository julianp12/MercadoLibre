from unittest.mock import AsyncMock
import pytest

from mcp.server.fastmcp import FastMCP
from mcp.types import GetPromptResult

from mcp_server_papers.application.config.container import Container
from mcp_server_papers.application.app import mcp
from mcp_server_papers.infrastructure.entry_points import prompts

@pytest.fixture(name='mock_mcp')
def setup_mock_mcp():
    """
    Fixture to create a mock MCP instance.
    """
    return AsyncMock(spec=FastMCP)

@pytest.fixture(name='mock_prompt_usecase')
def mock_prompt_usecase_fixture():
    """Mock PromptUseCase."""
    usecase = AsyncMock()
    usecase.generate_search_prompt.return_value = "Search prompt for topic"
    return usecase

@pytest.mark.asyncio
async def test_bind_prompts(mock_mcp):
    """
    Test the binding of prompts to the MCP instance.
    """
    # Call the bind_prompts function with the mock MCP instance
    prompts.bind_prompts(mock_mcp)

    # Verify that the prompt methods are bound correctly
    assert hasattr(mock_mcp, 'prompt')
    assert callable(mock_mcp.prompt)

    # Check if specific prompts are registered
    # One prompt should be registered
    assert mock_mcp.prompt.__dict__["_mock_call_count"] == 1

@pytest.mark.asyncio
async def test_generate_search_prompt_mcp_prompt(
    mock_prompt_usecase):
    """Test that MCP prompts are properly registered and callable."""
    container = Container()
    with container.prompt_usecase.override(mock_prompt_usecase):

        container.wire(modules=[prompts])
        prompts.bind_prompts(mcp)

        result_prompts = await mcp.list_prompts()
        assert isinstance(result_prompts, list)
        result: GetPromptResult = await mcp.get_prompt(
            "generate_search_prompt", {"topic": "ai", "num_papers": 1})

        assert isinstance(result, GetPromptResult)
        assert result.messages[0].content.text == "Search prompt for topic"

    container.reset_override()
