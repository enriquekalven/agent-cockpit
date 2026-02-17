try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.8.4 Sovereign Alignment: Optimized for Google Cloud Run
import ast
from typing import List
from .base import BaseAuditor, AuditFinding

class ReliabilityAuditor(BaseAuditor):
    """
    Analyzes code for execution patterns, identifying sequential bottlenecks and missing resiliency.
    """

    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        from agent_ops_cockpit.ops.discovery import DiscoveryEngine
        discovery = DiscoveryEngine()
        if discovery.is_library_file(file_path):
            return []
            
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                await_nodes = [n for n in ast.walk(node) if isinstance(n, ast.Await)]
                if len(await_nodes) > 2:
                    title = 'Sequential Bottleneck Detected'
                    if not self._is_ignored(node.lineno, content, title):
                        findings.append(AuditFinding(category='🧗 Reliability & Perf', title=title, description="Multiple sequential 'await' calls identified. This increases total latency linearly.", impact='MEDIUM', roi='Reduces latency by up to 50% using asyncio.gather().', line_number=node.lineno, file_path=file_path))
            
            if isinstance(node, ast.Call):
                func_name = ''
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                
                if any((x in func_name.lower() for x in ['get', 'post', 'request', 'fetch', 'query'])):
                    # Smarter Resiliency: Only flag if targeting external http/https endpoints
                    is_external = False
                    if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                        if node.args[0].value.startswith(('http://', 'https://')):
                            is_external = True
                    
                    if is_external:
                        parent = self._get_parent_function(tree, node)
                        # If no parent (top-level), it's definitely not decorated with @retry
                        if not parent or (not self._is_decorated_with_retry(parent)):
                            title = 'Missing Resiliency Logic'
                            if not self._is_ignored(node.lineno, content, title):
                                findings.append(AuditFinding(category='🧗 Reliability', title=title, description=f"External call '{func_name}' to '{node.args[0].value[:30]}...' is not protected by retry logic.", impact='HIGH', roi='Increases up-time and handles transient network failures.', line_number=node.lineno, file_path=file_path))
            
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                if isinstance(node.value, (ast.Constant, ast.JoinedStr)):
                    val = ''
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        val = node.value.value
                    elif isinstance(node.value, ast.JoinedStr):
                        val = ''.join([s.value for s in node.value.values if isinstance(s, ast.Constant)])
                    if len(val) > 20 and any((x in val.lower() for x in ['act as', 'you are', 'instruction'])):
                        if not any((x in val.lower() for x in ["don't know", 'unsure', 'refuse', 'do not make up'])):
                            title = 'High Hallucination Risk'
                            if not self._is_ignored(node.lineno, content, title):
                                findings.append(AuditFinding(category='🧗 Reliability', title=title, description="System prompt lacks negative constraints (e.g., 'If you don't know, say I don't know').", impact='HIGH', roi='Reduces autonomous failures by enforcing refusal boundaries.', line_number=node.lineno, file_path=file_path))
        return findings

    def _get_parent_function(self, tree, node):
        for p in ast.walk(tree):
            if isinstance(p, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if any((n is node for n in ast.walk(p))):
                    return p
        return None

    def _is_decorated_with_retry(self, node):
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and 'retry' in decorator.id.lower():
                return True
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and ('retry' in decorator.func.id.lower()):
                return True
        return False