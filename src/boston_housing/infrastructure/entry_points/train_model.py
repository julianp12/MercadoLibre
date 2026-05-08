import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import pandas as pd
from boston_housing.domain.usecase.train_usecase import TrainUseCase
from boston_housing.domain.usecase.evaluate_usecase import EvaluateUseCase
from boston_housing.infrastructure.driven_adapters.model_persistence import ModelPersistence

def train_model():
    """
    Entry point: Fase 2 → Entrenamiento, evaluación y persistencia del modelo.

    Requisitos previos:
        - Ejecutar prepare_data.py (Fase 1) primero
        - data/processed/boston_clean.csv debe existir
    """
    print("=" * 50)
    print("  FASE 2: Entrenamiento del modelo")
    print("=" * 50)

    # 1. Cargar datos procesados
    processed_path = "data/processed/boston_clean.csv"
    if not os.path.exists(processed_path):
        raise FileNotFoundError(
            f"No se encontró {processed_path}. Ejecuta primero:\n"
            "  python -m src.boston_housing.infrastructure.entry_points.prepare_data"
        )

    df = pd.read_csv(processed_path)
    X = df.drop(columns=["price"])
    y = df["price"]
    print(f"\n📋 Datos cargados: {X.shape[0]} registros, {X.shape[1]} features\n")

    # 2. Entrenar
    print("🏋️  Entrenando modelo Ridge Regression...\n")
    pipeline, X_train, X_test, y_train, y_test = TrainUseCase().execute(X, y)

    # 3. Evaluar
    print("\n📊 Evaluando modelo...\n")
    metrics = EvaluateUseCase().execute(pipeline, X_test, y_test)

    # 4. Persistir
    print("\n💾 Guardando modelo...\n")
    ModelPersistence().save(pipeline, metrics)

    print("\n✅ Fase 2 completada.")

if __name__ == "__main__":
    train_model()
