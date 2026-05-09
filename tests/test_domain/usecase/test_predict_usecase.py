from unittest.mock import MagicMock
import pytest
from src.boston_housing.domain.model.housing.model import Model
from src.boston_housing.domain.usecase.predict_usecase import PredictUseCase

def test_predict_use_case_with_mock_model():
    mock_model = MagicMock()
    mock_model.scale_features.return_value = [10.0, 20.0, 30.0]
    mock_model.predict.return_value = [11.0, 21.0, 31.0]

    use_case = PredictUseCase(mock_model)
    features = [1.0, 2.0, 3.0]
    prediction = use_case.predict(features)

    assert prediction == [11.0, 21.0, 31.0]
    mock_model.scale_features.assert_called_once_with(features)
    mock_model.predict.assert_called_once_with([10.0, 20.0, 30.0])