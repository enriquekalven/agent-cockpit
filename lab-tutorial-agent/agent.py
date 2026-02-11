import os
from fastapi import FastAPI

app = FastAPI(title="Lab Agent")

class LabAgent:
    def __init__(self):
        self.name = "lab-agent"

    def solve_task(self, prompt: str) -> str:
        # ❌ PROBLEM 1: No Resiliency. If this fails, the whole agent crashes. (Missing @retry)
        # ❌ PROBLEM 2: Mixed Logic. Returning HTML directly.
        return f"<html><body><h1>Lab Result</h1><p>Processed: {prompt}</p></body></html>"

agent = LabAgent()

@app.post("/chat")
async def chat(text: str):
    # ❌ PROBLEM 3: No Input Sanitization/PII Check.
    return {"response": agent.solve_task(text)}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
