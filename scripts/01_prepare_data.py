import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from boston_housing.infrastructure.repositories.csv_housing_repository import CsvHousingRepository
from boston_housing.application.use_cases.preprocess_data import PreprocessData

def main():
    print("=" * 50)
    print("  FASE 1: Limpieza y selección del dataset")
    print("=" * 50)

    repo = CsvHousingRepository(raw_path="data/raw/boston_housing.csv")
    records = repo.load()
    print(f"\n📋 Registros cargados: {len(records)}\n")

    print("🔧 Aplicando limpieza...\n")
    X, y = PreprocessData().execute(records)

    os.makedirs("data/processed", exist_ok=True)
    processed = X.copy()
    processed["price"] = y
    processed.to_csv("data/processed/boston_clean.csv", index=False)

    print(f"\n💾 Guardado en: data/processed/boston_clean.csv")
    print(f"\n📊 Estadísticas del target (price):")
    print(y.describe().to_string())
    print("\n✅ Fase 1 completada.")

if __name__ == "__main__":
    main()
