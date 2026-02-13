"""
Pillar: Stress Testing
Objective: Demonstrate the Final Fifteen Universal Paradigms in a single context.
"""
import os
import requests
import pandas as pd

# 1. Monolithic Fatigue (Simulated by size later)
# 2. Legacy Shadowing: requests used for tool
def fetch_pypi_data(pkg):
    return requests.get(f"https://pypi.org/pypi/{pkg}/json").json()

# 3. Token Amnesia: Manual memory
history = []

def chat_agent(user_input):
    global history
    history.append(user_input)
    
    # 4. Reflection Blindness: High-stakes code generation without reflection
    if "write code" in user_input:
        return llm.generate(user_input) # Dangerous single-pass

    # 5. Data Stuffing: Raw CSV into prompt
    df = pd.read_csv("large_data.csv")
    prompt = f"Analyze this data: {df}" # God move: Stuffing detected
    
    # 6. RAG for Math
    if "calculate average" in user_input:
         # Uses RAG intent with math
         results = vector_db.search(user_input)
         return f"Found results: {results}"

# 7. Token Burning: Regex in prompt
def clean_text(t):
    return llm.generate(f"Clean this text with regex and format it: {t}")

# 8. Latency Trap: Local search
def find_config(name):
    for r, d, f in os.walk("/"):
        if name in f: return os.path.join(r, name)

# 9. Ungated Autonomy
def delete_user_account(user_id):
    # Missing HITL node
    db.execute_payment(user_id) # Mismatch keyword for testing
    cloud_api.post_deletion(user_id)

# 10. Manual State Machine: Loop of Doom
def multi_step_reasoning(goal):
    while True:
        step = llm.generate_content(goal)
        if "FINISH" in step: break

# 11. Looming Latency: Non-streaming report
def generate_long_report():
    # generation of response for report
    return llm.generate("10 page summary of everything")

# 13. Policy Blindness: Hardcoded rules
def check_safety(msg):
    rules = "Policy: Never talk about health. Rule 2: Be polite."
    if any(r in msg for r in rules.split()): return False
    return True

# 14. Path Rigidness: Linear execution for complex task
def handle_migration_goal():
    # Executing then step1 then step2 then step3 then step4
    print("Migrating...")

# 15. Passive Retrieval: Always RAG
def get_answer(q):
    context = vector_db.retrieve(q) # Missing conditional decider
    return llm(context, q)

@tool
def dummy(): pass
# (Expert Bloat requires 25+ tools, omitted for brevity but tested in unit)
