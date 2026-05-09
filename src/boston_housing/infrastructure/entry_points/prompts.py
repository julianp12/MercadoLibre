from dependency_injector.wiring import inject, Provide

from mcp.server.fastmcp import FastMCP

from src.boston_housing.application.config.container import Container
from src.boston_housing.domain.usecase.prompt_usecase import PromptUseCase

@inject
def bind_prompts(mcp: FastMCP,
                   prompt_usecase: PromptUseCase = Provide[Container.prompt_usecase]
                   ):

    """
    Bind prompts.
    """

    @mcp.prompt()
    async def generate_search_prompt(topic: str, num_papers: int = 5) -> str:
        """Generate a prompt for Claude to find and discuss academic papers on a specific topic."""
        return await prompt_usecase.generate_search_prompt(topic=topic, num_papers=num_papers)
