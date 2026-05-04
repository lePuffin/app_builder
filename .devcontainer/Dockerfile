# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.14-trixie

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install additional OS packages.
WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir uv

# Install Python dependencies in requirements.txt
COPY pyproject.toml /workspace/pyproject.toml
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install .

ENV PATH="/workspace/.venv/bin:$PATH"

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /workspace
USER appuser

WORKDIR /workspace/src

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "src/main.py"]
