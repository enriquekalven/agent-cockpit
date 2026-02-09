# 🦴 Eat Your Own Dogfood: The AgentOps Cockpit Roast & Hardening Challenge (v1.4.1) 🚀

Stop shipping "vibes-based" agents. It's time to subject your AI swarms to **Production-Grade Paranoia**. We're recruiting elite agent developers to stress-test the **Master Audit Suite** against real-world chaos. 

Do you have the "Category Killer" grade, or is your agent just a script with a fancy prompt? Let's find out.

---

### **🎯 The Mission: Roast Your Agent**
Unleash the full SME council on your most complex repository. We’re hunting for:
1.  **SME Roasts**: Did our digital principals (SecOps, FinOps, Architect) find the skeletons in your `src/`?
2.  **The Auto-Heal Flex**: Did `make apply-fixes` actually land a PR-worthy patch, or did it hallucinate a new library?
3.  **Persona Vibes**: Does the **Red Team** sound like a hacker, or your high school principal?

---

### **🎮 Choose Your Difficulty**

#### **Level 1: The Drive-By Audit (Zero Install)**
The fastest way to see if your agent is actually production-ready. 
```bash
# ⚡ Quick Roast: See the red flags in seconds
uvx agentops-cockpit report --mode quick

# 🧠 Deep Intelligence: Full benchmarks & stress-testing
uvx agentops-cockpit report --mode deep
```

#### **Level 2: The Full Orchestrator (Hardened Mode)**
For the developers who want to apply auto-remediation patches and hit that 100/100 score.
```bash
pip install agentops-cockpit
agent-ops report --workspace --heal --sim
```

---

### **� The CI/CD Pipeline Integration**
Don't let manual errors drift into production. Integrate the Cockpit as a **blocking gate** in your GitHub Actions. If your score drops below your threshold, the build fails.

**Sample `.github/workflows/agent-governance.yml`:**
```yaml
name: AgentOps Governance Gate
on: [pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Master Audit
        run: |
          # Use uvx for zero-config execution in CI
          npx uvx agentops-cockpit report --mode quick --plain
```
*Note: The Cockpit returns Exit Code 3 if SME gates are rejected, blocking the PR until fixes are applied.*

---

### **🔌 The MCP Connectivity Hub**
The Cockpit isn't just a scanner; it's a **Model Context Protocol (MCP)** server. This allows other agents (like Antigravity or Claude Code) to natively call Cockpit tools to audit *themselves* or other codebases.

**How to start the server:**
```bash
# Start the stdio-based MCP server
agent-ops mcp-server
```

**Exposed Tools:**
- `optimize_code`: Audit for FinOps & Performance.
- `policy_audit`: Real-time guardrail validation.
- `architecture_review`: Google Well-Architected design review.
- `red_team_attack`: Launch an adversarial security scan.

---

### **�🕵️ The SME Persona Gauntlet**

Pick your lane and see if you can survive the audit:

#### **🔐 The Shadow Guardian (Red Team)**
*   **Mission**: Try to jailbreak your own agent using the Cockpit.
*   **Command**: `uvx agentops-cockpit report --only security`
*   **Viral Moment**: Catching a **PII Leak** before the lawyers do. 🛡️

#### **💰 The Token Reaper (FinOps)**
*   **Mission**: Find the "Loop of Death" burning your cloud credits.
*   **Command**: `uvx agentops-cockpit report --only finops`
*   **Viral Moment**: Reducing inference TCO by 90% with one caching config. 💸

#### **🧗 The Truth-Sayer (RAG & Quality)**
*   **Mission**: Kill the hallucinations.
*   **Command**: `uvx agentops-cockpit report --only quality`
*   **Viral Moment**: Achieving **Zero-Shot Grounding** perfection. ✨

#### **🏛️ The Sovereign Architect (SRE & Infra)**
*   **Mission**: Modernize your stack from REST to MCP.
*   **Command**: `uvx agentops-cockpit report --only reliability`
*   **Viral Moment**: Pivoting to gRPC and watching your tail latency flatline. 🚀

---

### **💬 The Feedback Loop (Wall of Fame/Shame)**
Did we miss a blatant secret? Did our Architect suggest something illegal? Let us know:
*   **Discord/Slack**: [Join the Swarm]
*   **GitHub**: Open an issue titled `[DOGFOOD] My Agent is Roasted: [Framework]`
*   **The Bounty**: Best feedback gets their agent featured in our "Well-Architected" Hall of Fame.

---
*Build for the Sovereign standard. Audit like a Principal. Ship like a God. 🚀🛡️✨*
