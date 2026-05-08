from unittest.mock import Mock, patch
import pytest

from mcp.server.fastmcp import FastMCP

from mcp_server_papers.server import main
from mcp_server_papers.application.app import lifespan, start_server, mcp

@pytest.fixture(name='mock_mcp')
def mock_mcp_fixture():
    """Mock FastMCP instance."""
    fast_mcp = Mock(spec=FastMCP)
    fast_mcp.tool = Mock()
    fast_mcp.resource = Mock()
    fast_mcp.prompt = Mock()
    return fast_mcp

@pytest.mark.asyncio
async def test_lifespan_setup_and_teardown(mock_mcp):
    """Test that lifespan properly sets up and tears down dependencies."""

    with patch('mcp_server_papers.application.app.Container') as mock_container_class:
        mock_container = Mock()
        mock_container_class.return_value = mock_container

        with patch('mcp_server_papers.application.app.tools') as mock_tools, \
                patch('mcp_server_papers.application.app.resources') as mock_resources, \
                patch('mcp_server_papers.application.app.prompts') as mock_prompts:

            # Test the lifespan context manager
            async with lifespan(mock_mcp):
                # Verify container was created and wired
                mock_container_class.assert_called_once()
                mock_container.wire.assert_called_once()

                # Verify modules were wired
                expected_modules = [mock_tools, mock_resources, mock_prompts]
                mock_container.wire.assert_called_with(modules=expected_modules)

                # Verify binding functions were called
                mock_tools.bind_tools.assert_called_once_with(mock_mcp)
                mock_resources.bind_resources.assert_called_once_with(mock_mcp)
                mock_prompts.bind_prompts.assert_called_once_with(mock_mcp)

@pytest.mark.asyncio
async def test_full_app_lifecycle():
    """Test the complete application lifecycle."""

    with patch('mcp_server_papers.application.app.Container') as mock_container_class:
        mock_container = Mock()
        mock_container_class.return_value = mock_container

        with patch('mcp_server_papers.application.app.tools') as mock_tools, \
                patch('mcp_server_papers.application.app.resources') as mock_resources, \
                patch('mcp_server_papers.application.app.prompts') as mock_prompts, \
                patch.object(mcp, 'run') as mock_run:

            # Test the full lifecycle
            async with lifespan(mcp):
                start_server()

            # Verify all components were properly initialized
            mock_container_class.assert_called_once()
            mock_container.wire.assert_called_once()
            mock_tools.bind_tools.assert_called_once_with(mcp)
            mock_resources.bind_resources.assert_called_once_with(mcp)
            mock_prompts.bind_prompts.assert_called_once_with(mcp)
            mock_run.assert_called_once()

def test_main():
    """Test the main entry point."""
    with patch('mcp_server_papers.application.app.start_server') as mock_start_server:
        main()
        mock_start_server.assert_called_once()
