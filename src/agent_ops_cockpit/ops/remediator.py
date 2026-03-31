import ast
import difflib
import os
from datetime import datetime

import libcst as cst

try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None

class ModernResiliencyTransformer(cst.CSTTransformer):
    """v2.0.7 Engineered Logic: Layout-preserving transformation using LibCST."""
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
    while preserving license headers, comments, and formatting. (v2.0.7 Cockpit Diffing)
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            self.content = f.read()
        self.original_content = self.content
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

    def _apply_cst_transformer(self, transformer):
        try:
            import libcst as cst
            from libcst.metadata import MetadataWrapper
            module = cst.parse_module(self.content)
            wrapper = MetadataWrapper(module)
            modified_module = wrapper.visit(transformer)
            self.content = modified_module.code
            self.lines = self.content.splitlines(keepends=True)
            self.tree = ast.parse(self.content)
        except Exception as e:
            print(f"LibCST Transformation Failed: {e}")

    def apply_resiliency(self, finding):
        """Injects @retry and imports if missing using LibCST AST rewriting directly."""
        try:
            import libcst as cst
            from libcst.metadata import PositionProvider
            
            class ResiliencyTransformer(cst.CSTTransformer):
                METADATA_DEPENDENCIES = (PositionProvider,)
                
                def __init__(self, target_line, module_code):
                    self.target_line = target_line
                    self.found = False
                    self.added_import = 'tenacity' in module_code
                
                def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
                    if not self.added_import:
                        import_stmt = cst.parse_statement("from tenacity import retry, wait_exponential, stop_after_attempt\n")
                        new_body = [import_stmt] + list(updated_node.body)
                        return updated_node.with_changes(body=tuple(new_body))
                    return updated_node

                def _apply_retry(self, original_node, updated_node):
                    if self.found:
                        return updated_node
                    pos = self.get_metadata(PositionProvider, original_node)
                    if pos and pos.start.line == self.target_line:
                        self.found = True
                        dummy = cst.parse_module("@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))\ndef f(): pass")
                        retry_dec = dummy.body[0].decorators[0]
                        new_decorators = list(updated_node.decorators)
                        new_decorators.insert(0, retry_dec)
                        return updated_node.with_changes(decorators=new_decorators)
                    return updated_node

                def leave_FunctionDef(self, original_node, updated_node):
                    return self._apply_retry(original_node, updated_node)

                def leave_AsyncFunctionDef(self, original_node, updated_node):
                    return self._apply_retry(original_node, updated_node)
            
            self._apply_cst_transformer(ResiliencyTransformer(finding.line_number, self.content))
        except ImportError:
            pass
        
    def apply_timeouts(self, finding):
        """Adds timeout=10 to async calls surgically."""
        try:
            import libcst as cst
            from libcst.metadata import PositionProvider
            
            class TimeoutTransformer(cst.CSTTransformer):
                METADATA_DEPENDENCIES = (PositionProvider,)
                
                def __init__(self, target_line):
                    self.target_line = target_line
                    self.found = False

                def leave_Call(self, original_node, updated_node):
                    if getattr(self, 'found', False):
                        return updated_node
                    pos = self.get_metadata(PositionProvider, original_node)
                    if pos and pos.start.line == self.target_line:
                        self.found = True
                        new_kw = cst.Arg(
                            keyword=cst.Name("timeout"), 
                            equal=cst.AssignEqual(whitespace_before=cst.SimpleWhitespace(''), whitespace_after=cst.SimpleWhitespace('')), 
                            value=cst.Integer("10")
                        )
                        new_args = list(updated_node.args)
                        if not any(arg.keyword and arg.keyword.value == "timeout" for arg in new_args):
                            new_args.append(new_kw)
                        return updated_node.with_changes(args=tuple(new_args))
                    return updated_node

            self._apply_cst_transformer(TimeoutTransformer(finding.line_number))
        except ImportError:
            pass

    def apply_caching(self, finding):
        """Injects ContextCacheConfig into Agent/App constructors surgically."""
        try:
            import libcst as cst
            from libcst.metadata import PositionProvider
            
            class CachingTransformer(cst.CSTTransformer):
                METADATA_DEPENDENCIES = (PositionProvider,)
                
                def __init__(self, target_line, module_code):
                    self.target_line = target_line
                    self.found = False
                    self.added_import = 'ContextCacheConfig' in module_code
                
                def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
                    if not self.added_import:
                        import_stmt = cst.parse_statement(
                            "try:\n"
                            "    from google.adk.agents.context_cache_config import ContextCacheConfig\n"
                            "except (ImportError, AttributeError, ModuleNotFoundError):\n"
                            "    ContextCacheConfig = None\n"
                        )
                        new_body = [import_stmt] + list(updated_node.body)
                        return updated_node.with_changes(body=tuple(new_body))
                    return updated_node

                def leave_Call(self, original_node, updated_node):
                    if self.found:
                        return updated_node
                    pos = self.get_metadata(PositionProvider, original_node)
                    if pos and pos.start.line == getattr(self, 'target_line', 0):
                        if isinstance(original_node.func, cst.Name) and original_node.func.value in ['Agent', 'App', 'LlmAgent']:
                            self.found = True
                            
                            val = cst.Call(
                                func=cst.Name("ContextCacheConfig"),
                                args=[
                                    cst.Arg(keyword=cst.Name("min_tokens"), value=cst.Integer("2048")),
                                    cst.Arg(keyword=cst.Name("ttl_seconds"), value=cst.Integer("600"))
                                ]
                            )
                            new_kw = cst.Arg(
                                keyword=cst.Name("context_cache_config"), 
                                equal=cst.AssignEqual(whitespace_before=cst.SimpleWhitespace(''), whitespace_after=cst.SimpleWhitespace('')),
                                value=val
                            )
                            new_args = list(updated_node.args)
                            if not any(arg.keyword and arg.keyword.value == "context_cache_config" for arg in new_args):
                                new_args.append(new_kw)
                            return updated_node.with_changes(args=tuple(new_args))
                    return updated_node

            self._apply_cst_transformer(CachingTransformer(finding.line_number, self.content))
        except ImportError:
            pass

    def apply_tool_hardening(self, finding):
        """Injects Poka-Yoke pattern for tool definitions surgically."""
        try:
            import libcst as cst
            from libcst.metadata import PositionProvider
            
            class PokaYokeTransformer(cst.CSTTransformer):
                METADATA_DEPENDENCIES = (PositionProvider,)
                
                def __init__(self, target_line, module_code):
                    self.target_line = target_line
                    self.found = False
                    self.added_import = 'from typing import Literal' in module_code
                
                def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
                    if not self.added_import:
                        import_stmt = cst.parse_statement("from typing import Literal\n")
                        new_body = [import_stmt] + list(updated_node.body)
                        return updated_node.with_changes(body=tuple(new_body))
                    return updated_node

                def leave_FunctionDef(self, original_node, updated_node):
                    if getattr(self, 'found', False):
                        return updated_node
                    pos = self.get_metadata(PositionProvider, original_node)
                    if pos and pos.start.line == self.target_line:
                        self.found = True
                        new_body_elements = [cst.SimpleStatementLine(body=[])] if not updated_node.body.body else list(updated_node.body.body)
                        dummy = cst.parse_statement("'''POKA-YOKE: Use Literal types for categorical parameters to prevent model hallucination.'''\n")
                        new_body_elements.insert(0, dummy)
                        return updated_node.with_changes(body=updated_node.body.with_changes(body=tuple(new_body_elements)))
                    return updated_node

            self._apply_cst_transformer(PokaYokeTransformer(finding.line_number, self.content))
        except ImportError:
            pass

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

    def _apply_decorator_cst(self, finding, decorator_code, import_code, import_check_str):
        try:
            import libcst as cst
            from libcst.metadata import PositionProvider
            
            class GenericDecoratorTransformer(cst.CSTTransformer):
                METADATA_DEPENDENCIES = (PositionProvider,)
                
                def __init__(self, target_line, module_code):
                    self.target_line = target_line
                    self.found = False
                    self.added_import = import_check_str in module_code
                
                def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
                    if not self.added_import:
                        import_stmt = cst.parse_statement(import_code)
                        new_body = [import_stmt] + list(updated_node.body)
                        return updated_node.with_changes(body=tuple(new_body))
                    return updated_node

                def _apply_decorator(self, original_node, updated_node):
                    if getattr(self, 'found', False):
                        return updated_node
                    pos = self.get_metadata(PositionProvider, original_node)
                    if pos and pos.start.line == getattr(self, 'target_line', 0):
                        self.found = True
                        dummy = cst.parse_module(f"{decorator_code}\ndef dummy_f(): pass")
                        new_dec = dummy.body[0].decorators[0]
                        if any(d.decorator == new_dec.decorator for d in updated_node.decorators):
                            return updated_node
                        new_decorators = list(updated_node.decorators)
                        new_decorators.insert(0, new_dec)
                        return updated_node.with_changes(decorators=new_decorators)
                    return updated_node

                def leave_FunctionDef(self, original_node, updated_node):
                    return self._apply_decorator(original_node, updated_node)

                def leave_AsyncFunctionDef(self, original_node, updated_node):
                    return self._apply_decorator(original_node, updated_node)

            self._apply_cst_transformer(GenericDecoratorTransformer(finding.line_number, self.content))
        except ImportError:
            pass

    def apply_cockpit_reflection(self, finding):
        """Injects Cockpit Reflection loop surgically."""
        self._apply_decorator_cst(
            finding, 
            "@cockpit_reflection", 
            "from reflection_engine import cockpit_reflection\n", 
            "cockpit_reflection"
        )

    def apply_mcp_gating(self, finding):
        """Injects MCP Tool Gate surgically."""
        self._apply_decorator_cst(
            finding, 
            "@mcp_tool_gate(require_confirmation=True)", 
            "from mcp_gate import mcp_tool_gate\n", 
            "mcp_tool_gate"
        )

    def apply_privilege_gate(self, finding):
        """Injects tool_privilege_check decorator surgically."""
        self._apply_decorator_cst(
            finding, 
            "@tool_privilege_check(required_scope='admin')", 
            "from agent_ops_cockpit.ops.guardrails import tool_privilege_check\n", 
            "tool_privilege_check"
        )

    def apply_cloud_abstraction(self, finding):
        """Injects a provider-agnostic bridge to eliminate monocultural bias."""
        self._apply_module_injection_cst(
            finding,
            "class CloudBridge:\n    '''Abstracted Cloud SDK Wrapper for Multi-Cloud Compliance.'''\n    def upload(self, bucket, data):\n        pass\n",
            "class CloudBridge"
        )

    def apply_manifest_drift_fix(self, finding):
        """Upgrades manifest JSON or Py configs safely."""
        try:
            import re
            new_content = re.sub(r'gpt-3\.5(-turbo)?', 'gpt-4o-mini', self.content, flags=re.I)
            new_content = re.sub(r'gemini-1\.0(-\w+)?', 'gemini-2.0-flash', new_content, flags=re.I)
            new_content = re.sub(r'claude-2', 'claude-3-5-haiku', new_content, flags=re.I)
            self.content = new_content
            self.lines = self.content.splitlines(keepends=True)
            import ast
            try:
                self.tree = ast.parse(self.content)
            except SyntaxError:
                self.tree = None
        except Exception:
            pass

    def apply_mcp_validation(self, finding):
        """Injects mandatory capability block into malformed MCP manifests."""
        if '"capabilities"' in self.content:
            return
        if self.content.strip().startswith('{'):
            self._add_edit(2, 0, 2, 0, '  "capabilities": {"tools": {}},\n')

    def apply_passive_retrieval(self, finding):
        """Injects Passive Retrieval logic surgically."""
        try:
            import libcst as cst
            from libcst.metadata import PositionProvider
            
            class PassiveRetrievalTransformer(cst.CSTTransformer):
                METADATA_DEPENDENCIES = (PositionProvider,)
                
                def __init__(self, target_line, module_code):
                    self.target_line = target_line
                    self.found = False
                    self.added_already = 'def decider_should_rag' in module_code
                
                def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
                    new_body = list(updated_node.body)
                    if not self.added_already:
                        decider_code = "def decider_should_rag(query: str) -> bool:\n    '''Fast semantic routing to avoid RAG inference waste.'''\n    return 'report' in query or 'data' in query\n"
                        injected_stmt = cst.parse_statement(decider_code)
                        idx = 0
                        for i, stmt in enumerate(new_body):
                            if isinstance(stmt, (cst.SimpleStatementLine)) and any(isinstance(n, (cst.Import, cst.ImportFrom)) for n in stmt.body):
                                idx = i + 1
                        new_body.insert(idx, injected_stmt)
                    return updated_node.with_changes(body=tuple(new_body))

                def leave_Call(self, original_node, updated_node):
                    if getattr(self, 'found', False):
                        return updated_node
                    pos = self.get_metadata(PositionProvider, original_node)
                    if pos and pos.start.line == self.target_line:
                        if isinstance(original_node.func, cst.Name) and original_node.func.value == 'retrieve':
                            self.found = True
                            dummy = cst.parse_expression("decider_should_rag(query) and dummy_func()")
                            new_node = dummy.with_changes(right=updated_node)
                            return new_node
                    return updated_node

            self._apply_cst_transformer(PassiveRetrievalTransformer(finding.line_number, self.content))
        except ImportError:
            pass

    def apply_structural_split(self, finding):
        """
        v2.0.7 Architectural Evolution: Suggests splitting oversized agents.
        Injects a 'Managed Router' boilerplate to facilitate modularity.
        """
        router_code = '''
# ARCHITECTURAL RECOMMENDATION: Split this agent into specialized sub-agents.
# E.g., Use an Orchestrator/Router pattern to delegate to poi_agent or booking_agent.
# This improves reasoning accuracy and reduces TTFT (Time To First Token).
'''
        self._apply_module_injection_cst(
            finding,
            "class ActionRouter:\n    '''Separation of Concerns: Routes instructions instead of monolithic tool calling.'''\n    def route(self, intent: str):\n        pass\n" + router_code,
            "class ActionRouter"
        )

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
        original = getattr(self, 'original_content', self.content)
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f'a/{self.file_path}',
            tofile=f'b/{self.file_path}'
        )
        return ''.join(diff)

    def save(self):
        new_content = self._get_new_content()
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='replace') as f:
                disk_content = f.read()
            if new_content == disk_content:
                return False
        except Exception:
            pass
        with open(self.file_path, 'w', encoding='utf-8') as f:
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

    def save_html_diff(self) -> str:
        """Generates a side-by-side HTML diff report for easy analysis."""
        new_content = self._get_new_content()
        original = getattr(self, 'original_content', self.content)
        if new_content == original:
            return ""
            
        html_diff = difflib.HtmlDiff().make_file(
            original.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromdesc=f"Original: {os.path.basename(self.file_path)}",
            todesc=f"Evolved: {os.path.basename(self.file_path)}",
            context=False,
            numlines=3
        )
        
        diff_dir = os.path.join(os.getcwd(), '.cockpit', 'evidence_lake', 'diffs')
        os.makedirs(diff_dir, exist_ok=True)
        
        file_slug = os.path.basename(self.file_path)
        timestamp = datetime.now().strftime('%H%M%S')
        diff_path = os.path.join(diff_dir, f"{file_slug}_evolution_{timestamp}.html")
        
        # Add basic styling improvements to the default difflib HTML
        styled_html = html_diff.replace(
            '<style type="text/css">',
            '<style type="text/css">\n    body { font-family: "Courier New", monospace; background-color: #0f172a; color: #f8fafc; }\n    table.diff { width: 100%; border-collapse: collapse; }\n    table.diff th { background-color: #1e293b; padding: 10px; border: 1px solid #334155; }\n    table.diff td { padding: 4px 8px; border: 1px solid #334155; }\n    .diff_add { background-color: #064e3b; }\n    .diff_chg { background-color: #422006; }\n    .diff_sub { background-color: #7f1d1d; }\n'
        )
        
        with open(diff_path, 'w', encoding='utf-8') as f:
            f.write(styled_html)
        return diff_path

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
 * v2.0.1 Cockpit Policy Engine: Deterministic Business Rules
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
    if (promoCode === 'COCKPIT20') return total * 0.8;
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

class CockpitPolicy(BaseModel):
    \"\"\"
    v2.1.0 Cockpit Policy Engine (Python): Deterministic Business Rules.
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
        if promo_code == 'COCKPIT20':
            return total * 0.8
        return total

# Example Usage:
# from policy_engine import CockpitPolicy
# if CockpitPolicy.is_eligible_for_return(date(2024, 1, 1)):
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
        Matches the Cockpit Cockpit branding for Human-in-the-Loop validation.
        """
        components_dir = os.path.join(target_dir, 'components')
        os.makedirs(components_dir, exist_ok=True)
        surface_path = os.path.join(components_dir, 'HitlSurface.tsx')
        
        content = """/**
 * v2.0.7 Cockpit A2UI: Human-in-the-Loop Approval Surface
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
            <h2 className="text-xl font-bold mb-4">⚠️ Cockpit HITL Approval Required</h2>
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
