import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../..", "src"))

import pytest
import pandas as pd
from boston_housing.domain.usecase.preprocess_usecase import PreprocessUseCase

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
        DummyHousing(7.0, None, 15.0, 5.0, 0.4, 0.2, 250, 70, 22.0),   # nulo
        DummyHousing(8.0, 10.0, 14.0, 6.0, 0.3, 0.3, 200, 80, 9999.0), # outlier
    ]

    use_case = PreprocessUseCase()
    X, y = use_case.execute(records)

    assert X.shape[0] < len(records)
    assert list(X.columns) == PreprocessUseCase.SELECTED_FEATURES
    assert X.isnull().sum().sum() == 0
    assert y.isnull().sum() == 0

def test_preprocess_use_case_raises_if_missing_target():
    class BadHousing:
        def __init__(self, rm, lstat):
            self.rm = rm
            self.lstat = lstat

    records = [BadHousing(6.0, 12.0)]
    use_case = PreprocessUseCase()

    with pytest.raises(KeyError):
        use_case.execute(records)
