import json
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

class Model:
    def __init__(self, model_path: str):
        # Cargar el archivo JSON
        with open(model_path, "r") as f:
            model_info = json.load(f)
        
        # Extraer información del modelo
        self.features = model_info["features"]
        self.metrics = model_info["metrics"]
        
        # Reconstruir el modelo (en este caso, Ridge)
        self.model = Ridge()  # Ajustar esegún el tipo de modelo
        self.scaler = StandardScaler()  # Escalador (ajústalo si es necesario)

    def scale_features(self, features):
        """
        Escala las características utilizando el escalador cargado.
        """
        return self.scaler.transform([features])

    def predict(self, scaled_features):
        """
        Realiza una predicción utilizando el modelo cargado.
        """
        return self.model.predict(scaled_features)