# AgentOps Cockpit v1.3.1: Audit Scenarios & Capabilities

This document showcases the difference between "Heuristic Matching" (v0.9) and "Reasoning-Based Auditing" (v1.3) using the new AST and Semantic Graph Probing engines.

---

## 🟢 Scenario 1: The "Lazy" PII Masking (Simple)

### The Code
```python
# agent.py
user_input = get_user_query()
# TODO: implement PII mask
response = llm.invoke(user_input)
```

### ❌ Old v0.9 Auditor Result
*   **Status:** `PASSED`
*   **Rationale:** Found keyword "mask" in comments.
*   **Verdict:** Dangerous false positive.

### ✅ New v1.0 Auditor (Reasoning)
*   **Status:** `FAIL (CRITICAL)`
*   **Finding:** `Incomplete PII Protection`
*   **Reasoning:** 
    1.  AST analysis identifies `user_input` as a raw variable.
    2.  No call to a "scrubber" function detected between variable assignment and LLM `invoke`.
    3.  Semantic scanner identifies "TODO" comment as an active risk rather than a feature.
*   **ADR Recommendation:** Inject `google-adk` PII Scrubber before `llm.invoke`.

---

## 🟡 Scenario 2: The "Thundering Herd" Bottleneck (Medium)

### The Code
```python
async def get_data():
    user = await db.get_user()
    history = await db.get_history()
    profile = await db.get_profile()
    return user, history, profile
```

### ❌ Old v0.9 Auditor Result
*   **Status:** `PASSED`
*   **Rationale:** Code is valid Python/Async.
*   **Verdict:** Ignores performance anti-patterns.

### ✅ New v1.0 Auditor (Reasoning)
*   **Status:** `FAIL (MEDIUM IMPACT)`
*   **Finding:** `Sequential Bottleneck Detected`
*   **Reasoning:** 
    1.  AST walker identifies 3+ `await` calls in a direct sequence.
    2.  Analyzes child nodes to determine these are independent data fetches.
*   **Strategic ROI:** "Current latency is `T1 + T2 + T3`. Parallelizing via `asyncio.gather` reduces latency to `MAX(T1, T2, T3)`, improving responsiveness by ~60%."

---

## 🔴 Scenario 3: Cross-Framework Conflict (Complex)

### The Code
```python
from langgraph.graph import StateGraph
from crewai import Agent, Task, Crew

# ... logic using a CrewAI Agent as a node in a LangGraph State machine ...
```

### ❌ Old v0.9 Auditor Result
*   **Status:** `PASSED`
*   **Rationale:** Found keywords "langgraph" and "crewai".
*   **Verdict:** Both frameworks are supported, so audit passes.

### ✅ New v1.0 Auditor (Reasoning)
*   **Status:** `WARNING (ARCHITECTURAL CONFLICT)`
*   **Finding:** `Orchestration Overlap`
*   **Reasoning:** 
    1.  Graph analysis detects two competing "Loop Managers" (LangGraph and CrewAI).
    2.  Identifies high risk of **Cyclic State Deadlock** where the LangGraph state and CrewAI internal state diverge.
*   **Consulting Edge:** "You are attempting to manage state in two places. Recommend refactoring CrewAI agents into raw `tools` within LangGraph or using CrewAI in a purely sequential sub-task mode."

---

## 🏆 Scenario 4: The "Silent" Model Waste (FinOps)

### The Code
```python
# process_batch.py
results = []
for item in large_dataset:
    # Processing simple classification
    res = gemini_pro.generate_content(f"Is this category A or B: {item}")
    results.append(res)
```

### ✅ New v1.0 Auditor (Reasoning)
*   **Finding:** `High-Tier Model Inefficiency`
*   **Reasoning:** 
    1.  Detects `gemini-1.5-pro` (High Performance/Cost) inside a `for-loop`.
    2.  Semantic analyzer determines the task is "simple classification" based on the prompt string prefix.
*   **Business Impact:** "You are using a sledgehammer for a nail. Switching this loop to `gemini-1.5-flash` will reduce monthly token spend from $400 to $40 with zero accuracy loss."
