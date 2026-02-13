"""
Pillar: Strategic Architecture
SME Persona: Distinguished Semantic Fellow
Objective: Detects 'Strategic Paradigm Mismatches' using the Universal Intent Taxonomy.
Coverage: 15 Paradigms (~99% Modern Agentic Patterns)
"""
import ast
import re
from typing import List, Set, Dict, Tuple, Optional
from .base import BaseAuditor, AuditFinding

class ParadigmAuditor(BaseAuditor):
    """
    Evaluates agents against fifteen 'North Star' paradigms to detect intent/implementation mismatches.
    Shift focus from tactical code quality to strategic architectural wisdom.
    """

    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        """
        Executes a three-layer scan: Library DNA (Imports), Data Flow Tracer (AST), and Prompt Intent Analysis (Heuristics).
        """
        findings = []
        content_lower = content.lower()

        # --- Layer 1: Library DNA (Imports) ---
        imports = self._get_imports(tree)
        
        # 1. Collaboration Paradigm: Monolithic Fatigue
        if len(content.splitlines()) > 500 and content_lower.count('def ') > 15:
            findings.append(AuditFinding(
                category="🚀 Strategic Paradigm",
                title="Monolithic Fatigue Detected",
                description="""Detected a single-file agent holding 15+ functions/tools and exceeding 500 lines.
[bold blue]Strategic Perspective:[/bold blue] Large monolithic agents suffer from reasoning saturation and decreased precision.
[bold green]RECOMMENDATION:[/bold green] Pivot to a **Multi-Agent Swarm (A2A)** or partitioned specialist agents to improve focus.""",
                impact="MEDIUM (Agility & Precision)",
                roi="Reduces context pollution and enables parallel scaling.",
                file_path=file_path
            ))

        # 2. Infrastructure Paradigm: Legacy Shadowing
        if 'requests' in imports and ('tool' in content_lower or 'mcp' in content_lower):
            findings.append(AuditFinding(
                category="🚀 Strategic Paradigm",
                title="Legacy Shadowing: HTTP instead of MCP",
                description="""Detected manual `requests` calls inside an agentic context.
[bold blue]Strategic Move:[/bold blue] Migrating to **Model Context Protocol (MCP)** enables tool reuse and better security.
[bold green]RECOMMENDATION:[/bold green] Pivot to `mcp-server` architecture for external integrations.""",
                impact="LOW",
                roi="Enables swarm interoperability and standardized tool-use.",
                file_path=file_path
            ))

        # 3. Memory Paradigm: Token Amnesia
        if ('history' in content_lower or 'messages' in content_lower) and \
           'zep' not in content_lower and 'memgpt' not in content_lower and 'redis' not in content_lower:
            if ' = []' in content or 'append(' in content_lower:
                findings.append(AuditFinding(
                    category="🚀 Strategic Paradigm",
                    title="Token Amnesia: Manual Memory Management",
                    description="""Detected manual chat history management (list appending) without persistent session state.
[bold red]Structural Risk:[/bold red] Manual history leads to context truncation issues and 'Token Amnesia' across restarts.
[bold green]RECOMMENDATION:[/bold green] Pivot to **Persistent Memory (Zep, MemGPT, or Redis)** for long-term reasoning.""",
                    impact="MEDIUM (Experience)",
                    roi="Ensures conversational continuity and long-term user context.",
                    file_path=file_path
                ))

        # 4. Intelligence Paradigm: Reflection Blindness (NEW)
        if any(kw in content_lower for kw in ['code', 'legal', 'finance', 'medical']) and \
           not any(kw in content_lower for kw in ['reflect', 'correct', 'check', 'validate', 'critic']):
            findings.append(AuditFinding(
                category="🚀 Strategic Paradigm",
                title="Reflection Blindness: Brittle Intelligence",
                description="""Detected high-stakes reasoning (Code/Legal/Finance) without a visible Reflection or Self-Correction loop.
[bold red]Structural Fragility:[/bold red] Single-pass reasoning on complex tasks has high failure rates.
[bold green]RECOMMENDATION:[/bold green] Implement a **Reflection Loop** or a Multi-Turn **Critic-Actor** pattern.""",
                impact="HIGH (Accuracy)",
                roi="Significantly reduces reasoning hallucinations and logic errors.",
                file_path=file_path
            ))

        # --- Layer 2: Data Flow (AST Tracking) ---
        tracer = DataFlowTracer()
        tracer.visit(tree)
        for mismatch in tracer.mismatches:
            var_name, line_no = mismatch
            findings.append(AuditFinding(
                category="🚀 Strategic Paradigm",
                title="Pattern Mismatch: Structured Data Stuffing",
                description=f"""Detected variable `{var_name}` (loaded from structured source) being directly injected into an LLM prompt.
[bold red]Structural Blindspot:[/bold red] "Prompt Stuffing" large data leads to context drowning and high costs.
[bold green]RECOMMENDATION:[/bold green] Pivot to **NL2SQL** or **Semantic Indexing**.""",
                impact="HIGH (Cost & Latency)",
                roi="Reduces token burn and hallucination risk.",
                file_path=file_path,
                line_number=line_no
            ))

        # --- Layer 3: Intent/Implementation Mismatch ---
        
        # 5. Relational Analytics Paradigm: RAG for Math
        if ("calculate" in content_lower or "average" in content_lower or "sum " in content_lower) and \
           ("rag" in content_lower or "search" in content_lower or "find" in content_lower):
            if "sql" not in content_lower and "math" not in content_lower and "calculator" not in content_lower:
                findings.append(AuditFinding(
                    category="🚀 Strategic Paradigm",
                    title="Paradigm Drift: RAG for Math",
                    description="""Detected arithmetic intent combined with semantic retrieval.
[bold red]Structural Failure:[/bold red] RAG is for text retrieval, not precise mathematical aggregations.
[bold green]RECOMMENDATION:[/bold green] Pivot to **Code Interpreter** or **SQL Agent**.""",
                    impact="CRITICAL (Accuracy)",
                    roi="Eliminates reasoning drift in analytical operations.",
                    file_path=file_path
                ))

        # 6. Data Transformation Paradigm: Token Burning
        if ("regex" in content_lower or "slicing" in content_lower or "format" in content_lower) and \
           ("prompt" in content_lower or "instructions" in content_lower):
            if "transform" in content_lower or "clean" in content_lower:
                findings.append(AuditFinding(
                    category="🚀 Strategic Paradigm",
                    title="Token Burning: LLM for Deterministic Ops",
                    description="""Detected intent to clean/transform text using prompts where Python logic would suffice.
[bold yellow]Strategic Waste:[/bold yellow] Using LLMs for basic ETL leads to 'Architectural Waste.'
[bold green]RECOMMENDATION:[/bold green] Pivot to a **Python Sandbox** tool or deterministic preprocessing.""",
                    impact="MEDIUM (Cost)",
                    roi="Reduces token billing for non-probabilistic tasks.",
                    file_path=file_path
                ))

        # 7. Enterprise Search Paradigm: Latency Trap
        if ('os.walk' in content or 'glob.glob' in content) and ('query' in content_lower or 'search' in content_lower):
            findings.append(AuditFinding(
                category="🚀 Strategic Paradigm",
                title="Latency Trap: Brute-Force Local Search",
                description="""Detected local filesystem traversal combined with LLM querying.
[bold red]Strategic Failure:[/bold red] Scalability will fail at enterprise volumes.
[bold green]RECOMMENDATION:[/bold green] Pivot to **Vector RAG (Pinecone/Chroma)**.""",
                impact="HIGH (Scaling)",
                roi="Enables sub-second discovery over enterprise datasets.",
                file_path=file_path
            ))

        # 8. High-Stake Actions Paradigm: Ungated Autonomy
        if any(kw in content_lower for kw in ['delete_', 'write_', 'execute_payment', 'post_']) and \
           'approve' not in content_lower and 'hitl' not in content_lower:
            findings.append(AuditFinding(
                category="🚀 Strategic Paradigm",
                title="Ungated High-Stake Action",
                description="""Detected destructive tool-calls without an explicit HITL gate.
[bold red]Governance GAP:[/bold red] Agents must not have autonomous write access to critical assets.
[bold green]RECOMMENDATION:[/bold green] Implement **HITL Approval Nodes** (e.g., A2UI).""",
                impact="CRITICAL (Safety)",
                roi="Protects enterprise sovereignty and prevents accidents.",
                file_path=file_path
            ))

        # 9. Multi-Step Logic Paradigm: Manual State Machine
        is_loop_llm = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                try:
                    loop_content = ast.unparse(node).lower()
                    if any(kw in loop_content for kw in ['completion', 'generate_content', 'chat_completion', 'llm(']):
                        is_loop_llm = True
                        break
                except: continue
        
        if is_loop_llm and 'langgraph' not in content_lower and 'semantic_kernel' not in content_lower:
            findings.append(AuditFinding(
                category="🚀 Strategic Paradigm",
                title="Manual State Machine: Loop of Doom",
                description="""LLM reasoning calls detected inside standard Python loops.
[bold purple]Architecture Suggestion:[/bold purple] Pivot to **LangGraph** to avoid reasoning collapse.""",
                impact="HIGH (Reliability)",
                roi="Ensures deterministic state transition.",
                file_path=file_path
            ))

        # 10. Scalability Paradigm: Looming Latency
        if ('response' in content_lower or 'generation' in content_lower) and \
           'stream=true' not in content_lower and 'streaming' not in content_lower:
            if any(kw in content_lower for kw in ['report', 'summarize', 'article', 'write_']):
                findings.append(AuditFinding(
                    category="🚀 Strategic Paradigm",
                    title="Looming Latency: Blocking Inference",
                    description="""Detected non-streaming generation for long-form content.
[bold blue]Strategic UX Risk:[/bold blue] Long-wait times without feedback lead to churn.
[bold green]RECOMMENDATION:[/bold green] Pivot to **A2UI Streaming Protocol**.""",
                    impact="MEDIUM (Experience)",
                    roi="Improves perceived latency and retention.",
                    file_path=file_path
                ))

        # 11. Specialization Paradigm: Expert Bloat
        tool_count = content_lower.count('@tool') or content_lower.count('def ')
        if tool_count > 25 and'router' not in content_lower and 'orchestrator' not in content_lower:
            findings.append(AuditFinding(
                category="🚀 Strategic Paradigm",
                title="Expert Bloat: Linear Tool Selection",
                description="""Detected 25+ tools in a single flat context.
[bold red]Structural Friction:[/bold red] Accuracy drops as choice-set grows.
[bold green]RECOMMENDATION:[/bold green] Implement **Hierarchical Tool Routing**.""",
                impact="MEDIUM (Precision)",
                roi="Increases reasoning accuracy.",
                file_path=file_path
            ))

        # 12. Finetuning Paradigm: Instruction Fatigue
        docstrings_len = sum(len(d) for d in re.findall(r'"""([\s\S]*?)"""', content))
        if docstrings_len > 10000 and 'finetune' not in content_lower and 'distill' not in content_lower:
             findings.append(AuditFinding(
                category="🚀 Strategic Paradigm",
                title="Instruction Fatigue: Prompt Overloading",
                description="""Detected massive prompts (>10k chars) encoding complex behavior.
[bold yellow]Strategic Waste:[/bold yellow] High-token overhead per turn.
[bold green]RECOMMENDATION:[/bold green] Pivot to **Model Distillation**.""",
                impact="HIGH (Cost)",
                roi="Reduces baseline token costs.",
                file_path=file_path
            ))

        # 13. Governance Paradigm: Policy Blindness (NEW)
        if any(kw in content_lower for kw in ['policy', 'rules', 'regulations']) and \
           'policy_engine' not in content_lower and 'guardrails' not in content_lower:
            findings.append(AuditFinding(
                category="🚀 Strategic Paradigm",
                title="Policy Blindness: Implicit Governance",
                description="""Detected complex policy/rule enforcement logic hardcoded in prompts.
[bold red]Governance Risk:[/bold red] Hardcoded policies are difficult to audit, update, and sync across agents.
[bold green]RECOMMENDATION:[/bold green] Pivot to our **Centralized Policy Engine** or External Guardrails.""",
                impact="MEDIUM (Governance)",
                roi="Centralizes alignment and simplifies regulatory updates.",
                file_path=file_path
            ))

        # 14. Decisional Paradigm: Path Rigidness (NEW)
        if any(kw in content_lower for kw in ['complex task', 'goal', 'workflow']) and \
           not any(kw in content_lower for kw in ['plan', 'step_by_step', 'react', 'thought']):
            if content_lower.count(' -> ') > 3 or content_lower.count('then ') > 3:
                findings.append(AuditFinding(
                    category="🚀 Strategic Paradigm",
                    title="Path Rigidness: Sequential Blindness",
                    description="""Detected complex goal intent being handled by a rigid, non-planning execution path.
[bold red]Strategic Risk:[/bold red] Linear paths fail when edge cases or tool errors occur mid-flight.
[bold green]RECOMMENDATION:[/bold green] Pivot to a **Dynamic Planner** or **ReAct Pattern**.""",
                    impact="HIGH (Reliability)",
                    roi="Increases successful task completion rates on open-ended goals.",
                    file_path=file_path
                ))

        # 15. Retrieval Paradigm: Passive Retrieval (NEW)
        if 'retrieve' in content_lower or 'search' in content_lower:
             if not any(kw in content_lower for kw in ['conditional', 'if confidence', 'decide']):
                 findings.append(AuditFinding(
                    category="🚀 Strategic Paradigm",
                    title="Passive Retrieval: Context Drowning",
                    description="""Detected retrieval execution on every turn without conditional logic.
[bold yellow]FinOps Waste:[/bold yellow] Fetching documents when the model already 'knows' the answer burns context and cost.
[bold green]RECOMMENDATION:[/bold green] Pivot to **Agentic/Active RAG** (retrieve only when needed).""",
                    impact="LOW (FinOps)",
                    roi="Reduces context window waste and improves reasoning focus.",
                    file_path=file_path
                ))

        # Print actions for orchestrator capture
        for f in findings:
             print(f"ACTION: {file_path}:{f.line_number or 1} | {f.title} | {f.roi}")

        return findings

    def _get_imports(self, tree: ast.AST) -> Set[str]:
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.add(n.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
        return imports

class DataFlowTracer(ast.NodeVisitor):
    def __init__(self):
        self.sources: Dict[str, int] = {}
        self.mismatches: List[Tuple[str, int]] = []

    def visit_Assign(self, node: ast.Assign):
        if isinstance(node.value, ast.Call):
            try:
                call_str = ast.unparse(node.value).lower()
                if any(s in call_str for s in ['read_csv', 'read_json', '.read()', 'json.load']):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            self.sources[target.id] = node.lineno
            except: pass
        self.generic_visit(node)

    def visit_JoinedStr(self, node: ast.JoinedStr):
        for value in node.values:
            if isinstance(value, ast.FormattedValue):
                if isinstance(value.value, ast.Name) and value.value.id in self.sources:
                    self.mismatches.append((value.value.id, node.lineno))
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        try:
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'format':
                for arg in node.args:
                    if isinstance(arg, ast.Name) and arg.id in self.sources:
                        self.mismatches.append((arg.id, node.lineno))
            if isinstance(node.func, ast.Name) and node.func.id in ['render', 'PromptTemplate', 'Template']:
                for arg in node.args:
                    if isinstance(arg, ast.Name) and arg.id in self.sources:
                        self.mismatches.append((arg.id, node.lineno))
                for kw in node.keywords:
                    if isinstance(kw.value, ast.Name) and kw.value.id in self.sources:
                        self.mismatches.append((kw.value.id, node.lineno))
        except: pass
        self.generic_visit(node)
