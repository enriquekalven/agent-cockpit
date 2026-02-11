# Use a slim Python image
FROM python:3.12-slim

# Install system dependencies and uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Mount the package cache to speed up installs and install dependencies
RUN uv sync --frozen --no-dev

# Copy the rest of the application
COPY . .

# Ensure the app directory is in the PYTHONPATH
ENV PYTHONPATH=/app

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
# We use uvicorn to serve the FastAPI app defined in app/agent.py
CMD ["uv", "run", "uvicorn", "app.agent:app", "--host", "0.0.0.0", "--port", "8080"]
