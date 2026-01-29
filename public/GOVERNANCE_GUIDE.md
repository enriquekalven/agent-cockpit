# 🛡️ Governance: Privacy & Trust

For enterprise AI, "Black Box" reasoning is not acceptable. The AgentOps Cockpit implements industry-standard governance to protect data, ensure transparency, and maintain human control.

## 🔒 PII Scrubber (Privacy Pillar)
The `PIIScrubber` is an automated middleware that sits between the user and the LLM, acting as a **PII Guardrail** (a core OpenAI/Anthropic standard).
- **Auto-Detection**: Scans for Emails, Credit Cards, SSNs, and Phone Numbers.
- **Masking**: Replaces sensitive info with labels like `[[MASKED_EMAIL]]` before it leaves your VPC.
- **Compliance**: Ensures your training logs and fine-tuning datasets remain PII-free by default.

## ⚖️ Human-in-the-Loop (Governance Node)
Following OpenAI and Anthropic safety guidelines, the Cockpit enforces **HITL** for high-stakes actions.
- **Approval Nodes**: Critical tools (e.g., `execute_payment`, `delete_resource`) trigger a UI pause in the **Face (A2UI)**.
- **Manual Intervention**: Agents cannot proceed until a human operator clicks "Approve" or "Reject".
- **Safety Gate**: This prevents autonomous "drift" and ensures accountability for financial or system changes.

## 🧪 Evidence Packing (Source Attribution)
OpenAI recommends "showing sources" for all grounded generations. The Cockpit's **Evidence Packet** system automates this:
- **The Packet**: A structured JSON object containing:
    - **Reasoning Path**: The thought chain the agent followed.
    - **Sources**: Direct links/snippets to the RAG documents used.
    - **Tool Evidence**: The raw output of function calls.
- **The Benefit**: Users can click "Show Sources" in the **Face (A2UI)** to see exactly why the agent gave a specific answer, reducing the risk of "hallucinations".

## 🔐 Secret Governance (The Vault)
To maintain the highest level of trust, the Cockpit enforces a **Zero-Secret Policy** in source code.
- **Automated Scanning**: The `make scan-secrets` command uses specialized regex to detect Google Cloud, AWS, and OpenAI keys before they are committed.
- **Abstraction**: We mandate the use of **Google Cloud Secret Manager** to abstract credentials from the runtime environment.
- **Audit Failure**: The deployment pipeline is hard-coded to fail if any unencrypted keys are detected.

## 🎭 Face Architecture Review (UI/UX Trust)
Governance extends to the **Face** (UI/UX) through the automated `ui-auditor`.
- **A2UI Protocol**: Ensures all streaming surfaces provide unique `surfaceId`s for downstream auditability.
- **Accessibility (a11y)**: Mandates `aria-labels` on all agentic interactive triggers to ensure the interface is inclusive.
- **Performance**: High-fidelity agents require low-latency UIs. We audit for large component trees and non-reactive patterns in **Angular** and **Lit**.

---

## 📑 Audit Trail (The Ledger)
We maintain a tamper-proof audit trail for every agent interaction:
- **Complete Traces**: Log every `input`, `thought`, `tool_call`, and `response`.
- **Identity mapping**: Attach a unique `AgentID` and `UserID` to every log entry.
- **Persistence**: Exports logs to BigQuery for long-term governance and compliance reporting.


```bash
# Run the design review
make arch-review
```
