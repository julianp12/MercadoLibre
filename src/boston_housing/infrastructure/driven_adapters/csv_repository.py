import pandas as pd
import os
from typing import List
from boston_housing.domain.model.housing.housing import Housing
from boston_housing.domain.model.housing.gateway.housing_repository import HousingRepository

class CsvHousingRepository(HousingRepository):
    """
    Adaptador concreto: Carga Boston Housing únicamente desde archivos locales.
    Eliminada la dependencia de OpenML/Kaggle para garantizar estabilidad.
    """
    
    COLUMN_MAPPING = {
        "CRIM": "crim", "ZN": "zn", "INDUS": "indus", "CHAS": "chas",
        "NOX": "nox", "RM": "rm", "AGE": "age", "DIS": "dis",
        "RAD": "rad", "TAX": "tax", "PTRATIO": "ptratio", "B": "b",
        "LSTAT": "lstat", "MEDV": "price"
    }

    def __init__(self, raw_path: str = "data/raw/boston_housing.csv"):
        # Priorizamos la carpeta raw, pero daremos flexibilidad en la carga
        self.raw_path = raw_path
    def load(self) -> List[Housing]:
        # Rutas posibles dentro del contenedor y local
        possible_paths = [
            self.raw_path,                  # data/raw/boston_housing.csv
            "HousingData.csv",              # Raíz del proyecto
            "/app/HousingData.csv",         # Raíz en Docker
            "data/HousingData.csv"          # Carpeta data
        ]
        
        df = None
        for path in possible_paths:
            if os.path.exists(path):
                print(f"📂 Dataset encontrado en: {path}")
                df = pd.read_csv(path)
                break
        
        if df is None:
            raise FileNotFoundError(
                f"❌ No se encontró el dataset. Rutas intentadas: {possible_paths}. "
                "Verifica que el archivo esté en la raíz de tu proyecto."
            )

        # Normalización (igual que antes)
        df.columns = [self.COLUMN_MAPPING.get(c.upper(), c.lower()) for c in df.columns]
        known_cols = list(self.COLUMN_MAPPING.values())
        df = df[[c for c in known_cols if c in df.columns]]
        return [Housing(**row) for row in df.to_dict(orient="records")]

    def load_as_dataframe(self) -> pd.DataFrame:
        """Carga dataset como DataFrame para el pipeline de entrenamiento."""
        records = self.load()
        return pd.DataFrame([r.__dict__ for r in records])
