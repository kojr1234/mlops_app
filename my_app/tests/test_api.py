from my_app.config import settings
from my_app.schemas import Health
from classifier_model import __version__ as model_version
from my_app import __version__
from fastapi.testclient import TestClient
from loguru import logger

def test_api_health_output(client: TestClient) -> None:
    response = client.get(
        'http://localhost:8001/api/v1/health'
    )

    status_code = response.status_code
    response_dict = response.json()

    logger.info(f"Test health: request status code: {status_code}")

    assert status_code == 200
    assert response_dict.get('api_version') == __version__
    assert response_dict.get('model_version') == model_version