# Use official Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy only necessary files first for better caching
COPY setup.py requirements.txt pyproject.toml README.md /app/

# Install build tools and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install .

# Copy the rest of the project files
COPY deepshell /app/deepshell
COPY docs /app/docs

# Create a non-root user and switch to it
RUN useradd -m deepshelluser
USER deepshelluser

# Set default command to run deepshell CLI
ENTRYPOINT ["deepshell"]
CMD ["--help"]
