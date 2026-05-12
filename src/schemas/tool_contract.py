from typing import Callable
from pydantic import BaseModel


class ToolDefinition(BaseModel):

    name: str

    description: str

    function: Callable

    model: type[BaseModel]

    schema: dict

    class Config:
        arbitrary_types_allowed = True