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
                if node.lineno == finding.line_number or any(f.title == finding.title for f in []): # Match by line or title
                    # Add @retry(wait=wait_exponential(...))
                    retry_decorator = ast.parse("retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))").body[0].value
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

    def save(self):
        """Saves the transformed AST back to the file using native ast.unparse."""
        new_code = ast.unparse(self.tree)
        with open(self.file_path, 'w') as f:
            f.write(new_code)
        return True
