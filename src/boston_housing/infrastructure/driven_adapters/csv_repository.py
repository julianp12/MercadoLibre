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
        """
        Carga dataset y lo mapea a entidades Housing buscando en rutas locales.
        """
        # 1. Intentar cargar desde la ruta configurada (data/raw/boston_housing.csv)
        if os.path.exists(self.raw_path):
            print(f"📂 Cargando desde: {self.raw_path}")
            df = pd.read_csv(self.raw_path)
        
        # 2. Backup: Buscar en la raíz de data por si el archivo se llama distinto
        elif os.path.exists("data/HousingData.csv"):
            print("📂 Cargando desde backup local: data/HousingData.csv")
            df = pd.read_csv("data/HousingData.csv")
        
        else:
            raise FileNotFoundError(
                f"❌ No se encontró el dataset local en {self.raw_path} ni en data/HousingData.csv. "
                "Asegúrate de copiar el archivo al contenedor."
            )

        # Normalización de columnas (Mayúsculas a minúsculas según el mapping)
        df.columns = [self.COLUMN_MAPPING.get(c.upper(), c.lower()) for c in df.columns]
        
        # Mantener solo columnas conocidas para evitar errores de mapeo
        known_cols = list(self.COLUMN_MAPPING.values())
        df = df[[c for c in known_cols if c in df.columns]]

        return [Housing(**row) for row in df.to_dict(orient="records")]

    def load_as_dataframe(self) -> pd.DataFrame:
        """Carga dataset como DataFrame para el pipeline de entrenamiento."""
        records = self.load()
        return pd.DataFrame([r.__dict__ for r in records])
