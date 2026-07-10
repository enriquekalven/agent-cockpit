# 🦴 Dogfooding: The AgentOps Cockpit Fleet Audit (v2.0.17)

We are recruiting active agent developers to "Dogfood" the **AgentOps Cockpit**. Our goal is to test the **Master Audit Suite** against real-world agent codebases and swarms to refine our SME reasoning and auto-remediation patches.

---

### **🎯 The Challenge**
Run the Cockpit against your most complex agentic repository. We want to know:
1.  **Detection Quality**: Did our SMEs (SecOps, FinOps, Architect, Quality) find actual gaps in your code?
2.  **Remediation ROI**: Did `uvx agentops-cockpit evolve` generate a patch that you would actually merge?
3.  **Persona Fidelity**: Did the feedback from specific personas (like the **Red Team** or **RAG Truth-Sayer**) feel like expert advice?

---

### **🚀 Setup & Execution**

#### **Option A: The Portable Audit (Recommended)**
No installation required. Run this from the root of your agent's repository:
```bash
# 1. Quick Scan (Seconds)
uvx agentops-cockpit audit report --mode quick

# 2. Deep Intelligence Scan (Full Benchmarks)
uvx agentops-cockpit audit report --mode deep

# 3. Expertise Matrix (Check the Cockpit's Competency)
uvx agentops-cockpit audit maturity
```

#### **Option B: The Collaborative CLI**
If you want to apply fixes and use the interactive workbench:
```bash
pip install agentops-cockpit
uvx agentops-cockpit audit report --workspace --heal --sim
```

---

### **🧪 Testing Scenarios (Persona-Tailored)**

If you are a specialist, you can "Dogfood" specific lanes of the Cockpit:

#### **🛡️ For the SecOps Engineer (Red Team / Brand Safety)**
*   **Command**: `uvx agentops-cockpit audit report --only security` or `uvx agentops-cockpit audit security`
*   **Dogfood Focus**: Attempt to provoke a **Prompt Injection** or **PII Leak**. 
*   **Feedback**: Did the Red Team Auditor catch the attack? Is the severity ranking appropriate for enterprise risk?

#### **💰 For the FinOps Analyst (Economics & ROI)**
*   **Command**: `uvx agentops-cockpit audit report --only finops` or `uvx agentops-cockpit audit roi`
*   **Dogfood Focus**: Check the **Reasoning Density** of your LLM calls.
*   **Feedback**: Does the ROI Waterfall accurately reflect your model costs? Are the caching recommendations actionable?

#### **🧗 For the AI Quality SME (Evaluations & RAG)**
*   **Command**: `uvx agentops-cockpit audit report --only quality` or `uvx agentops-cockpit audit quality`
*   **Dogfood Focus**: Audit your **Vector Retrieval** and **Grounding Logic**.
*   **Feedback**: Did it detect missing citations or high-hallucination temperatures? Is the Hill Climbing feedback improving your prompts?

#### **🏛️ For the Autonomous Architect (SRE & Infrastructure)**
*   **Command**: `uvx agentops-cockpit audit report --only reliability` or `uvx agentops-cockpit audit arch`
*   **Dogfood Focus**: Scan for **Networking Debt** (e.g., REST vs gRPC) and **Cockpit Gates**.
*   **Feedback**: Did it identify race conditions in your NoSQL writes (Firestore/Spanner)? Is the CI/CD gate advice actually implementable?

#### **🎭 For the UX Designer (Face & A2UI)**
*   **Command**: `uvx agentops-cockpit audit report --only ux` or `uvx agentops-cockpit audit face`
*   **Dogfood Focus**: Audit your frontend for **A2UI Surface Compliance**.
*   **Feedback**: Is the GenUI readiness score accurate for mobile viewports? Are the interface micro-animations correctly categorized?

---

### **💬 Feedback Loop**
Please share your findings in the **GitHub Issues** or via a **SME Feedback Report**:
*   **Discord/Slack**: [Link to Community]
*   **Subject**: `Dogfooding Feedback: [Framework (e.g., LangGraph)] - [Maturity Level]`
*   **Details**: 
    *   What did we miss? (Indicators/Indicators)
    *   Where were we too loud? (False positives)
    *   How was the "Persona" advice?

---
*Help us build the Cockpit Standard for AI Operations. 🚀🛡️✨*
