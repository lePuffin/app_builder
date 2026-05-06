from pydantic import BaseModel
from typing import Literal, Optional


class Evaluation(BaseModel):
    status: Literal["success", "retry"]
    error: Optional[str] = None