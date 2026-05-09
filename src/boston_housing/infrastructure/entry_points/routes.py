import pandas as pd
from functools import lru_cache
from pathlib import Path
from typing import Union
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel

# Importación ajustada para el entorno de ejecución en Docker/Local
try:
    from boston_housing.infrastructure.driven_adapters.model_persistence import ModelPersistence
except ImportError:
    from src.boston_housing.infrastructure.driven_adapters.model_persistence import ModelPersistence

router = APIRouter(tags=["inference"])

# --- Modelos de Pydantic ---

class PredictRequest(BaseModel):
    features: Union[dict[str, float], list[float]]

class PredictionResponse(BaseModel):
    prediction: list[float]
    model_features: list[str]

class HealthResponse(BaseModel):
    status: str

# --- Utilidades Internas ---

def _resolve_models_dir() -> Path:
    """
    Localiza la carpeta de modelos de forma robusta para reentrenamiento.
    Busca primero en la raíz del contenedor (/app/models) y luego relativa al archivo.
    """
    # 1. Intentar ruta absoluta de Docker
    docker_path = Path("/app/models")
    if docker_path.exists():
        return docker_path
    
    # 2. Intentar ruta relativa al proyecto (ajustado a 4 niveles arriba desde infrastructure/entry_points)
    local_path = Path(__file__).resolve().parents[4] / "models"
    return local_path

@lru_cache(maxsize=1)
def _load_pipeline_and_features():
    """
    Carga el modelo más reciente generado por el orquestador de reentrenamiento.
    Usa el adaptador ModelPersistence corregido para evitar errores de rutas.
    """
    try:
        persistence = ModelPersistence(str(_resolve_models_dir()))
        pipeline = persistence.load_latest()
        
        feature_names = list(getattr(pipeline, "feature_names_in_", []))
        if not feature_names:
            raise ValueError("El modelo cargado no expone 'feature_names_in_'.")
            
        return pipeline, feature_names
    except FileNotFoundError as e:
        raise RuntimeError(f"Error crítico: No se encontró el archivo del modelo. {e}")
    except Exception as e:
        raise RuntimeError(f"Error al cargar el modelo: {e}")

def _build_features_frame(features, expected_features):
    """Construye el DataFrame para la predicción validando las features."""
    try:
        if isinstance(features, dict):
            missing = [f for f in expected_features if f not in features]
            if missing:
                raise ValueError(f"Faltan features requeridas: {missing}")
            row = {f: float(features[f]) for f in expected_features}
            return pd.DataFrame([row], columns=expected_features)

        if isinstance(features, list):
            if len(features) != len(expected_features):
                raise ValueError(
                    f"Se esperaban {len(expected_features)} valores y se recibieron {len(features)}."
                )
            row = {f: float(v) for f, v in zip(expected_features, features)}
            return pd.DataFrame([row], columns=expected_features)
            
    except (ValueError, TypeError) as e:
        raise ValueError(f"Error en el formato de los datos: {str(e)}")

    raise ValueError("'features' debe ser un diccionario o una lista de valores numéricos.")

# --- Endpoints ---

@router.get("/health", response_model=HealthResponse)
@router.get("/api/health", response_model=HealthResponse, include_in_schema=False)
async def health_check() -> HealthResponse:
    """Monitoreo básico de salud del servicio."""
    return HealthResponse(status="ok")

@router.post("/predict", response_model=PredictionResponse)
@router.post("/api/predict", response_model=PredictionResponse, include_in_schema=False)
async def predict(payload: PredictRequest) -> PredictionResponse:
    """
    Endpoint de inferencia. 
    Cumple con el requerimiento de producción al cargar siempre el modelo 'latest'.
    """
    try:
        # Cargar pipeline (usa el caché si ya fue cargado)
        pipeline, expected_features = _load_pipeline_and_features()
        
        # Procesar entrada
        input_frame = _build_features_frame(payload.features, expected_features)
        
        # Predecir
        prediction = pipeline.predict(input_frame)
        
        return PredictionResponse(
            prediction=prediction.tolist(),
            model_features=expected_features,
        )

    except RuntimeError as err:
        raise HTTPException(status_code=503, detail=str(err))
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": str(exc),
                "expected_features": expected_features if 'expected_features' in locals() else "unknown",
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

def bind_routes(app: FastAPI):
    """Registra las rutas en la aplicación FastAPI."""
    app.include_router(router)
