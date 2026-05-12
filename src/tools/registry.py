from tools.file_tools import FileTools
from tools.schema_utils import pydantic_to_tool
from schemas.tool_contract import ToolDefinition

from schemas.tool_contract import (
    ToolDefinition
)

from schemas.tools import (
    ListFilesArgs,
    ReadFileArgs,
    WriteFileArgs,
    GrepArgs,
    SearchCodeArgs,
    ApplyPatchArgs
)


class ToolRegistry:

    def __init__(
        self,
        workspace_manager,
        workspace_path
    ):

        self.file_tools = FileTools(
            workspace_manager,
            workspace_path
        )

    # ==========================================
    # TOOLS
    # ==========================================

    def get_tools(self):

        return {

            # ======================================
            # LIST FILES
            # ======================================

            "list_files": ToolDefinition(

                name="list_files",

                description=(
                    "List all files in workspace"
                ),

                function=self.file_tools.list_files,

                model=ListFilesArgs,

                schema=pydantic_to_tool(
                    ListFilesArgs,
                    "list_files",
                    "List all files in workspace"
                )
            ),

            # ======================================
            # READ FILE
            # ======================================

            "read_file": ToolDefinition(

                name="read_file",

                description=(
                    "Read a file from workspace"
                ),

                function=self.file_tools.read_file,

                model=ReadFileArgs,

                schema=pydantic_to_tool(
                    ReadFileArgs,
                    "read_file",
                    "Read a file from workspace"
                )
            ),

            # ======================================
            # WRITE FILE
            # ======================================

            "write_file": ToolDefinition(

                name="write_file",

                description=(
                    "Write or create file"
                ),

                function=self.file_tools.write_file,

                model=WriteFileArgs,

                schema=pydantic_to_tool(
                    WriteFileArgs,
                    "write_file",
                    "Write or create file"
                )
            ),

            # ======================================
            # APPLY PATCH
            # ======================================

            "apply_patch": ToolDefinition(

                name="apply_patch",

                description=(
                    "Apply patches to project"
                ),

                function=self.file_tools.apply_patch,

                model=ApplyPatchArgs,

                schema=pydantic_to_tool(
                    ApplyPatchArgs,
                    "apply_patch",
                    "Apply patches to project"
                )
            ),

            # ======================================
            # GREP
            # ======================================

            "grep": ToolDefinition(

                name="grep",

                description=(
                    "Search text in workspace"
                ),

                function=self.file_tools.grep,

                model=GrepArgs,

                schema=pydantic_to_tool(
                    GrepArgs,
                    "grep",
                    "Search text in workspace"
                )
            ),

            # ======================================
            # SEARCH CODE
            # ======================================

            "search_code": ToolDefinition(

                name="search_code",

                description=(
                    "Search code patterns"
                ),

                function=self.file_tools.search_code,

                model=SearchCodeArgs,

                schema=pydantic_to_tool(
                    SearchCodeArgs,
                    "search_code",
                    "Search code patterns"
                )
            )
        }