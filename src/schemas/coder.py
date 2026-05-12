from pydantic import BaseModel
from typing import List, Optional


class GeneratedCode(BaseModel):
    code: str
    dependencies: List[str] = []
    entrypoint: str = "main.py"


class FilePatch(BaseModel):
    path: str
    content: str


class DebuggedProject(BaseModel):
    files: List[FilePatch]
    summary: Optional[str] = None


class TestSuite(BaseModel):
    test_code: str


class RefactoredCode(BaseModel):
    code: str
    summary: Optional[str] = None


class DependencyResolution(BaseModel):
    dependencies: List[str]