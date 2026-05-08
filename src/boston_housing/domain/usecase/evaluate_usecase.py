import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import Dict

class EvaluateUseCase:
    """
    Caso de uso: Evaluación del modelo entrenado.

    Métricas calculadas:
        - RMSE  → penaliza errores grandes (mismas unidades que el target)
        - MAE   → error absoluto medio
        - R²    → proporción de varianza explicada (1.0 = perfecto)
    """

    def execute(self, pipeline: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> Dict:
        """
        Evalúa el modelo sobre el conjunto de test.

        Args:
            pipeline: Modelo entrenado
            X_test:   Features de test
            y_test:   Target real de test

        Returns:
            Diccionario con métricas RMSE, MAE, R²
        """
        y_pred = pipeline.predict(X_test)

        metrics = {
            "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
            "mae":  float(mean_absolute_error(y_test, y_pred)),
            "r2":   float(r2_score(y_test, y_pred))
        }

        print(f"  RMSE : {metrics['rmse']:.4f}  (error en miles de $)")
        print(f"  MAE  : {metrics['mae']:.4f}  (error medio absoluto)")
        print(f"  R²   : {metrics['r2']:.4f}  (varianza explicada)")

        return metrics
