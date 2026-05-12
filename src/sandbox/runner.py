import docker
import tarfile
import io
from pathlib import Path

client = docker.from_env()


def _workspace_to_tar(workspace_path):

    data = io.BytesIO()

    with tarfile.open(fileobj=data, mode="w") as tar:

        for file_path in workspace_path.rglob("*"):

            if file_path.is_file():

                relative = file_path.relative_to(workspace_path)

                tar.add(file_path, arcname=str(relative))

    data.seek(0)

    return data


def run_project(
    workspace_path,
    entrypoint="main.py",
    dependencies=None
):
    
    dependencies = dependencies or []

    container = None

    try:

        # ==========================================
        # CREATE CONTAINER
        # ==========================================

        container = client.containers.create(
            image="sandbox-python",
            command="tail -f /dev/null",
            working_dir="/app",
            network_disabled=False,
            mem_limit="256m",
            nano_cpus=1_000_000_000,
            pids_limit=128,
            detach=True
        )

        # ==========================================
        # UPLOAD PROJECT
        # ==========================================

        tar_data = _workspace_to_tar(
            workspace_path
        )

        container.put_archive(
            "/app",
            tar_data
        )

        # ==========================================
        # START CONTAINER
        # ==========================================

        container.start()

        container.reload()

        print("container status:", container.status)

        # ==========================================
        # INSTALL DEPENDENCIES
        # ==========================================

        if dependencies:

            deps = " ".join(dependencies)

            install = container.exec_run(
                f"pip install --no-cache-dir {deps}",
                demux=True
            )

            stdout = (
                install.output[0].decode()
                if install.output[0]
                else ""
            )

            stderr = (
                install.output[1].decode()
                if install.output[1]
                else ""
            )

            if install.exit_code != 0:

                return {
                    "stdout": stdout,
                    "stderr": stderr,
                    "exit_code": install.exit_code,
                    "success": False
                }
            
        # ==========================================
        # EXECUTE PROJECT
        # ==========================================

        execution = container.exec_run(
            f"python3 /app/{entrypoint}",
            demux=True
        )

        stdout = (
            execution.output[0].decode()
            if execution.output[0]
            else ""
        )

        stderr = (
            execution.output[1].decode()
            if execution.output[1]
            else ""
        )

        return {
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": execution.exit_code,
            "success": execution.exit_code == 0
        }


    except Exception as e:

        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": 1,
            "success": False
        }

    finally:

        if container:
            try:
                container.remove(force=True)
            except:
                pass