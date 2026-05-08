import uvicorn
from fastapi import FastAPI

from src.boston_housing.infrastructure.entry_points.routes import bind_routes


def create_app() -> FastAPI:
    app = FastAPI(
        title="Boston Housing API",
        version="1.0.0",
        description="API REST para inferencia de precios de viviendas usando Boston Housing.",
    )
    bind_routes(app)
    return app


app = create_app()


def start_server(host: str = "127.0.0.1", port: int = 8000) -> int:
    uvicorn.run(app, host=host, port=port)
    return 0