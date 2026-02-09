from tenacity import retry, wait_exponential, stop_after_attempt
import ast
from typing import List
from .base import BaseAuditor, AuditFinding

class ReliabilityAuditor(BaseAuditor):
    """
    Analyzes code for execution patterns, identifying sequential bottlenecks and missing resiliency.
    """

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                await_nodes = [n for n in ast.walk(node) if isinstance(n, ast.Await)]
                if len(await_nodes) > 2:
                    findings.append(AuditFinding(category='🧗 Reliability & Perf', title='Sequential Bottleneck Detected', description="Multiple sequential 'await' calls identified. This increases total latency linearly.", impact='MEDIUM', roi='Reduces latency by up to 50% using asyncio.gather().', line_number=node.lineno, file_path=file_path))
            if isinstance(node, ast.Call):
                func_name = ''
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                if any((x in func_name.lower() for x in ['get', 'post', 'request', 'fetch', 'query'])):
                    parent = self._get_parent_function(tree, node)
                    if parent and (not self._is_decorated_with_retry(parent)):
                        findings.append(AuditFinding(category='🧗 Reliability', title='Missing Resiliency Logic', description=f"External call '{func_name}' is not protected by retry logic.", impact='HIGH', roi='Increases up-time and handles transient network failures.', line_number=node.lineno, file_path=file_path))
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                if isinstance(node.value, (ast.Constant, ast.JoinedStr)):
                    val = ''
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        val = node.value.value
                    elif isinstance(node.value, ast.JoinedStr):
                        val = ''.join([s.value for s in node.value.values if isinstance(s, ast.Constant)])
                    if len(val) > 20 and any((x in val.lower() for x in ['act as', 'you are', 'instruction'])):
                        if not any((x in val.lower() for x in ["don't know", 'unsure', 'refuse', 'do not make up'])):
                            findings.append(AuditFinding(category='🧗 Reliability', title='High Hallucination Risk', description="System prompt lacks negative constraints (e.g., 'If you don't know, say I don't know').", impact='HIGH', roi='Reduces autonomous failures by enforcing refusal boundaries.', line_number=node.lineno, file_path=file_path))
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