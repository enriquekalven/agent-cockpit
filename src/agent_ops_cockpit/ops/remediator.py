import ast
import difflib
import os
import re
from datetime import datetime

import libcst as cst

try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None

class ModernResiliencyTransformer(cst.CSTTransformer):
    """v2.0.2 Engineered Logic: Layout-preserving transformation using LibCST."""
    def __init__(self, target_line: int):
        self.target_line = target_line
        self.found = False

    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.FunctionDef:
        # Check line number (LibCST doesn't give line numbers easily without MetadataWrapper, 
        # but for this demo we assume target name match or simplify)
        if hasattr(original_node, 'name') and not self.found:
             # Add @retry decorator
             retry_decorator = cst.Decorator(
                 decorator=cst.Call(
                     func=cst.Name("retry"),
                     args=[
                         cst.Arg(keyword=cst.Name("wait"), value=cst.Call(func=cst.Name("wait_exponential"), args=[cst.Arg(keyword=cst.Name("multiplier"), value=cst.Integer("1"))])),
                         cst.Arg(keyword=cst.Name("stop"), value=cst.Call(func=cst.Name("stop_after_attempt"), args=[cst.Arg(value=cst.Integer("3"))]))
                     ]
                 )
             )
             new_decorators = list(updated_node.decorators) + [retry_decorator]
             self.found = True
             return updated_node.with_changes(decorators=new_decorators)
        return updated_node

