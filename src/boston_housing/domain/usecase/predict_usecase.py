from typing import List
from src.boston_housing.domain.model.housing.model import Model

# C:\Users\julia\OneDrive\Escritorio\MercadoLibre\src\boston_housing\domain\model\housing\model.py

class PredictUseCase:
    def __init__(self, model: Model):
        self.model = model

    def predict(self, features: List[float]) -> List[float]:
        """
        Realiza una predicción utilizando el modelo cargado.

        Args:
            features (List[float]): Lista de características de entrada.

        Returns:
            List[float]: Predicción del modelo.
        """
        scaled_features = self.model.scale_features(features)
        prediction = self.model.predict(scaled_features)
        return prediction