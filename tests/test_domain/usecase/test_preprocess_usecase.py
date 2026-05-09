import pytest
import pandas as pd
from src.boston_housing.domain.usecase.preprocess_usecase import PreprocessUseCase
from src.boston_housing.domain.model.housing.housing import Housing

# Clase dummy para simular Housing
class DummyHousing:
    def __init__(self, rm, lstat, ptratio, dis, nox, crim, tax, age, price):
        self.rm = rm
        self.lstat = lstat
        self.ptratio = ptratio
        self.dis = dis
        self.nox = nox
        self.crim = crim
        self.tax = tax
        self.age = age
        self.price = price


def test_preprocess_pipeline_removes_duplicates_nulls_outliers():
    records = [
        DummyHousing(6.0, 12.0, 18.0, 4.0, 0.5, 0.1, 300, 65, 20.0),
        DummyHousing(6.0, 12.0, 18.0, 4.0, 0.5, 0.1, 300, 65, 20.0),  # duplicado
        DummyHousing(7.0, None, 15.0, 5.0, 0.4, 0.2, 250, 70, 22.0),   # nulo en lstat
        DummyHousing(8.0, 10.0, 14.0, 6.0, 0.3, 0.3, 200, 80, 9999.0), # posible outlier
    ]

    use_case = PreprocessUseCase()
    X, y = use_case.execute(records)

    # Debe eliminar al menos 1 duplicado
    assert X.shape[0] < len(records)

    # Verificamos que las columnas seleccionadas sean las esperadas
    assert list(X.columns) == PreprocessUseCase.SELECTED_FEATURES

    # Verificamos que no haya nulos en el resultado
    assert X.isnull().sum().sum() == 0
    assert y.isnull().sum() == 0


def test_preprocess_use_case_raises_if_missing_target():
    # Creamos registros sin la columna price
    class BadHousing:
        def __init__(self, rm, lstat):
            self.rm = rm
            self.lstat = lstat

    records = [BadHousing(6.0, 12.0)]

    use_case = PreprocessUseCase()

    # Esperamos que falle porque falta la columna TARGET
    with pytest.raises(KeyError):
        use_case.execute(records)