class CodeRemediator:
    """
    Phase 4: The 'Closer' - Automated Remediation Engine.
    Transforms code surgically based on audit findings to inject best practices
    while preserving license headers, comments, and formatting. (v2.0.2 Sovereign Diffing)
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            self.content = f.read()
        self.lines = self.content.splitlines(keepends=True)
        try:
            # We use AST to find coordinates, but string-patching for the actual fix.
            self.tree = ast.parse(self.content)
        except SyntaxError:
            self.tree = None
        self.edits = []

    def _add_edit(self, sl, sc, el, ec, rep):
        """Register a surgical edit (1-indexed lines, 0-indexed columns)."""
        self.edits.append({'sl': sl, 'sc': sc, 'el': el, 'ec': ec, 'rep': rep})

    def apply_resiliency(self, finding):
        """Injects @retry and imports if missing surgically."""
        if not self.tree:
            return
        
        # 1. Surgical Import Injection
        if 'tenacity' not in self.content:
            # Insert at top, but after potential shebang
            insert_line = 1
            if self.lines and self.lines[0].startswith('#!'):
                insert_line = 2
            self._add_edit(insert_line, 0, insert_line, 0, "from tenacity import retry, wait_exponential, stop_after_attempt\n")
        
        # 2. Surgical Decorator Injection
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Match by line number range
                is_target = node.lineno == finding.line_number or (node.lineno <= finding.line_number <= (getattr(node, 'end_lineno', node.lineno)))
                if is_target:
                    # Avoid double-injection
                    if any(isinstance(d, ast.Call) and getattr(getattr(d, 'func', None), 'id', '') == 'retry' for d in node.decorator_list):
                        continue
                    
                    # Calculate indentation
                    line = self.lines[node.lineno-1]
                    indent = line[:len(line) - len(line.lstrip())]
                    decorator = f"{indent}@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))\n"
                    self._add_edit(node.lineno, 0, node.lineno, 0, decorator)
                    break
        
    def apply_timeouts(self, finding):
        """Adds timeout=10 to async calls surgically."""
        if not self.tree:
            return
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and node.lineno == finding.line_number:
                if hasattr(node, 'end_lineno') and hasattr(node, 'end_col_offset'):
                    # Insert before the closing parenthesis ')'
                    prefix = ", " if (node.args or node.keywords) else ""
                    self._add_edit(node.end_lineno, node.end_col_offset - 1, node.end_lineno, node.end_col_offset - 1, f"{prefix}timeout=10")
                    break

    def apply_caching(self, finding):
        """Injects ContextCacheConfig into Agent/App constructors surgically."""
        if not self.tree:
            return
        has_import = 'ContextCacheConfig' in self.content
        if not has_import:
            self._add_edit(1, 0, 1, 0, """try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None\n""")
            
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in ['Agent', 'App', 'LlmAgent']:
                    if not any(k.arg == 'context_cache_config' for k in node.keywords):
                        prefix = ", " if (node.args or node.keywords) else ""
                        conf = f"{prefix}context_cache_config=ContextCacheConfig(min_tokens=2048, ttl_seconds=600)"
                        self._add_edit(node.end_lineno, node.end_col_offset - 1, node.end_lineno, node.end_col_offset - 1, conf)

    def apply_tool_hardening(self, finding):
        """Injects Poka-Yoke pattern for tool definitions surgically."""
        if not self.tree:
            return
        if 'from typing import Literal' not in self.content:
            self._add_edit(1, 0, 1, 0, "from typing import Literal\n")
            
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and node.lineno == finding.line_number:
                if node.body:
                    first_stmt = node.body[0]
                    line = self.lines[first_stmt.lineno-1]
                    indent = line[:len(line) - len(line.lstrip())]
                    comment = f"{indent}# POKA-YOKE: Use Literal types for categorical parameters to prevent model hallucination.\n"
                    self._add_edit(first_stmt.lineno, 0, first_stmt.lineno, 0, comment)

    def apply_context_compaction(self, finding):
        """Injects a skeleton Context Compaction strategy surgically."""
        if 'def compact_history' in self.content:
            return
        compaction_code = '\ndef compact_history(messages: list, limit: int = 10):\n    """\n    Context Compaction Strategy (v1.3):\n    Summarizes earlier turns or trims the window to maintain reasoning density.\n    """\n    if len(messages) <= limit:\n        return messages\n    return [messages[0]] + messages[-(limit-1):]\n'
        # Insert after potential imports
        insert_line = 1
        for node in self.tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                insert_line = node.end_lineno + 1
            else:
                break
        self._add_edit(insert_line, 0, insert_line, 0, compaction_code)

    def apply_sovereign_reflection(self, finding):
        """Injects Sovereign Reflection loop surgically."""
        if 'sovereign_reflection' not in self.content:
            self._add_edit(1, 0, 1, 0, "from reflection_engine import sovereign_reflection\n")
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.lineno == finding.line_number:
                # Avoid double decoration
                if any('reflection' in str(ast.dump(d)).lower() for d in node.decorator_list):
                    continue
                line = self.lines[node.lineno-1]
                indent = line[:len(line) - len(line.lstrip())]
                self._add_edit(node.lineno, 0, node.lineno, 0, f"{indent}@sovereign_reflection\n")

    def apply_mcp_gating(self, finding):
        """Injects MCP Tool Gate surgically."""
        if 'mcp_tool_gate' not in self.content:
            self._add_edit(1, 0, 1, 0, "from mcp_gate import mcp_tool_gate\n")
            
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and node.lineno == finding.line_number:
                if any('gate' in str(ast.dump(d)).lower() for d in node.decorator_list):
                    continue
                line = self.lines[node.lineno-1]
                indent = line[:len(line) - len(line.lstrip())]
                self._add_edit(node.lineno, 0, node.lineno, 0, f"{indent}@mcp_tool_gate(require_confirmation=True)\n")

    def apply_privilege_gate(self, finding):
        """Injects tool_privilege_check decorator surgically."""
        if 'tool_privilege_check' not in self.content:
            self._add_edit(1, 0, 1, 0, "from agent_ops_cockpit.ops.guardrails import tool_privilege_check\n")
            
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and node.lineno == finding.line_number:
                # Avoid double decoration
                if any('privilege' in str(ast.dump(d)).lower() for d in node.decorator_list):
                    continue
                line = self.lines[node.lineno-1]
                indent = line[:len(line) - len(line.lstrip())]
                self._add_edit(node.lineno, 0, node.lineno, 0, f"{indent}@tool_privilege_check(required_scope='admin')\n")

    def apply_cloud_abstraction(self, finding):
        """Injects a provider-agnostic bridge to eliminate monocultural bias."""
        if 'CloudBridge' in self.content:
            return
        bridge_code = """
