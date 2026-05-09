import pandas as pd
import numpy as np
import pytest
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.boston_housing.domain.usecase.evaluate_usecase import EvaluateUseCase  # ajusta el import según tu estructura


@pytest.fixture
def sample_data():
    # Datos simples: y = 2x + 1
    X = pd.DataFrame({"feature": np.arange(10)})
    y = pd.Series(2 * X["feature"] + 1)
    return X, y


def test_execute_returns_metrics(sample_data):
    X, y = sample_data

    # Entrenamos un pipeline sencillo
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression())
    ])
    pipeline.fit(X, y)

    # Evaluamos
    evaluator = EvaluateUseCase()
    metrics = evaluator.execute(pipeline, X, y)

    # Verificamos que devuelve las claves correctas
    assert set(metrics.keys()) == {"rmse", "mae", "r2"}

    # Como el modelo es perfecto, esperamos métricas ideales
    assert pytest.approx(metrics["rmse"], 0.01) == 0.0
    assert pytest.approx(metrics["mae"], 0.01) == 0.0
    assert pytest.approx(metrics["r2"], 0.01) == 1.0
