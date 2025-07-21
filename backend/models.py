from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

# Response models
class TeamBuilderResponse(BaseModel):
    status: str
    message: str
    budget: Optional[float] = None

# Product categories enum
class ProductCategory(str, Enum):
    electronics = "Electronics"
    audio = "Audio"
    furniture = "Furniture"
    wearables = "Wearables"
    displays = "Displays"
    accessories = "Accessories"
    storage = "Storage"
    peripherals = "Peripherals"

# Product model
class Product(BaseModel):
    id: int
    name: str
    price: int
    rating: float
    description: Optional[str] = None
    category: Optional[ProductCategory]
    value: Optional[float] = None

# Response models
class TeamBuilderResponse(BaseModel):
    status: str
    message: str
    budget: Optional[float] = None
    products: Optional[List[Product]] = None

class NotFoundException(BaseModel):
    """
    Not Found Exception
    """
    status_code: Optional[int] = 404
    message: Optional[str] = "Resource Not Found"
