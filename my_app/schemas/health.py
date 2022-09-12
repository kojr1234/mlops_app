from pydantic import BaseModel
from typing import Optional

class Health(BaseModel):
    name: str
    api_version: str
    model_version: str
    my_text: Optional[str]
