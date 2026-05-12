import re

from schemas.tool_result import ToolResult


class FileTools:

    def __init__(
        self,
        workspace_manager,
        workspace_path
    ):

        self.workspace = workspace_manager
        self.workspace_path = workspace_path

    # ==========================================
    # FILESYSTEM
    # ==========================================

    def list_files(self):

        try:

            files = self.workspace.list_files(
                self.workspace_path
            )

            return ToolResult(
                success=True,
                data=files
            ).model_dump()

        except Exception as e:

            return ToolResult(
                success=False,
                error=str(e)
            ).model_dump()

    def read_file(self, path):

        try:
            
            print(f"📂 reading file: {path}")

            content = self.workspace.read_file(
                self.workspace_path,
                path
            )

            return ToolResult(
                success=True,
                data=content
            ).model_dump()

        except Exception as e:

            return ToolResult(
                success=False,
                error=str(e)
            ).model_dump()

    def write_file(
        self,
        relative_path,
        content
    ):

        try:

            path = (
                self.workspace_path
                / relative_path
            )

            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            path.write_text(
                content,
                encoding="utf-8"
            )

            return ToolResult(
                success=True,
                data={
                    "path": relative_path
                }
            ).model_dump()

        except Exception as e:

            return ToolResult(
                success=False,
                error=str(e)
            ).model_dump()

    def apply_patch(self, patches):

        try:

            normalized = []

            for patch in patches:

                if hasattr(
                    patch,
                    "model_dump"
                ):

                    normalized.append(
                        patch.model_dump()
                    )

                else:
                    normalized.append(
                        patch
                    )

            self.workspace.apply_patch(
                self.workspace_path,
                normalized
            )

            return ToolResult(
                success=True,
                data={
                    "patched_files": len(
                        normalized
                    )
                }
            ).model_dump()

        except Exception as e:

            return ToolResult(
                success=False,
                error=str(e)
            ).model_dump()

    # ==========================================
    # SEARCH
    # ==========================================

    def grep(self, text):

        try:

            result = self.workspace.grep(
                self.workspace_path,
                text
            )

            return ToolResult(
                success=True,
                data=result
            ).model_dump()

        except Exception as e:

            return ToolResult(
                success=False,
                error=str(e)
            ).model_dump()

    def search_code(self, query):

        try:

            matches = []

            for path in self.workspace_path.rglob("*.py"):

                content = path.read_text(
                    encoding="utf-8"
                )

                if re.search(
                    query,
                    content,
                    re.IGNORECASE
                ):

                    matches.append({
                        "path": str(
                            path.relative_to(
                                self.workspace_path
                            )
                        )
                    })

            return ToolResult(
                success=True,
                data=matches
            ).model_dump()

        except Exception as e:

            return ToolResult(
                success=False,
                error=str(e)
            ).model_dump()