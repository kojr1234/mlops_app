import json

from typing import AnyStr

import numpy as np
import pandas as pd

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger

from classifier_model import __version__ as model_version
from classifier_model.predict import make_prediction

from my_app import __version__, schemas

from my_app.config import settings

api_router = APIRouter()

@api_router.get('/health', response_model=schemas.Health, status_code=200)
def health() -> dict:
    """
    Root get
    """
    health = schemas.Health(
        name=settings.PROJECT_NAME,
        api_version=__version__,
        model_version=model_version
    )

    return health.dict()