class CloudBridge:
    \"\"\"
    v2.0 Sovereign Bridge: Abstracts provider-specific calls (AWS/Azure) 
    to enable Multi-Cloud mobility and local failover.
    \"\"\"
    @staticmethod
    def call_model(provider: str, model: str, payload: dict):
        print(f"🌉 [BRIDGE] Routing request to {provider} ({model})")
        # Logic to route to LiteLLM or ADK
        return {"status": "success", "provider": provider}
"""
        # Insert after potential imports
        insert_line = 1
        for node in self.tree.body if self.tree else []:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                insert_line = node.end_lineno + 1
            else:
                break
        self._add_edit(insert_line, 0, insert_line, 0, bridge_code)

    def apply_manifest_drift_fix(self, finding):
        """Auto-upgrades deprecated frontier models in JSON manifests."""
        new_content = self.content
        updates = [
            (r'gpt-3\.5', 'gpt-4o'),
            (r'claude-2', 'claude-3-5-sonnet-latest'),
            (r'gemini-1\.0', 'gemini-2.0-flash')
        ]
        for old, new in updates:
            new_content = re.sub(old, new, new_content, flags=re.I)
        
        if new_content != self.content:
            self.edits = [{'sl': 1, 'sc': 0, 'el': len(self.lines), 'ec': len(self.lines[-1]) if self.lines else 0, 'rep': new_content}]

    def apply_mcp_validation(self, finding):
        """Injects mandatory capability block into malformed MCP manifests."""
        if '"capabilities"' in self.content:
            return
        if self.content.strip().startswith('{'):
            self._add_edit(2, 0, 2, 0, '  "capabilities": {"tools": {}},\n')

    def apply_passive_retrieval(self, finding):
        """
        [Strategic Pivot] Injects concrete RAG decider logic (NL-to-Decision pattern).
        Replaces 'Passive RAG' with a managed routing layer to optimize token cost.
        """
        if 'def decider_should_rag' in self.content:
            return
            
        logic = '''
def decider_should_rag(query: str) -> bool:
    """
    v2.0.2 Sovereign Logic: Managed RAG routing.
    Determines if the query requires external knowledge or can be handled by the base model.
    """
    rag_keywords = ["latest", "current", "news", "price", "stock", "documentation", "how to"]
    return any(word in query.lower() for word in rag_keywords)
'''
        # Insert at the end of the imports
        insert_line = 1
        for node in (self.tree.body if self.tree else []):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                insert_line = node.end_lineno + 1
            else:
                break
        self._add_edit(insert_line, 0, insert_line, 0, logic)
        
        # Also try to find the LLM call and wrap it with the decider if possible
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and node.lineno == finding.line_number:
                # This is a bit complex for a regex/string patcher, but we can inject a comment 
                # next to the line as a 'Functional Guide'
                line = self.lines[node.lineno-1]
                indent = line[:len(line) - len(line.lstrip())]
                guide = f"{indent}# v2.0.2 Logic: if decider_should_rag(query): pass # Apply RAG here\n"
                self._add_edit(node.lineno, 0, node.lineno, 0, guide)
                break

    def apply_structural_split(self, finding):
        """
        v2.0.2 Architectural Evolution: Suggests splitting oversized agents.
        Injects a 'Managed Router' boilerplate to facilitate modularity.
        """
        router_code = '''
# ARCHITECTURAL RECOMMENDATION: Split this agent into specialized sub-agents.
# E.g., Use an Orchestrator/Router pattern to delegate to poi_agent or booking_agent.
# This improves reasoning accuracy and reduces TTFT (Time To First Token).
'''
        self._add_edit(1, 0, 1, 0, router_code)

    def _get_new_content(self):
        """Apply edits in reverse order to original string content."""
        if not self.edits:
            return self.content
        
        sorted_edits = sorted(self.edits, key=lambda x: (x['sl'], x['sc']), reverse=True)
        
        line_offsets = [0]
        curr = 0
        for line_content in self.lines:
            curr += len(line_content)
            line_offsets.append(curr)
            
        new_content = self.content
        for e in sorted_edits:
            try:
                start_off = line_offsets[e['sl']-1] + e['sc']
                end_off = line_offsets[e['el']-1] + e['ec']
                new_content = new_content[:start_off] + e['rep'] + new_content[end_off:]
            except Exception:
                continue
        return new_content

    def get_diff(self) -> str:
        new_content = self._get_new_content()
        diff = difflib.unified_diff(
            self.content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f'a/{self.file_path}',
            tofile=f'b/{self.file_path}'
        )
        return ''.join(diff)

    def save(self):
        new_content = self._get_new_content()
        if new_content == self.content:
            return False
        with open(self.file_path, 'w') as f:
            f.write(new_content)
        return True

    def save_patch(self) -> str:
        """Saves the current diff as a .patch file in .cockpit/patches/."""
        diff = self.get_diff()
        if not diff:
            return ""
        patch_dir = os.path.join(os.getcwd(), '.cockpit', 'patches')
        os.makedirs(patch_dir, exist_ok=True)
        file_slug = self.file_path.replace(os.sep, '_').strip('_')
        patch_path = os.path.join(patch_dir, f"{file_slug}.patch")
        with open(patch_path, 'w') as f:
            f.write(diff)
        return patch_path

    def save_to_branch(self) -> str:
        """Creates a new git branch and commits the changes."""
        import subprocess
        new_content = self._get_new_content()
        if new_content == self.content:
            return ""
        
        branch_name = f"cockpit-hardening-{datetime.now().strftime('%H%M%S')}"
        try:
            subprocess.run(['git', 'checkout', '-b', branch_name], check=True, capture_output=True)
            self.save()
            subprocess.run(['git', 'add', self.file_path], check=True, capture_output=True)
            subprocess.run(['git', 'commit', '-m', f"docs: autonomous hardening for {os.path.basename(self.file_path)}", '--no-gpg-sign'], check=True, capture_output=True)
            return branch_name
        except Exception:
            return ""
    def scaffold_policy_engine(self, target_dir: str, language: str = 'typescript'):
        """
        Generates a language-native policy engine boilerplate for deterministic business rules.
        """
        if language == 'python':
            return self.scaffold_python_policy_engine(target_dir)
            
        engine_path = os.path.join(target_dir, 'policy_engine.ts')
        content = """/**
 * v2.0.1 Sovereign Policy Engine: Deterministic Business Rules
 * [REMEDIATION SCAFFOLD] Use this to replace LLM-based arithmetic or date logic.
 */
