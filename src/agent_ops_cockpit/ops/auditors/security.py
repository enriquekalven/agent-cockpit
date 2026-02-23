"""
Pillar: Sovereign Security
SME Persona: Distinguished SecOps Fellow
Objective: Reasoning-based security auditing focusing on 'Architectural Sovereignty' and 'Risk Blinds'.
"""
import ast
import re
from typing import List

from tenacity import retry, stop_after_attempt, wait_exponential

from .base import AuditFinding, BaseAuditor


class SecurityAuditor(BaseAuditor):
    """
    Sovereign Security Auditor: Evaluates the system for architectural security failures.
    Moves beyond signature-based secrets to 'Intent-Implementation' security gaps.
    """
    
    @retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        is_python = file_path.endswith('.py')
        is_ts_js = file_path.endswith(('.ts', '.js', '.tsx', '.jsx'))
        
        if not (is_python or is_ts_js):
            return findings
            
        content_lower = content.lower()

        # --- Tier 1: Sovereignty & Control ---
        
        # 1. Ungated Production Access (The Sovereignty Gap)
        sensitive_ops = ['delete', 'drop', 'execute_payment', 'transfer', 'terminate', 'provision']
        if any(op in content_lower for op in sensitive_ops):
            # v2.0.2 Semantic Pivot: Ask the Policy SME if this is actually gated
            is_gated = self.semantic_verify(
                content, 
                "Does this code enforce a Human-in-the-Loop (HITL) gate or manual approval for sensitive operations like delete, payment, or termination?"
            )
            
            if not is_gated:
                title = "Sovereignty Gap: Ungated Production Access"
                if not self._is_ignored(0, content, title):
                    findings.append(AuditFinding(
                        category="🛡️ Security",
                        title=title,
                        description="""Semantic verify failed: Detected sensitive operations without a functional Human-in-the-Loop (HITL) gate.
[bold red]Structural Risk:[/bold red] Autonomous agents must not have ungated write access to production assets.
[bold green]RECOMMENDATION:[/bold green] Implement a **Governance Gate** or a 2-Factor Approval trigger.""",
                        impact="CRITICAL",
                        roi="Protects enterprise assets from autonomous logic failures.",
                        file_path=file_path
                    ))

        # 2. Insecure Output Handling (The 'eval' Trap)
        if 'eval(' in content or 'exec(' in content:
            title = "Insecure Output Handling: Execution Trap"
            if not self._is_ignored(0, content, title):
                findings.append(AuditFinding(
                    category="🛡️ Security",
                    title=title,
                    description="""Detected `eval()` or `exec()` on strings. 
[bold red]Critical Vulnerability:[/bold red] If an agent generates code that is then executed via `eval`, it creates a RCE path.
[bold green]RECOMMENDATION:[/bold green] Pivot to a **Python Sandbox** or use a typed JSON parser like Pydantic.""",
                    impact="CRITICAL",
                    roi="Eliminates Remote Code Execution (RCE) vectors.",
                    file_path=file_path
                ))

        # --- Tier 2: Information Protection ---

        # 3. PII Osmosis (Implicit Data Leakage)
        crm_imports = ['salesforce', 'hubspot', 'crm', 'db_client']
        if any(imp in content_lower for imp in crm_imports) and \
           not any(kw in content_lower for kw in ['scrub', 'mask', 'pii', 'anonymize', 'guard']):
             title = "PII Osmosis: Implicit Leakage Risk"
             if not self._is_ignored(0, content, title):
                 findings.append(AuditFinding(
                    category="🛡️ Security",
                    title=title,
                    description="""Detected CRM or customer data interaction without visible PII scrubbing or masking logic.
[bold yellow]Compliance Risk:[/bold yellow] Sending raw customer data to shared LLM endpoints creates GDPR/SOC2 liability.
[bold green]RECOMMENDATION:[/bold green] Implement a **Pre-Inference Scrubber** to mask sensitive identifiers.""",
                    impact="HIGH",
                    roi="Closes the compliance gap for data privacy regulations.",
                    file_path=file_path
                ))

        # 4. Credential Proximity (Shadow ENV)
        if '.env' in content_lower and ('os.environ' in content or 'os.getenv' in content):
             if 'secret_manager' not in content_lower and 'vault' not in content_lower:
                title = "Credential Proximity: Shadow ENV Usage"
                if not self._is_ignored(0, content, title):
                    findings.append(AuditFinding(
                        category="🛡️ Security",
                        title=title,
                        description="""Detected use of local `.env` files for secrets in an agentic environment.
[bold purple]Security Gap:[/bold purple] Local ENVs can be leaked into the agent's context if it gains file-read or environment access.
[bold green]RECOMMENDATION:[/bold green] Pivot to **Google Secret Manager (GCP)** or **AWS Secrets Manager**.""",
                        impact="MEDIUM",
                        roi="Prevents cross-contamination of secrets into training/logging channels.",
                        file_path=file_path
                    ))

        # --- Tier 3: Injection & Integrity ---

        # 5. Indirect Prompt Injection (Trusted Context Trap)
        if ('retrieve' in content_lower or 'search' in content_lower or 'read_url' in content_lower) and \
           not any(kw in content_lower for kw in ['sanitize', 'untrust', 'instruction_check']):
            title = "Untrusted Context Trap: Indirect Injection"
            if not self._is_ignored(0, content, title):
                findings.append(AuditFinding(
                    category="🛡️ Sovereign Security",
                    title=title,
                    description="""retrieved data from external sources (RAG/Web) is being fed to the LLM without sanitization.
[bold red]Vulnerability:[/bold red] Indirect Prompt Injection occurs when a malicious website or document 'hijacks' the agent via retrieval.
[bold green]RECOMMENDATION:[/bold green] Implement **Delimited Context** or a 'Safety Critic' turn to verify the retrieval payload.""",
                    impact="HIGH",
                    roi="Prevents 3rd-party data from overtaking the agent's system instructions.",
                    file_path=file_path
                ))

        # 6. Lateral Movement (Tool Over-Privilege)
        if ('subprocess' in content or 'shutil' in content or 'os.system' in content) and \
           'restricted' not in content_lower and 'sandbox' not in content_lower:
            title = "Lateral Movement: Tool Over-Privilege"
            if not self._is_ignored(0, content, title):
                findings.append(AuditFinding(
                    category="🛡️ Sovereign Security",
                    title=title,
                    description="""Detected system-level execution capabilities without a restricted sandbox.
[bold red]Exploitation Risk:[/bold red] A compromised agent could move laterally within the host system.
[bold green]RECOMMENDATION:[/bold green] Run agent tasks in a **Docker Sandbox** or apply the **Autonomous Fix** (tool_privilege_check decorator).""",
                    impact="CRITICAL",
                    roi="Isolates the agent's blast radius to its immediate task shell.",
                    file_path=file_path
                ))

        # 7. Knowledge Base Poisoning
        if ('upsert' in content_lower or 'index.add' in content_lower) and \
           'verify' not in content_lower and 'admin' not in content_lower:
             title = "Knowledge Base Poisoning: Ungated Ingestion"
             if not self._is_ignored(0, content, title):
                 findings.append(AuditFinding(
                    category="🛡️ Sovereign Security",
                    title=title,
                    description="""Detected high-volume data ingestion into the Vector Store without a verification gate.
[bold blue]Integrity Risk:[/bold blue] Users could poison the agent's 'truth' by feeding it malicious data for RAG.
[bold green]RECOMMENDATION:[/bold green] Implement an **Ingestion Guardrail** to audit data before it hits the production index.""",
                    impact="MEDIUM",
                    roi="Maintains the 'Truth Integrity' of the RAG Knowledge Base.",
                    file_path=file_path
                ))

        # --- Tier 4: Cross-Cloud Governance (AWS/Azure) ---
        
        # 8. AWS Bedrock: Missing Guardrails Configuration (Sovereign Parity)
        if 'boto3' in content_lower and 'invoke_model' in content_lower:
            if 'guardrailIdentifier' not in content:
                title = "AWS Bedrock: Missing Guardrail ID"
                if not self._is_ignored(0, content, title):
                    findings.append(AuditFinding(
                        category="🛡️ Sovereign Security",
                        title=title,
                        description="""Detected AWS Bedrock `invoke_model` call without an explicit Guardrail Identifier.
[bold orange]Governance Gap:[/bold orange] Unlike Vertex AI, Bedrock requires explicit Guardrail binding for PII/Safety enforcement in the API call.
[bold green]RECOMMENDATION:[/bold green] Provision a **Bedrock Guardrail** and bind it to the request payload via `guardrailIdentifier`.""",
                        impact="HIGH",
                        roi="Enforces centralized safety policies on AWS infrastructure.",
                        file_path=file_path
                    ))

        # 9. Azure OpenAI: Ungated API Endpoint
        if 'openai.azure.com' in content:
            if 'api-key' in content_lower and '.dotenv' not in content_lower and 'secret_manager' not in content_lower:
                title = "Azure OpenAI: Exposed Endpoint Logic"
                if not self._is_ignored(0, content, title):
                    findings.append(AuditFinding(
                        category="🛡️ Sovereign Security",
                        title=title,
                        description="""Detected Azure OpenAI service endpoint hardcoded with potentially weak credential management.
[bold red]Structural Risk:[/bold red] Azure OpenAI endpoints are often targets for lateral movement if the API key is compromised.
[bold green]RECOMMENDATION:[/bold green] Pivot to **Microsoft Entra ID (Managed Identity)** for authentication instead of API keys.""",
                        impact="CRITICAL",
                        roi="Eliminates the risk of leaked Azure API keys.",
                        file_path=file_path
                    ))

        # --- Tier 4: Polyglot Security (TS/Node) ---
        if is_ts_js:
            # 8. Ungated Agentic Routes (The 'route.ts' Gap)
            if 'route.ts' in file_path and ('post' in content_lower or 'get' in content_lower):
                if '@openai/agents' in content or 'agent' in content_lower:
                    if not any(kw in content_lower for kw in ['auth', 'middleware', 'protect', 'clerk', 'next-auth']):
                        title = "Ungated Agentic Route (TypeScript)"
                        if not self._is_ignored(0, content, title):
                            findings.append(AuditFinding(
                                category="🛡️ Sovereign Security",
                                title=title,
                                description="""Detected a potential Next.js/Node.js agentic route without visible authentication or protecting middleware.
[bold red]Vulnerability:[/bold red] Exposed agent endpoints can be abused for unauthorized LLM consumption or prompt injection.
[bold green]RECOMMENDATION:[/bold green] Wrap route handlers in an **Auth Middleware** (e.g., Clerk, NextAuth).""",
                                impact="CRITICAL",
                                roi="Prevents unauthorized API abuse and cost-spikes.",
                                file_path=file_path
                            ))

            # 9. Insecure Context Injection (TS RAG)
            if 'dangerouslySetInnerHTML' in content or 'eval(' in content:
                title = "Insecure Client-Side Injection"
                if not self._is_ignored(0, content, title):
                    findings.append(AuditFinding(
                        category="🛡️ Sovereign Security",
                        title=title,
                        description="""Detected `dangerouslySetInnerHTML` or `eval` in a TS/JS agent frontend.
[bold red]Risk:[/bold red] Agent-generated markdown/HTML could contain XSS payloads if rendered without sanitization.
[bold green]RECOMMENDATION:[/bold green] Use a **Sanitization Library** (e.g., DOMPurify) before rendering agent outputs.""",
                        impact="HIGH",
                        roi="Eliminates Client-Side Prompt Injection and XSS vectors.",
                        file_path=file_path
                    ))
        
        # 10. Semantic Taint Tracking (AST-Aware)
        # Tracks variable names like 'query', 'input', 'prompt' from entry points to dangerous calls
        user_input_vars = set()
        for node in ast.walk(tree):
            # Find assignments from common input sources (e.g., function args, input())
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for arg in node.args.args:
                    if any(x in arg.arg.lower() for x in ['query', 'input', 'prompt', 'task']):
                        user_input_vars.add(arg.arg)
            
            # Find sensitive calls using these variables
            if isinstance(node, ast.Call):
                call_name = ""
                if isinstance(node.func, ast.Name):
                    call_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    call_name = node.func.attr
                
                if any(x in call_name.lower() for x in ['execute', 'run', 'shell', 'subprocess', 'eval', 'exec', 'mcp']):
                    # Check if any argument contains a tainted variable
                    for arg in node.args:
                        names = [n.id for n in ast.walk(arg) if isinstance(n, ast.Name)]
                        for name in names:
                            if name in user_input_vars:
                                # Simple heuristic: Check for 'sanitize' in the preceding lines
                                context_start = max(0, node.lineno - 5)
                                if 'sanitize' not in content.splitlines()[context_start:node.lineno].__str__().lower():
                                    title = "Sovereign Taint Detected: Unsanitized Input Flow"
                                    if not self._is_ignored(node.lineno, content, title):
                                        findings.append(AuditFinding(
                                            category="🛡️ Sovereign Security",
                                            title=title,
                                            description=f"Detected tainted variable `{name}` flowing into sensitive call `{call_name}` without visible sanitization.\n[bold red]Injection Risk:[/bold red] Direct flow from user input to tool execution is a primary attack vector for Prompt Injection.",
                                            impact="CRITICAL",
                                            roi="Blocks direct remote manipulation of the agent's tools.",
                                            line_number=node.lineno,
                                            file_path=file_path
                                        ))
                                        break

        # Secrets Scanner (Hardcoded)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if any(x in target.id.lower() for x in ["key", "token", "secret", "password", "auth"]):
                            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                                val = node.value.value
                                if len(val) > 16 and re.search(r"\d", val) and re.search(r"[a-zA-Z]", val):
                                    title = "Hardcoded Secret Detected"
                                    if not self._is_ignored(node.lineno, content, title):
                                        findings.append(AuditFinding(
                                            category="🛡️ Sovereign Security",
                                            title=title,
                                            description="Detected a potential high-entropy credential hardcoded in source.",
                                            impact="CRITICAL",
                                            roi="Prevent total system compromise via leaked credentials.",
                                            line_number=node.lineno,
                                            file_path=file_path
                                        ))

        return findings
