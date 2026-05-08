import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from boston_housing.infrastructure.entry_points.prepare_data import prepare_data
from boston_housing.infrastructure.entry_points.train_model import train_model

def run_pipeline():
    """
    Pipeline completo reproducible y automatizable:
        Fase 1 → Preprocesamiento y limpieza
        Fase 2 → Entrenamiento, evaluación y persistencia
    """
    print("\n" + "=" * 50)
    print("  PIPELINE BOSTON HOUSING - INICIO")
    print("=" * 50 + "\n")

    prepare_data()

    print()

    train_model()

    print("\n" + "=" * 50)
    print("  PIPELINE COMPLETADO ✅")
    print("=" * 50)

if __name__ == "__main__":
    run_pipeline()
