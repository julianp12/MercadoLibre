import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from typing import Tuple

class TrainUseCase:
    """
    Caso de uso: Entrenamiento del modelo base de regresión.

    Pipeline sklearn:
        1. StandardScaler  → normaliza features
        2. Ridge Regression → modelo base de regresión lineal regularizada
    """

    def __init__(self, test_size: float = 0.2, random_state: int = 42, alpha: float = 1.0):
        self.test_size = test_size
        self.random_state = random_state
        self.alpha = alpha

    def execute(
        self, X: pd.DataFrame, y: pd.Series
    ) -> Tuple[Pipeline, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Entrena el modelo con los datos preprocesados.

        Args:
            X: Features limpias
            y: Target (precio)

        Returns:
            pipeline: Modelo entrenado (scaler + estimador)
            X_train, X_test, y_train, y_test: Splits de evaluación
        """
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state
        )
        print(f"  Train: {len(X_train)} registros | Test: {len(X_test)} registros")

        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("model", Ridge(alpha=self.alpha))
        ])

        pipeline.fit(X_train, y_train)
        print(f"  ✅ Modelo entrenado: Ridge(alpha={self.alpha})")

        return pipeline, X_train, X_test, y_train, y_test
