from pydantic import BaseModel
from typing import List


# ==========================================
# LIST FILES
# ==========================================

class ListFilesArgs(BaseModel):
    pass


# ==========================================
# READ FILE
# ==========================================

class ReadFileArgs(BaseModel):
    path: str


# ==========================================
# WRITE FILE
# ==========================================

class WriteFileArgs(BaseModel):
    relative_path: str
    content: str


# ==========================================
# GREP
# ==========================================

class GrepArgs(BaseModel):
    text: str


# ==========================================
# SEARCH CODE
# ==========================================

class SearchCodeArgs(BaseModel):
    query: str


# ==========================================
# PATCHES
# ==========================================

class FilePatch(BaseModel):
    path: str
    content: str


class ApplyPatchArgs(BaseModel):
    patches: List[FilePatch]