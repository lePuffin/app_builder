FROM python:3.14-trixie

# Non-root user for security
RUN useradd -m sandboxuser

# Working directory
WORKDIR /app

# Useful for debugging and logs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Dependencies
RUN pip install --no-cache-dir pytest && \
    rm -rf /home/sandboxuser/.cache

# Change to the non-root user
USER sandboxuser

CMD ["python3"]