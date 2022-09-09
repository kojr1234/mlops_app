from typing import Generator

import pandas as pd
import pytest
from classifier_model.config.core import config
from classifier_model.preprocessing.data_manager import load_dataset
from classifier_model.preprocessing.get_data import download_data
from classifier_model.split_data import split_train_test_data
from fastapi.testclient import TestClient

from my_app.main import app


@pytest.fixture(scope="module")
def test_data() -> pd.DataFrame:
    download_data()
    split_train_test_data()
    return load_dataset(file_name=config.app_config.test_data)


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as _client:
        yield _client
        app.dependency_overrides = {}
