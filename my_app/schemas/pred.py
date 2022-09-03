from typing import Any, Optional

from classifier_model.preprocessing.data_validation import (
    SpaceshipTitanicDataInputSchema,
)
from pydantic import BaseModel


class ModelOutput(BaseModel):
    predictions: Optional[list[int]]
    version: str
    errors: Optional[Any]


class MulitpleSpaceshipTitanicInput(BaseModel):
    inputs: list[SpaceshipTitanicDataInputSchema]

    # this class comes out of the box with pydantic BaseModel
    class Config:
        # the schema_extra example here
        # is used for placeholder default in
        # our api docs
        # the schema_extra allows to exnted
        # or override the already existent
        # json schema using the key examples
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "PassengerId": "5323_01",
                        "HomePlanet": "Mars",
                        "CryoSleep": True,
                        "Cabin": "F/1091/P",
                        "Destination": "TRAPPIST-1e",
                        "Age": 38.0,
                        "VIP": False,
                        "RoomService": 0.0,
                        "FoodCourt": 0.0,
                        "ShoppingMall": 0.0,
                        "Spa": None,
                        "VRDeck": 0.0,
                        "Name": "Coakey Cort"
                        # Transported: True
                    }
                ]
            }
        }
