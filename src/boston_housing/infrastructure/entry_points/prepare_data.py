import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from boston_housing.infrastructure.driven_adapters.csv_repository import CsvHousingRepository
from boston_housing.domain.usecase.preprocess_usecase import PreprocessUseCase

def prepare_data():
    """
    Entry point: Script de entrada para la Fase 1 (Preparación y Limpieza).
    
    Flujo:
        1. Carga dataset desde OpenML (o local si existe)
        2. Ejecuta caso de uso de preprocesamiento
        3. Guarda datos limpios en data/processed/
    """
    print("=" * 50)
    print("  FASE 1: Limpieza y selección del dataset")
    print("=" * 50)

    # 1. Cargar datos raw
    repo = CsvHousingRepository(raw_path="HousingData.csv")
    records = repo.load()
    print(f"\n📋 Registros cargados: {len(records)}\n")

    # 2. Preprocesar
    print("🔧 Aplicando limpieza...\n")
    X, y = PreprocessUseCase().execute(records)

    # 3. Guardar datos procesados
    os.makedirs("data/processed", exist_ok=True)
    processed = X.copy()
    processed["price"] = y
    processed.to_csv("data/processed/boston_clean.csv", index=False)

    print(f"\n💾 Guardado en: data/processed/boston_clean.csv")
    print(f"\n📊 Estadísticas del target (price):")
    print(y.describe().to_string())
    print("\n✅ Fase 1 completada.")

if __name__ == "__main__":
    prepare_data()
