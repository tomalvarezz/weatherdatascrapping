# schemas/city_request.py

from pydantic import BaseModel
from typing import List

class CityRequest(BaseModel):
    cities: List[str]