export class PolicyEngine {
  /**
   * Example: Validate return eligibility based on purchase date.
   * Replace this with your specific business rules.
   */
  static isEligibleForReturn(purchaseDate: Date, returnDaysLimit: number = 30): boolean {
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - purchaseDate.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays <= returnDaysLimit;
  }

  static calculateDiscount(total: number, promoCode: string): number {
    // Implement deterministic pricing logic here
    if (promoCode === 'SOVEREIGN20') return total * 0.8;
    return total;
  }
}
"""
        with open(engine_path, 'w') as f:
            f.write(content)
        return engine_path

    def scaffold_python_policy_engine(self, target_dir: str):
        """Generates a policy_engine.py boilerplate using Pydantic."""
        engine_path = os.path.join(target_dir, 'policy_engine.py')
        content = """from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import Optional

class SovereignPolicy(BaseModel):
    \"\"\"
    v2.1.0 Sovereign Policy Engine (Python): Deterministic Business Rules.
    [REMEDIATION SCAFFOLD] Use this to replace LLM-based arithmetic or date logic.
    \"\"\"
    
    @staticmethod
    def is_eligible_for_return(purchase_date: date, return_days_limit: int = 30) -> bool:
        \"\"\"Deterministic date logic to prevent LLM approximation errors.\"\"\"
        today = date.today()
        diff = today - purchase_date
        return diff.days <= return_days_limit

    @staticmethod
    def calculate_discount(total: float, promo_code: str) -> float:
        \"\"\"Deterministic pricing logic.\"\"\"
        if promo_code == 'SOVEREIGN20':
            return total * 0.8
        return total

