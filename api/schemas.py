# api/schemas.py
from pydantic import BaseModel
from typing import Optional

class PredictRequest(BaseModel):
    category: str

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "category": "Furniture"
            }]
        }
    }

class PredictResponse(BaseModel):
    category: str
    predicted_sales: float
    model_used: str