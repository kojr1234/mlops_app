import numpy as np
import pandas as pd
from classifier_model import __version__ as model_version
from classifier_model.config.core import config
from fastapi.testclient import TestClient
from loguru import logger

from my_app import __version__


def test_api_health_output(client: TestClient) -> None:
    response = client.get("http://localhost:8001/api/v1/health")

    status_code = response.status_code
    response_dict = response.json()

    logger.info(f"Test health: request status code: {status_code}")

    assert status_code == 200
    assert response_dict.get("api_version") == __version__
    assert response_dict.get("model_version") == model_version


def test_api_performance_output(client: TestClient) -> None:
    response = client.get("http://localhost:8001/api/v1/performance")

    status_code = response.status_code
    response_dict = response.json()

    logger.info(f"Test performance: request status code: {status_code}")

    assert status_code == 200
    assert response_dict.get("model_version") == model_version
    assert response_dict.get("metric_name") == config.model_config.metric
    assert response_dict.get("metric_val") >= 0.75


def test_api_prediction(client: TestClient, test_data: pd.DataFrame):

    payload = {"inputs": test_data.replace({np.nan: None}).to_dict(orient="records")}

    logger.debug(payload)

    response = client.post("http://localhost:8001/api/v1/predict", json=payload)

    response_dict = response.json()

    assert response.status_code == 200
    assert not response_dict.get("errors")
    assert response_dict["predictions"][0] == 1
