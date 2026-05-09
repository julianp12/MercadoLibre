import pytest
import pandas as pd
import numpy as np
from src.boston_housing.domain.usecase.train_usecase import TrainUseCase

def test_train_use_case_executes_and_returns_pipeline():
    # Creamos datos sintéticos: y = 2x + ruido
    X = pd.DataFrame({"feature": np.arange(100)})
    y = pd.Series(2 * X["feature"] + np.random.normal(0, 0.1, size=100))

    use_case = TrainUseCase(test_size=0.2, random_state=42, alpha=1.0)
    pipeline, X_train, X_test, y_train, y_test = use_case.execute(X, y)

    # Verificamos tamaños de los splits
    assert len(X_train) == 80
    assert len(X_test) == 20
    assert len(y_train) == 80
    assert len(y_test) == 20

    # Verificamos que el pipeline tenga los pasos correctos
    steps = dict(pipeline.named_steps)
    assert "scaler" in steps
    assert "model" in steps

    # Verificamos que el modelo esté entrenado y pueda predecir
    preds = pipeline.predict(X_test)
    assert len(preds) == len(y_test)
    # La R² debería ser alta porque los datos son lineales
    r2 = pipeline.score(X_test, y_test)
    assert r2 > 0.9
