from pydantic import BaseModel
from typing import Optional

# Response models
class TeamBuilderResponse(BaseModel):
    status: str
    message: str
    budget: Optional[float] = None