FROM python:3.9-slim

WORKDIR /app

# Copy only necessary files first for caching
COPY setup.py requirements.txt pyproject.toml README.md /app/

# Copy source code before installing
COPY deepshell /app/deepshell
COPY docs /app/docs

<<<<<<< HEAD
# Copy entrypoint script and make it executable
=======
# Copy entrypoint script
>>>>>>> 399a905 (Dcokerfile fixed)
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install .

RUN useradd -m deepshelluser
USER deepshelluser

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["--help"]
