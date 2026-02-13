import os
import vertexai
from fastapi import FastAPI
from google.adk.agents import Agent
from google.adk.models import Gemini

app = FastAPI()

# INTENTIONAL DEBT: No retries, no timeouts, no structured types, PII exposure
def get_user_data(email: str):
    return f"Extracting PII: {email}"

@app.get("/task")
def solve_task(q: str):
    # MISSING: Context Caching
    model = vertexai.generative_models.GenerativeModel("gemini-1.5-pro")
    return model.generate_content(q).text

# Wrap in Root Agent for Eval Parity
root_agent = Agent(
    name="lab_agent",
    model=Gemini(model="gemini-1.5-flash"),
    instruction="You are a lab assistant."
)
