# AgentOps Cockpit v2.0.2: Audit Scenarios & Capabilities

This document showcases the difference between "Heuristic Matching" (Legacy) and **"Reasoning-Based Auditing" (v2.0.2)** using the new AST and Sovereign SME Probing engines.

---

## 🟢 Scenario 1: The "Lazy" PII Masking (Security SME)

### The Code
```python
# agent.py
user_input = get_user_query()
# TODO: implement PII mask
response = llm.invoke(user_input)
```

### ❌ Legacy Auditor Result
*   **Status:** `PASSED`
*   **Rationale:** Found keyword "mask" in comments.
*   **Verdict:** Dangerous false positive.

### ✅ v2.0.2 Governing Board (Security Persona)
*   **Status:** `FAIL (CRITICAL)`
*   **Finding:** `Incomplete PII Protection (Guardian Gap)`
*   **Reasoning:** 
    1.  **AST Analysis**: Identifies `user_input` as a raw variable passing directly to an LLM node.
    2.  **Logic Trace**: No call to a "scrubber" or **Sovereign Gateway** sidecar detected.
    3.  **Semantic Context**: Identifies "TODO" comment as an active risk rather than a feature.
*   **Remediation**: Inject `agent-ops-gateway` PII Scrubber before `llm.invoke`.

---

## 🟡 Scenario 2: The "Thundering Herd" (SRE SME)

### The Code
```python
async def get_data():
    user = await db.get_user()
    history = await db.get_history()
    profile = await db.get_profile()
    return user, history, profile
```

### ❌ Legacy Auditor Result
*   **Status:** `PASSED`
*   **Rationale:** Valid Python/Async syntax.
*   **Verdict:** Ignores performance anti-patterns.

### ✅ v2.0.2 Governing Board (SRE Persona)
*   **Status:** `FAIL (MEDIUM IMPACT)`
*   **Finding:** `Sequential Bottleneck Detected`
*   **Reasoning:** 
    1.  **AST Pattern**: Identifies 3+ `await` calls in a direct sequence.
    2.  **Dependency Graph**: Determines these are independent data fetches from a shared source.
*   **Strategic ROI**: "Current latency is `T1+T2+T3`. Parallelizing via `asyncio.gather` reduces latency to `MAX(T1, T2, T3)`, improving UI responsiveness by ~60%."

---

## 🔴 Scenario 3: Architectural "Split Brain" (Architect SME)

### The Code
```python
from langgraph.graph import StateGraph
from crewai import Agent, Task, Crew

# ... logic using a CrewAI Agent as a node in a LangGraph State machine ...
```

### ❌ Legacy Auditor Result
*   **Status:** `PASSED`
*   **Rationale:** Both frameworks are supported.
*   **Verdict:** Ignores structural fragility.

### ✅ v2.0.2 Governing Board (Architect Persona)
*   **Status:** `WARNING (ARCHITECTURAL CONFLICT)`
*   **Finding:** `Orchestration Overlap (Split Brain)`
*   **Reasoning:** 
    1.  **Graph Analysis**: Detects two competing "Loop Managers" (LangGraph and CrewAI).
    2.  **Risk Profile**: Identifies high risk of **Cyclic State Deadlock** where internal states will eventually diverge.
*   **Consulting Edge**: "Single-point-of-truth violation. Recommend refactoring CrewAI agents into raw `tools` within LangGraph or using the **ADK Unified Runner**."

---

## 🏆 Scenario 4: The "Silent" Model Waste (FinOps SME)

### The Code
```python
# process_batch.py
for item in large_dataset:
    # Processing simple classification
    res = gemini_pro.generate_content(f"Is this category A or B: {item}")
```

### ✅ v2.0.2 Governing Board (FinOps Persona)
*   **Finding:** `High-Tier Model Inefficiency (Strategic Debt)`
*   **Reasoning:** 
    1.  **Iterative Pattern**: Detects high-cost `gemini-1.5-pro` usage inside a large loop.
    2.  **Prompt Analysis**: Determines the task is "simple classification" (low reasoning complexity).
*   **Business Impact**: "Using a sledgehammer for a nail. Switching this loop to `gemini-1.5-flash` reduces monthly token spend by **90%** with zero accuracy loss."
