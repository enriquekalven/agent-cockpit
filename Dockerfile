FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/

# Set PYTHONPATH so it can find the modules
ENV PYTHONPATH=/app/src

# Run mandatory AgentOps Audit during build
RUN python src/agent_ops_cockpit/ops/orchestrator.py --mode quick

CMD ["python", "src/agent_ops_cockpit/agent.py"]
