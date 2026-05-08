# from dependency_injector import containers, providers
# from arxiv import Client

# from mcp_server_papers.domain.usecase.paper_usecase import PaperUseCase
# from mcp_server_papers.domain.usecase.resource_usecase import ResourceUseCase
# from mcp_server_papers.domain.usecase.prompt_usecase import PromptUseCase

# from mcp_server_papers.infrastructure.driven_adapters.http_client.arxiv_papers import ArxivPaper
# from mcp_server_papers.infrastructure.driven_adapters.local_files.local_papers import LocalPaper
# from mcp_server_papers.infrastructure.driven_adapters.prompts.papers import PromptPaper

# PAPER_DIR = "arXiv-papers"

# class Container(containers.DeclarativeContainer):


#     paper_adapter = providers.Singleton(
#         ArxivPaper,
#         client=Client(),
#         paper_dir=PAPER_DIR
#     )

#     resource_adapter = providers.Singleton(
#         LocalPaper
#     )

#     prompt_adapter = providers.Singleton(
#         PromptPaper
#     )

#     paper_usecase = providers.Singleton(
#         PaperUseCase,
#         paper_repository=paper_adapter
#     )

#     resource_usecase = providers.Singleton(
#         ResourceUseCase,
#         resource_repository=resource_adapter
#     )

#     prompt_usecase = providers.Singleton(
#         PromptUseCase,
#         prompt_repository=prompt_adapter
#     )
