import sys
import os
from pathlib import Path
import pandas as pd
import mlflow
import mlflow.sklearn
from boston_housing.domain.usecase.train_usecase import TrainUseCase
from boston_housing.domain.usecase.evaluate_usecase import EvaluateUseCase
from boston_housing.infrastructure.driven_adapters.model_persistence import ModelPersistence

# Configuración de ruta raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

def train_model():
    """
    Fase 2 → Entrenamiento, evaluación y persistencia con MLflow Model Registry.
    """
    print("=" * 50)
    print(" FASE 2: Entrenamiento del modelo")
    print("=" * 50)

    # 1. Configuración de MLflow para Producción (Docker) o Local
    # En Docker, 'mlflow' es el nombre del servicio en docker-compose
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("BostonHousing")

    # 2. Cargar datos procesados
    processed_path = "data/processed/boston_clean.csv"
    if not os.path.exists(processed_path):
        raise FileNotFoundError(
            f"No se encontró {processed_path}. Ejecuta primero el orquestador."
        )

    df = pd.read_csv(processed_path)
    X = df.drop(columns=["price"])
    y = df["price"]

    print(f"\n📋 Datos cargados: {X.shape[0]} registros, {X.shape[1]} features\n")

    with mlflow.start_run() as run:
        # 3. Entrenar
        print("🏋️ Entrenando modelo Ridge Regression...\n")
        pipeline, X_train, X_test, y_train, y_test = TrainUseCase().execute(X, y)

        # 4. Evaluar
        print("\n📊 Evaluando modelo...\n")
        metrics = EvaluateUseCase().execute(pipeline, X_test, y_test)

        # Log de métricas en MLflow
        for k, v in metrics.items():
            mlflow.log_metric(k, v)

        # 5. Persistencia y Registro (REENTRENAMIENTO)
        print("\n💾 Guardando y Registrando modelo...\n")
        
        # Persistencia local (tu clase actual)
        ModelPersistence().save(pipeline, metrics)

        # Registro en MLflow Model Registry (Esto habilita las VERSIONES en la pestaña Models)
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="model",
            registered_model_name="BostonHousing_Prod" # <--- CLAVE PARA REENTRENAMIENTO
        )

        print(f"\n✅ Fase 2 completada.")
        print(f"📍 Run ID: {run.info.run_id}")
        print(f"📦 Modelo registrado como: BostonHousing_Prod")

if __name__ == "__main__":
    train_model()
