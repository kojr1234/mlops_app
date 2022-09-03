from pydantic import BaseModel


class PerformanceCheck(BaseModel):
    model_version: str
    metric_name: str
    metric_val: float
