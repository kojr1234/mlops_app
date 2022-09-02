
from email.generator import Generator
import pandas as pd
import pytest

from fastapi.testclient import TestClient

from classifier_model.config.core import config
from classifier_model.preprocessing.data_manager import load_dataset

from my_app.main import app

@pytest.fixture(scope='module')
def test_data() -> pd.DataFrame:
    return load_dataset(file_name=config.app_config.test_data)

@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as _client:
        yield _client
        app.dependency_overrides = {}
