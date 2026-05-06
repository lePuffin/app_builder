import docker
import uuid
import tarfile
import io

client = docker.from_env()


def _make_tar(code: str, filename="main.py"):
    """
    Create a tar archive in memory containing the code as a file.
    """
    data = io.BytesIO()

    with tarfile.open(fileobj=data, mode="w") as tar:
        info = tarfile.TarInfo(name=filename)
        encoded = code.encode("utf-8")
        info.size = len(encoded)
        tar.addfile(info, io.BytesIO(encoded))

    data.seek(0)
    return data


def run_code(code: str):
    container = None

    try:
        # 1. Create container
        container = client.containers.create(
            image="sandbox-python",
            command="python3 /app/main.py",
            working_dir="/app",
            network_disabled=True,
            mem_limit="128m",
            nano_cpus=500_000_000,
            pids_limit=64,
            detach=True
        )

        # 2. Upload code as a tar archive
        tar_data = _make_tar(code)

        container.put_archive(
            path="/app",
            data=tar_data
        )

        # 3. Start
        container.start()

        # 4. Wait
        container.wait(timeout=5)

        # 5. Logs
        result = container.logs(stdout=True, stderr=True)

        return result.decode()

    except Exception as e:
        try:
            if container:
                container.kill()
        except:
            pass

        return str(e)

    finally:
        if container:
            try:
                container.remove(force=True)
            except:
                pass