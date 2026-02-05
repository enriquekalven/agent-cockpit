import ast
from .auditors.base import AuditFinding

class CodeRemediator:
    """
    Phase 4: The 'Closer' - Automated Remediation Engine.
    Transforms AST based on audit findings to inject best practices.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(file_path, 'r') as f:
            self.content = f.read()
        self.tree = ast.parse(self.content)

    def apply_resiliency(self, finding: AuditFinding):
        """Injects @retry and imports if missing."""
        has_tenacity = "tenacity" in self.content
        
        class RetryInjector(ast.NodeTransformer):
            def visit_FunctionDef(self, node):
                # Check if the finding line is within this function definition
                # node.lineno is the start, end_lineno is the end (available in Python 3.8+)
                is_target = False
                if node.lineno == finding.line_number:
                     is_target = True
                elif hasattr(node, 'end_lineno') and node.lineno <= finding.line_number <= node.end_lineno:
                     is_target = True
                
                if is_target:
                    # Add @retry(wait=wait_exponential(...))
                    retry_decorator = ast.parse("retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))").body[0].value
                    # Avoid double decoration
                    if not any(isinstance(d, ast.Call) and getattr(getattr(d, 'func', None), 'id', '') == 'retry' for d in node.decorator_list):
                        node.decorator_list.append(retry_decorator)
                return node
            
            def visit_AsyncFunctionDef(self, node):
                return self.visit_FunctionDef(node)

        self.tree = RetryInjector().visit(self.tree)
        
        if not has_tenacity:
             # Prepend imports
             import_node = ast.parse("from tenacity import retry, wait_exponential, stop_after_attempt\n").body[0]
             self.tree.body.insert(0, import_node)

    def apply_timeouts(self, finding: AuditFinding):
        """Adds timeout=10 to async calls."""
        class TimeoutInjector(ast.NodeTransformer):
            def visit_Call(self, node):
                if node.lineno == finding.line_number:
                    # Add timeout=10 keyword
                    node.keywords.append(ast.keyword(arg='timeout', value=ast.Constant(value=10)))
                return node
        
        self.tree = TimeoutInjector().visit(self.tree)

    def apply_caching(self, finding: AuditFinding):
        """Injects ContextCacheConfig into Agent/App constructors."""
        class CachingInjector(ast.NodeTransformer):
            def visit_Call(self, node):
                # Target Agent, App, or LlmAgent constructors
                if isinstance(node.func, ast.Name) and node.func.id in ['Agent', 'App', 'LlmAgent']:
                    # Check if context_cache_config is already there
                    if not any(k.arg == 'context_cache_config' for k in node.keywords):
                        cache_config = ast.Call(
                            func=ast.Name(id='ContextCacheConfig', ctx=ast.Load()),
                            args=[],
                            keywords=[
                                ast.keyword(arg='min_tokens', value=ast.Constant(value=2048)),
                                ast.keyword(arg='ttl_seconds', value=ast.Constant(value=600))
                            ]
                        )
                        node.keywords.append(ast.keyword(arg='context_cache_config', value=cache_config))
                return node
        
        self.tree = CachingInjector().visit(self.tree)
        
        if "ContextCacheConfig" not in self.content:
             import_node = ast.parse("from google.adk.agents.context_cache_config import ContextCacheConfig\n").body[0]
             self.tree.body.insert(0, import_node)

    def apply_tool_hardening(self, finding: AuditFinding):
        """Injects Literal import and Poka-Yoke pattern for tool definitions."""
        if "from typing import Literal" not in self.content:
            import_node = ast.parse("from typing import Literal\n").body[0]
            self.tree.body.insert(0, import_node)
        
        class ToolHardener(ast.NodeTransformer):
            def visit_FunctionDef(self, node):
                # Look for parameters that could benefit from Literals (categorical strings)
                # and add a Poka-Yoke comment if it's the target line
                if node.lineno == finding.line_number:
                    node.body.insert(0, ast.Expr(value=ast.Constant(value="POKA-YOKE: Use Literal types for categorical parameters to prevent model hallucination.")))
                return node
        
        self.tree = ToolHardener().visit(self.tree)

    def apply_context_compaction(self, finding: AuditFinding):
        """Injects a skeleton Context Compaction strategy."""
        compaction_code = """
def compact_history(messages: list, limit: int = 10):
    \"\"\"
    Context Compaction Strategy (v1.3): 
    Summarizes earlier turns or trims the window to maintain reasoning density.
    \"\"\"
    if len(messages) <= limit:
        return messages
    # Keep system prompt, keep last N messages
    return [messages[0]] + messages[-(limit-1):]
"""
        compaction_node = ast.parse(compaction_code).body[0]
        # Insert at the top of the file but after imports
        self.tree.body.insert(1, compaction_node)

    def get_diff(self) -> str:
        """Returns a unified diff of the changes without saving to disk."""
        import difflib
        new_code = ast.unparse(self.tree)
        diff = difflib.unified_diff(
            self.content.splitlines(keepends=True),
            new_code.splitlines(keepends=True),
            fromfile=f"a/{self.file_path}",
            tofile=f"b/{self.file_path}"
        )
        return "".join(diff)

    def save(self):
        """Saves the transformed AST back to the file using native ast.unparse."""
        new_code = ast.unparse(self.tree)
        with open(self.file_path, 'w') as f:
            f.write(new_code)
        return True
