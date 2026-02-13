from google.adk.agents import Agent
from google.adk.apps import App

root_agent = Agent(
    name="root_agent",
    model="gemini-1.5-pro",
    instruction="You are a helpful assistant."
)

adk_app = App(root_agent=root_agent, name="my_app")

