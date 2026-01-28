FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/

# Set PYTHONPATH so it can find the modules
ENV PYTHONPATH=/app/src

CMD ["python", "src/backend/agent.py"]
