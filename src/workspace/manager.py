from pathlib import Path
import uuid
import shutil


BASE_DIR = Path("./workspaces")


class WorkspaceManager:

    def create(self):

        workspace_id = str(uuid.uuid4())

        path = BASE_DIR / workspace_id

        path.mkdir(parents=True, exist_ok=True)

        return {
            "id": workspace_id,
            "path": path
        }

    def write_project(self, workspace_path, project):

        for file in project["files"]:

            file_path = workspace_path / file["path"]

            file_path.parent.mkdir(parents=True, exist_ok=True)

            file_path.write_text(file["content"], encoding="utf-8")

    def read_project(self, workspace_path):

        files = []

        for path in workspace_path.rglob("*"):

            if path.is_file():

                relative = path.relative_to(workspace_path)

                files.append({
                    "path": str(relative),
                    "content": path.read_text(encoding="utf-8")
                })

        return files

    def update_file(self, workspace_path, relative_path, content):

        file_path = workspace_path / relative_path

        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_text(content, encoding="utf-8")

    def delete(self, workspace_path):

        shutil.rmtree(workspace_path, ignore_errors=True)


    def list_files(self, workspace_path):

        return [
            str(p.relative_to(workspace_path))
            for p in workspace_path.rglob("*")
            if p.is_file()
        ]

    def grep(self, workspace_path, text):

        matches = []

        for path in workspace_path.rglob("*"):

            if not path.is_file():
                continue

            try:
                content = path.read_text(encoding="utf-8")
            except:
                continue

            if text in content:
                matches.append(str(path.relative_to(workspace_path)))

        return matches

    def apply_patch(self, workspace_path, patches):

        for patch in patches:

            file_path = workspace_path / patch["path"]

            file_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            file_path.write_text(
                patch["content"],
                encoding="utf-8"
            )