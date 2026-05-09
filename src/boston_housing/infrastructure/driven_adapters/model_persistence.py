import joblib
import json
import os
from datetime import datetime
from sklearn.pipeline import Pipeline
from typing import Dict

class ModelPersistence:
    """
    Adaptador: Persistencia del modelo entrenado.

    Guarda:
        - models/model_<version>.joblib   → modelo serializado
        - models/model_<version>.json     → métricas y metadata
        - models/latest.txt               → apunta a la versión más reciente
    """

    def __init__(self, models_dir: str = "models"):
        self.models_dir = models_dir
        os.makedirs(models_dir, exist_ok=True)

    def save(self, pipeline: Pipeline, metrics: Dict, version: str = None) -> str:
        """
        Serializa el modelo y guarda sus métricas.

        Args:
            pipeline: Modelo sklearn entrenado
            metrics:  Diccionario con RMSE, MAE, R²
            version:  Etiqueta de versión (por defecto timestamp)

        Returns:
            Ruta al archivo .joblib guardado
        """
        version = version or datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f"model_{version}.joblib"
        model_path  = os.path.join(self.models_dir, model_filename)
        meta_path   = os.path.join(self.models_dir, f"model_{version}.json")
        latest_path = os.path.join(self.models_dir, "latest.txt")

        # Guardar modelo
        joblib.dump(pipeline, model_path)

        # Guardar métricas + metadata
        metadata = {
            "version": version,
            "model_type": type(pipeline.named_steps["model"]).__name__,
            "features": list(pipeline.feature_names_in_) if hasattr(pipeline, "feature_names_in_") else [],
            "metrics": metrics
        }
        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=2)

        # Actualizar puntero a latest
        with open(latest_path, "w") as f:
            f.write(model_filename)

        print(f"  ✅ Modelo  → {model_path}")
        print(f"  ✅ Métricas → {meta_path}")
        return model_path

    def load_latest(self) -> Pipeline:
        """Carga el modelo de la versión más reciente."""
        latest_path = os.path.join(self.models_dir, "latest.txt")
        if not os.path.exists(latest_path):
            raise FileNotFoundError("No hay modelos guardados. Ejecuta train primero.")
        with open(latest_path) as f:
            stored_path = f.read().strip()

        # Extraer solo el nombre del archivo para evitar conflictos de separadores (Windows vs Linux)
        # El replace asegura que podamos manejar rutas antiguas que aún tengan backslashes
        filename = os.path.basename(stored_path.replace("\\", "/"))
        full_path = os.path.join(self.models_dir, filename)
        return joblib.load(full_path)

    def load(self, model_path: str) -> Pipeline:
        """Carga un modelo específico por ruta."""
        return joblib.load(model_path)
