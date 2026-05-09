import pandas as pd
from typing import List, Tuple
from src.boston_housing.domain.model.housing.housing import Housing

class PreprocessUseCase:
    """
    Caso de uso: Limpieza y selección de features del dataset Boston Housing.
    
    Responsabilidades:
        - Validar tipos de datos
        - Eliminar duplicados
        - Tratar nulos
        - Eliminar outliers
        - Seleccionar features relevantes
    """

    SELECTED_FEATURES = ["rm", "lstat", "ptratio", "dis", "nox", "crim", "tax", "age"]
    TARGET = "price"

    def execute(self, records: List[Housing]) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Ejecuta el pipeline de preprocesamiento.
        
        Args:
            records: Lista de entidades Housing cargadas desde repositorio
            
        Returns:
            X: DataFrame con features seleccionadas
            y: Series con el target (precios)
        """
        df = pd.DataFrame([vars(r) for r in records])
        print(f"  Shape inicial: {df.shape}")

        df = self._validate_types(df)
        df = self._remove_duplicates(df)
        df = self._handle_nulls(df)
        df = self._remove_outliers(df)
        X, y = self._select_features(df)

        print(f"  Shape final:   {X.shape}")
        return X, y

    def _validate_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fuerza tipos numéricos en todas las columnas."""
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        return df

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Elimina filas duplicadas."""
        before = len(df)
        df = df.drop_duplicates()
        removed = before - len(df)
        if removed:
            print(f"  ⚠️  Duplicados eliminados: {removed}")
        return df

    def _handle_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detecta e imputa nulos con mediana."""
        nulls = df.isnull().sum()
        cols_with_nulls = nulls[nulls > 0]
        if cols_with_nulls.empty:
            print("  ✅ Sin valores nulos")
        else:
            print(f"  ⚠️  Nulos encontrados:\n{cols_with_nulls}")
            for col in cols_with_nulls.index:
                df[col] = df[col].fillna(df[col].median())
            print("  ✅ Nulos imputados con mediana")
        return df

    def _remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Elimina outliers del target usando IQR."""
        before = len(df)
        y = df[self.TARGET]
        Q1, Q3 = y.quantile(0.25), y.quantile(0.75)
        IQR = Q3 - Q1
        mask = (y >= Q1 - 1.5 * IQR) & (y <= Q3 + 1.5 * IQR)
        df = df[mask]
        removed = before - len(df)
        if removed:
            print(f"  ⚠️  Outliers eliminados del target: {removed}")
        return df

    def _select_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Selecciona features relevantes y separa target."""
        y = df[self.TARGET]
        X = df[self.SELECTED_FEATURES]
        print(f"  ✅ Features seleccionadas: {self.SELECTED_FEATURES}")
        return X.reset_index(drop=True), y.reset_index(drop=True)
