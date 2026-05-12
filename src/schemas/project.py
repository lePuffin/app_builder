from pydantic import BaseModel
from typing import List


class ProjectFile(BaseModel):
    path: str
    content: str


class GeneratedProject(BaseModel):
    files: List[ProjectFile]
    entrypoint: str
    dependencies: List[str] = []