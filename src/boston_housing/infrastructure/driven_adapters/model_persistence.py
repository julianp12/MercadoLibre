import joblib
import json
import os
from pathlib import Path  # Usamos Path para manejar rutas de forma inteligente
from datetime import datetime
from sklearn.pipeline import Pipeline
from typing import Dict

class ModelPersistence:
    """
    Adaptador: Persistencia del modelo entrenado.
    Funciona tanto en Windows como en Linux sin errores de barras (\\ vs /).
    """
    def __init__(self, models_dir: str = "models"):
        # Convertimos a objeto Path para que sea multiplataforma
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def save(self, pipeline: Pipeline, metrics: Dict, version: str = None) -> str:
        version = version or datetime.now().strftime("%Y%m%d_%H%M%S")
        
        model_filename = f"model_{version}.joblib"
        # Usamos / con Path para unir rutas (funciona en cualquier OS)
        model_path = self.models_dir / model_filename
        meta_path = self.models_dir / f"model_{version}.json"
        latest_path = self.models_dir / "latest.txt"

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

        # IMPORTANTE: Guardamos SOLO el nombre del archivo, NO la ruta completa
        # Esto evita que se guarden barras "\\" de Windows que rompen Linux
        with open(latest_path, "w") as f:
            f.write(model_filename)

        print(f" ✅ Modelo local → {model_path}")
        return str(model_path)

    def load_latest(self) -> Pipeline:
        """Carga el modelo de la versión más reciente de forma segura."""
        latest_path = self.models_dir / "latest.txt"
        
        if not latest_path.exists():
            raise FileNotFoundError(f"No hay modelos en {latest_path}. Ejecuta el pipeline primero.")

        with open(latest_path) as f:
            filename = f.read().strip()
        
        # Limpiamos el nombre por si acaso venía con rutas antiguas
        filename = Path(filename.replace("\\", "/")).name
        full_path = self.models_dir / filename

        print(f" 📂 Cargando modelo desde: {full_path}")
        return joblib.load(full_path)

    def load(self, model_path: str) -> Pipeline:
        """Carga un modelo específico por ruta."""
        return joblib.load(model_path)
