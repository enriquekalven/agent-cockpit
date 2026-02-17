FROM python:3.11-slim

# Create a non-root user for security alignment (v1.8.2)
RUN groupadd -r agentuser && useradd -r -g agentuser agentuser

WORKDIR /app

# Ensure correct permissions for the cockpit evidence lake
RUN mkdir -p .cockpit && chown -R agentuser:agentuser .cockpit

COPY pyproject.toml .
COPY requirements.txt .
COPY cockpit.yaml .
RUN pip install -r requirements.txt

COPY src/ ./src/
RUN chown -R agentuser:agentuser /app

# Set PYTHONPATH so it can find the modules
ENV PYTHONPATH=/app/src

USER agentuser

# Run mandatory AgentOps Audit during build
RUN python -m agent_ops_cockpit.ops.orchestrator --mode quick --target src/agent_ops_cockpit

CMD ["python", "src/agent_ops_cockpit/agent.py"]
