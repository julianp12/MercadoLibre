from functools import lru_cache
from pathlib import Path
from typing import Union

import pandas as pd
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel

from src.boston_housing.infrastructure.driven_adapters.model_persistence import ModelPersistence


router = APIRouter(tags=["inference"])


class PredictRequest(BaseModel):
    features: Union[dict[str, float], list[float]]


class PredictionResponse(BaseModel):
    prediction: list[float]
    model_features: list[str]


class HealthResponse(BaseModel):
    status: str


def _resolve_models_dir() -> Path:
    return Path(__file__).resolve().parents[4] / "models"


@lru_cache(maxsize=1)
def _load_pipeline_and_features():
    pipeline = ModelPersistence(str(_resolve_models_dir())).load_latest()
    feature_names = list(getattr(pipeline, "feature_names_in_", []))
    if not feature_names:
        raise ValueError("El modelo cargado no expone feature_names_in_.")
    return pipeline, feature_names


def _build_features_frame(features, expected_features):
    if isinstance(features, dict):
        missing = [feature for feature in expected_features if feature not in features]
        if missing:
            raise ValueError(f"Faltan features requeridas: {missing}")
        row = {feature: float(features[feature]) for feature in expected_features}
        return pd.DataFrame([row], columns=expected_features)

    if isinstance(features, list):
        if len(features) != len(expected_features):
            raise ValueError(
                f"Se esperaban {len(expected_features)} valores en 'features' y se recibieron {len(features)}."
            )
        row = {feature: float(value) for feature, value in zip(expected_features, features)}
        return pd.DataFrame([row], columns=expected_features)

    raise ValueError("'features' debe ser un objeto con nombres de columnas o una lista de valores.")


@router.get("/health", response_model=HealthResponse)
@router.get("/api/health", response_model=HealthResponse, include_in_schema=False)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/predict", response_model=PredictionResponse)
@router.post("/api/predict", response_model=PredictionResponse, include_in_schema=False)
async def predict(payload: PredictRequest) -> PredictionResponse:
    try:
        pipeline, expected_features = _load_pipeline_and_features()
        input_frame = _build_features_frame(payload.features, expected_features)
        prediction = pipeline.predict(input_frame)
        return PredictionResponse(
            prediction=prediction.tolist(),
            model_features=expected_features,
        )
    except ValueError as exc:
        _, expected_features = _load_pipeline_and_features()
        raise HTTPException(
            status_code=400,
            detail={
                "error": str(exc),
                "expected_features": expected_features,
            },
        ) from exc


def bind_routes(app: FastAPI):
    """Registra las rutas de inferencia en la aplicación FastAPI."""
    app.include_router(router)
