"""
Pillar: cockpit Security
SME Persona: Distinguished SecOps Fellow
Objective: Reasoning-based security auditing focusing on 'Architectural cockpitty' and 'Risk Blinds'.
"""
import ast
import re
from typing import List

from tenacity import retry, stop_after_attempt, wait_exponential

from .base import AuditFinding, BaseAuditor


class SecurityAuditor(BaseAuditor):
    """
    cockpit Security Auditor: Evaluates the system for architectural security failures.
    Aligned with OWASP Agentic Top 10 (ASI) Taxonomy.
    """
    
    @retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        is_python = file_path.endswith('.py')
        is_ts_js = file_path.endswith(('.ts', '.js', '.tsx', '.jsx'))
        
        if not (is_python or is_ts_js):
            return findings
            
        content_lower = content.lower()

        # --- Tier 1: cockpitty & Control (ASI-02: Broken Tool Auth) ---
        
        # 1. Ungated Production Access (The cockpitty Gap)
        sensitive_ops = ['delete', 'drop', 'execute_payment', 'transfer', 'terminate', 'provision', 'wipe_disk']
        if any(op in content_lower for op in sensitive_ops):
            is_gated = self.semantic_verify(
                content, 
                "Does this code enforce a Human-in-the-Loop (HITL) gate or manual approval for sensitive operations?"
            )
            
            if not is_gated:
                title = "ASI-02: Cockpit Gap (Ungated Tool Access)"
                if not self._is_ignored(0, content, title):
                    findings.append(AuditFinding(
                        category="🛡️ SecOps",
                        title=title,
                        description="""Detected sensitive operations without a functional HITL gate.
[bold red]ASI-02 Risk:[/bold red] Broken Tool Authorization allows agents to execute high-impact actions without oversight.
[bold green]RECOMMENDATION:[/bold green] Implement a **Frontend (GenUI) Approval Modal** (AG UI / CopilotKit) or a restricted tool schema.""",
                        impact="CRITICAL",
                        roi="Prevents multi-agent chain reactions and unauthorized financial/data loss.",
                        file_path=file_path
                    ))

        # 2. Insecure Output Handling (ASI-03: RCE/Trap)
        if 'eval(' in content or 'exec(' in content or 'dangerouslySet' in content:
            title = "ASI-03: Insecure Output Handling"
            if not self._is_ignored(0, content, title):
                findings.append(AuditFinding(
                    category="🛡️ SecOps",
                    title=title,
                    description="""Detected `eval()`, `exec()`, or un-sanitized client-side injection.
[bold red]ASI-03 Risk:[/bold red] Agent-generated content could contain malicious code executed by the host.
[bold green]RECOMMENDATION:[/bold green] Pivot to a **Python Sandbox** or **DOMPurify** for UI rendering.""",
                    impact="CRITICAL",
                    roi="Eliminates Remote Code Execution (RCE) and XSS pathways.",
                    file_path=file_path
                ))

        # --- Tier 2: Information Protection (ASI-05/06) ---

        # 3. PII Osmosis & Data Leakage (ASI-05)
        crm_imports = ['salesforce', 'hubspot', 'crm', 'db_client', 'supabase', 'firebase_admin']
        if any(imp in content_lower for imp in crm_imports) and \
           not any(kw in content_lower for kw in ['scrub', 'mask', 'pii', 'anonymize', 'guard', 'redact']):
             title = "ASI-05: PII Osmosis (Data Leakage)"
             if not self._is_ignored(0, content, title):
                 findings.append(AuditFinding(
                    category="🛡️ SecOps",
                    title=title,
                    description="""CRM/DB interaction detected without PII scrubbing logic.
[bold red]ASI-05 Risk:[/bold red] Unauthorized disclosure of sensitive customer data to LLM providers.
[bold green]RECOMMENDATION:[/bold green] Integrate the **Cockpit PII Scrubber** into the request pipeline.""",
                    impact="HIGH",
                    roi="Closes GDPR/SOC2 compliance gaps.",
                    file_path=file_path
                ))

        # 4. Credential Proximity (Hardcoded Secrets)
        if '.env' in content_lower and ('os.environ' in content or 'os.getenv' in content):
             if 'secret_manager' not in content_lower and 'vault' not in content_lower:
                title = "Credential Risk: Shadow ENV"
                if not self._is_ignored(0, content, title):
                    findings.append(AuditFinding(
                        category="🛡️ SecOps",
                        title=title,
                        description="""Local `.env` usage detected for secrets.
[bold yellow]Strategic Gap:[/bold yellow] Tokens can be leaked into reasoning traces or training datasets.
[bold green]RECOMMENDATION:[/bold green] Migrate to **Managed Secrets** (ASM/GSM).""",
                        impact="MEDIUM",
                        roi="Ensures zero-trust credential isolation.",
                        file_path=file_path
                    ))

        # --- Tier 3: Injection & Integrity (ASI-01/10) ---

        # 5. Indirect Prompt Injection (ASI-01)
        if ('retrieve' in content_lower or 'search' in content_lower or 'read_url' in content_lower or 'fetch' in content_lower) and \
           not any(kw in content_lower for kw in ['sanitize', 'untrust', 'instruction_check', 'jailbreak_check']):
            title = "ASI-01: Untrusted Context (Indirect Injection)"
            if not self._is_ignored(0, content, title):
                findings.append(AuditFinding(
                    category="🛡️ SecOps",
                    title=title,
                    description="""Retrieved 3rd-party data fed directly to LLM without sanitization.
[bold red]ASI-01 Risk:[/bold red] Malicious external content can hijack the agent's core instructions.
[bold green]RECOMMENDATION:[/bold green] Implement **Safety Critic** turns or Delimited XML blocks.""",
                    impact="HIGH",
                    roi="Prevents RAG-based 'Instruction Hijacking'.",
                    file_path=file_path
                ))

        # 6. Tool Over-Privilege (ASI-04: Lateral Movement)
        if ('subprocess' in content or 'shutil' in content or 'os.system' in content or 'mcp' in content_lower) and \
           'restricted' not in content_lower and 'sandbox' not in content_lower:
            title = "ASI-04: Tool Over-Privilege"
            if not self._is_ignored(0, content, title):
                findings.append(AuditFinding(
                    category="🛡️ SecOps",
                    title=title,
                    description="""Detected system-level shell execution or MCP access without isolation.
[bold red]ASI-04 Risk:[/bold red] Compromised agents can move laterally across the host network/filesystem.
[bold green]RECOMMENDATION:[/bold green] Use **GVisor** or **Docker Sandboxes** for tool execution.""",
                    impact="CRITICAL",
                    roi="Isolates the blast radius of any individual agent compromise.",
                    file_path=file_path
                ))

        # 7. Knowledge Base Poisoning (ASI-10)
        if ('upsert' in content_lower or 'index.add' in content_lower or 'vector_store' in content_lower) and \
           'verify' not in content_lower and 'admin' not in content_lower:
             title = "ASI-10: Integrity Poisoning (Ungated RAG)"
             if not self._is_ignored(0, content, title):
                 findings.append(AuditFinding(
                    category="🛡️ Integrity",
                    title=title,
                    description="""Ungated data ingestion into knowledge base detected.
[bold yellow]ASI-10 Risk:[/bold yellow] Insecure retrieval-augmented generation (RAG) through poisoned data.
[bold green]RECOMMENDATION:[/bold green] Implement a **Vector Guardian** to validate document fidelity.""",
                    impact="MEDIUM",
                    roi="Maintains the 'cockpit Truth' of the agent's knowledge.",
                    file_path=file_path
                ))

        # --- Tier 4: Polyglot Taint Analysis (SME Deep Scan) ---
        if is_python:
            taint_findings = self._run_python_taint_scan(tree, content, file_path)
            findings.extend(taint_findings)
        
        # Hardcoded Secrets Pattern Match (Polyglot)
        if re.search(r'(key|token|secret|password|auth|api_key)\s*=\s*["\'][A-Za-z0-9+/=_%.-]{16,}["\']', content, re.I):
             title = "Hardcoded Secret (Entropy Check)"
             if not self._is_ignored(0, content, title):
                 findings.append(AuditFinding(
                    category="🛡️ SecOps",
                    title=title,
                    description="Detected high-entropy hardcoded string assigned to a credential variable.",
                    impact="CRITICAL",
                    roi="Prevents repository-based credential leakage.",
                    file_path=file_path
                ))

        return findings

    def _run_python_taint_scan(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        """
        Deep Taint Tracking: Identifies data flows from source (input) to sink (sensitive call).
        Adopts logic from 'agent-audit' for intra-procedural tracing.
        """
        findings = []
        user_input_vars = set()
        
        # 1. Source Identification: Track variables derived from user-controlled inputs
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for arg in node.args.args:
                    if any(x in arg.arg.lower() for x in ['query', 'input', 'prompt', 'task', 'payload', 'body']):
                        user_input_vars.add(arg.arg)
            
            if isinstance(node, ast.Assign):
                # Trace: x = input() or x = request.get_json()
                try:
                    call_str = ast.unparse(node.value).lower() if hasattr(ast, 'unparse') else ""
                    if any(s in call_str for s in ['input(', 'get_json', 'params.get', 'read()']):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                user_input_vars.add(target.id)
                except Exception:
                    pass

        # 2. Sink Detection: Monitor sensitive calls consuming 'user_input_vars'
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                call_name = ""
                if isinstance(node.func, ast.Name):
                    call_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    call_name = node.func.attr
                
                # Sinks: Shell execution, DB queries, MCP tool invocation
                sinks = ['execute', 'run', 'shell', 'subprocess', 'eval', 'exec', 'mcp', 'sql', 'query']
                if any(x in call_name.lower() for x in sinks):
                    for arg in node.args:
                        names = [n.id for n in ast.walk(arg) if isinstance(n, ast.Name)]
                        for name in names:
                            if name in user_input_vars:
                                # Check for sanitization in preceding code
                                context_start = max(0, node.lineno - 10)
                                recent_lines = content.splitlines()[context_start:node.lineno]
                                if not any('sanitize' in line.lower() or 'validate' in line.lower() for line in recent_lines):
                                    title = "cockpit Taint Flow: Unsanitized Data to Sink"
                                    if not self._is_ignored(node.lineno, content, title):
                                        findings.append(AuditFinding(
                                            category="🛡️ SecOps",
                                            title=title,
                                            description=f"Direct flow from `{name}` (source) to `{call_name}` (sink) without sanitization.\\n[bold red]Attack Vector:[/bold red] Prompt Injection or RCE via Tool manipulation.",
                                            impact="CRITICAL",
                                            roi="Eliminates the most common ASI injection vectors.",
                                            line_number=node.lineno,
                                            file_path=file_path
                                        ))
                                        break
                                        break
        return findings
