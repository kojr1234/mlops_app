import json
from typing import Any

import numpy as np
import pandas as pd
from classifier_model import __version__ as model_version
from classifier_model.predict import make_prediction
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger

from my_app import __version__, schemas
from my_app.config import settings

# the APIRouter is used to give fastapi flexibility of having
# different files with routers, instead of writing all endpoints
# in main.py
api_router = APIRouter()


@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """
    Root get
    """
    health = schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version, my_text="This app was deployed via Docker"
    )

    return health.dict()


# Removing performance because this shouldnt be here
# (this should be evaluated on the model development)
# @api_router.get(
#     "/performance", response_model=schemas.PerformanceCheck, status_code=200
# )
# def performance() -> dict:
#     """
#     Get models performance
#     """
#     from classifier_model.config.core import config
#     from classifier_model.predict import make_prediction
#     from classifier_model.preprocessing.data_manager import load_dataset
#     from sklearn.metrics import accuracy_score

#     test_df = load_dataset(file_name=config.app_config.test_data)

#     results = make_prediction(input_data=test_df)

#     if not results["errors"]:
#         preds = results["predictions"]
#         val = accuracy_score(test_df[config.model_config.target], preds)

#     perf = schemas.PerformanceCheck(
#         model_version=model_version,
#         metric_name=config.model_config.metric,
#         metric_val=val,
#     )

#     return perf.dict()


@api_router.post("/predict", response_model=schemas.ModelOutput, status_code=200)
def predict(*, input_data: schemas.MulitpleSpaceshipTitanicInput) -> Any:

    input_data = pd.DataFrame(jsonable_encoder(input_data.inputs)).replace(
        {np.nan: None}
    )
    results = make_prediction(input_data=input_data)
    results["predictions"] = results["predictions"].astype(int).tolist()
    if results["errors"] is not None:
        logger.warning(f"Prediction validation error: {results.get('errors')}")
        raise HTTPException(status_code=400, detail=json.loads(results["errors"]))

    logger.info(f"Prediction results: {results.get('predictions')}")

    return results