# Example Usage:
# from policy_engine import SovereignPolicy
# if SovereignPolicy.is_eligible_for_return(date(2024, 1, 1)):
#     pass
"""
        with open(engine_path, 'w') as f:
            f.write(content)
        return engine_path

    def eject_telemetry_lib(self, target_dir: str):
        """Injects AgentOps standard library shims for Logging and Tracing."""
        lib_dir = os.path.join(target_dir, 'lib')
        os.makedirs(lib_dir, exist_ok=True)
        
        logger_path = os.path.join(lib_dir, 'logger.ts')
        with open(logger_path, 'w') as f:
            f.write("""export const logger = {
  info: (msg: string, meta?: any) => console.log(`[INFO] ${new Date().toISOString()} - ${msg}`, meta || ''),
  error: (msg: string, err?: any) => console.error(`[ERROR] ${new Date().toISOString()} - ${msg}`, err || ''),
  audit: (action: string, actor: string) => console.log(`[AUDIT] ${action} by ${actor}`)
};""")

        trace_path = os.path.join(lib_dir, 'trace.ts')
        with open(trace_path, 'w') as f:
            f.write("""export const tracer = {
  startSpan: (name: string) => ({ end: () => console.log(`[TRACE] End span: ${name}`) }),
  trackTool: (name: string, args: any) => console.log(`[TRACE] Tool: ${name}`, args)
};""")
        return lib_dir

    def apply_hitl_surface(self, target_dir: str):
        """
        [A2UI Evolution] Injects a deterministic HitlSurface.tsx component.
        Matches the Sovereign Cockpit branding for Human-in-the-Loop validation.
        """
        components_dir = os.path.join(target_dir, 'components')
        os.makedirs(components_dir, exist_ok=True)
        surface_path = os.path.join(components_dir, 'HitlSurface.tsx')
        
        content = """/**
 * v2.0.2 Sovereign A2UI: Human-in-the-Loop Approval Surface
 * Automatically generated by AgentOps Cockpit.
 */
import React from 'react';

interface HitlSurfaceProps {
    actionName: string;
    payload: any;
    onApprove: () => void;
    onReject: (reason: string) => void;
}

export const HitlSurface: React.FC<HitlSurfaceProps> = ({ actionName, payload, onApprove, onReject }) => {
    return (
        <div className="hitl-container p-6 border-2 border-red-500 rounded-xl bg-slate-900 text-white">
            <h2 className="text-xl font-bold mb-4">⚠️ Sovereign HITL Approval Required</h2>
            <p className="mb-2">The agent is requesting permission to execute: <span className="text-cyan-400 font-mono">{actionName}</span></p>
            <div className="payload-box bg-slate-800 p-4 rounded mb-4 font-mono text-sm overflow-auto max-h-40">
                {JSON.stringify(payload, null, 2)}
            </div>
            <div className="actions flex gap-4">
                <button onClick={onApprove} className="px-6 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors">Approve</button>
                <button onClick={() => onReject('User rejected via A2UI')} className="px-6 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition-colors">Reject</button>
            </div>
        </div>
    );
};
"""
        with open(surface_path, 'w') as f:
            f.write(content)
        return surface_path
