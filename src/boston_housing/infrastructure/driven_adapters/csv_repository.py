import pandas as pd
import os
from typing import List
from boston_housing.domain.model.housing.housing import Housing
from boston_housing.domain.model.housing.gateway.housing_repository import HousingRepository

class CsvHousingRepository(HousingRepository):
    """
    Adaptador concreto: Carga Boston Housing desde OpenML (open-source).
    
    Responsabilidades:
        - Descargar dataset desde OpenML si no existe localmente
        - Leer CSV y mapear columnas a entidades
        - Proporcionar datos en formato Housing o DataFrame
    """

    OPENML_URL = "https://www.openml.org/data/get_csv/531/boston_corrected.arff"

    COLUMN_MAPPING = {
        "CRIM": "crim", "ZN": "zn", "INDUS": "indus", "CHAS": "chas",
        "NOX": "nox", "RM": "rm", "AGE": "age", "DIS": "dis",
        "RAD": "rad", "TAX": "tax", "PTRATIO": "ptratio",
        "B": "b", "LSTAT": "lstat", "MEDV": "price"
    }

    def __init__(self, raw_path: str = "data/raw/boston_housing.csv"):
        self.raw_path = raw_path

    def download(self) -> pd.DataFrame:
        """Descarga el dataset desde OpenML y lo guarda localmente."""
        dirpath = os.path.dirname(self.raw_path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        print("📥 Descargando dataset desde OpenML...")
        df = pd.read_csv(self.OPENML_URL)
        cols = [c for c in self.COLUMN_MAPPING if c in df.columns]
        df = df[cols].rename(columns=self.COLUMN_MAPPING)
        df.to_csv(self.raw_path, index=False)
        print(f"✅ Guardado en: {self.raw_path} → {len(df)} registros")
        return df

    def load(self) -> List[Housing]:
        """
        Carga dataset y lo mapea a entidades Housing.
        - Si el CSV existe localmente → lo carga directamente
        - Si no existe → descarga desde OpenML
        """
        if not os.path.exists(self.raw_path):
            df = self.download()
        else:
            print(f"📂 Cargando desde: {self.raw_path}")
            df = pd.read_csv(self.raw_path)

        # Renombrar columnas si vienen en mayúsculas (CSV original)
        df.columns = [self.COLUMN_MAPPING.get(c, c.lower()) for c in df.columns]

        # Mantener solo columnas conocidas
        known_cols = list(self.COLUMN_MAPPING.values())
        df = df[[c for c in known_cols if c in df.columns]]

        return [Housing(**row) for row in df.to_dict(orient="records")]

    def load_as_dataframe(self) -> pd.DataFrame:
        """Carga dataset como DataFrame (útil para análisis)."""
        if not os.path.exists(self.raw_path):
            return self.download()
        return pd.read_csv(self.raw_path)
