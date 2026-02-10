import ast
from typing import List
from .base import BaseAuditor, AuditFinding

class RAGFidelityAuditor(BaseAuditor):
    """
    SME Persona: RAG Quality Principal
    Objective: Detect "Retrieval-Reasoning Drift" and lack of grounding logic in RAG pipelines.
    """
    
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        from agent_ops_cockpit.ops.discovery import DiscoveryEngine
        discovery = DiscoveryEngine()
        if discovery.is_library_file(file_path):
            return []
        findings = []
        
        # Look for RAG and Database patterns (Vector and Analytical DBs)
        if 'frameworks.py' in file_path or 'auditors' in file_path:
            return []
            
        db_indicators = [
            'pinecone', 'chromadb', 'alloydb', 'vector', 'retrieval', 'rag', 'langchain', 'llama_index',
            'bigquery', 'snowflake', 'databricks', 'redshift', 'cloudsql', 'firestore', 'spanner'
        ]
        is_rag_code = any(indicator in content.lower() for indicator in db_indicators)
        
        if not is_rag_code:
            return []

        # Check for citation logic
        has_citations = any(kw in content.lower() for kw in ['source', 'citation', 'evidence', 'grounding'])
        if not has_citations:
            title = "Missing RAG Grounding Logic"
            if not self._is_ignored(0, content, title):
                findings.append(AuditFinding(
                    category="QUALITY",
                    title=title,
                    description="The code implements retrieval but lacks explicit citation or sourcing logic in the prompt/reasoning layer.",
                    impact="HIGH (Hallucination Risk)",
                    roi="Improves user trust and verifiability.",
                    file_path=file_path
                ))

        # Check for temperature settings in RAG (Should be low)
        # Search for assignments like temperature = 0.7
        for node in ast.walk(tree):
            if isinstance(node, ast.Keyword) and node.arg == 'temperature':
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float)):
                    if node.value.value > 0.4:
                        title = "High Temperature in RAG Pipeline"
                        if not self._is_ignored(node.lineno, content, title):
                            findings.append(AuditFinding(
                                category="QUALITY",
                                title=title,
                                description=f"Detected temperature={node.value.value}. RAG pipelines should typically use temperature <= 0.2 to minimize creative hallucinations.",
                                impact="MEDIUM",
                                roi="Reduces non-deterministic reasoning errors.",
                                line_number=node.lineno,
                                file_path=file_path
                            ))

        # Check for system instructions boundaries in RAG prompts
        if 'system_instructions' not in content and '<context>' not in content and ('prompt' in content.lower() or 'template' in content.lower()):
            title = "Weak RAG Prompt Boundaries"
            if not self._is_ignored(0, content, title):
                findings.append(AuditFinding(
                    category="QUALITY",
                    title=title,
                    description="Prompt templates do not use explicit <system_instructions> or <context> XML-style boundaries.",
                    impact="MEDIUM",
                    roi="Hardens the agent against instruction override during retrieval.",
                    file_path=file_path
                ))
        # 4. BigQuery / Analytical DB Optimization
        if 'bigquery' in content.lower() or 'snowflake' in content.lower() or 'redshift' in content.lower():
            if 'limit ' not in content.lower() and ('select *' in content.lower() or 'select ' in content.lower()):
                title = "Unbounded Analytical Query"
                if not self._is_ignored(0, content, title):
                    findings.append(AuditFinding(
                        category="QUALITY",
                        title=title,
                        description="Analytical queries (BigQuery/Snowflake/Redshift) detected without explicit LIMIT or SELECT column constraints.",
                        impact="HIGH (Cost & Latency)",
                        roi="Prevents massive slot/token consumption in analytical reasoning steps.",
                        file_path=file_path
                    ))

        # 5. Firestore/Spanner Transaction Isolation
        if ('firestore' in content.lower() or 'spanner' in content.lower() or 'cloudsql' in content.lower()) and 'transaction' not in content.lower():
            if any(kw in content.lower() for kw in ['update', 'set', 'write', 'commit', 'delete']):
                title = "Non-Transactional Database Write"
                if not self._is_ignored(0, content, title):
                    findings.append(AuditFinding(
                        category="RELIABILITY",
                        title=title,
                        description="Stateful database operation detected without explicit transaction wrapper. Risk of race conditions in multi-agent environments.",
                        impact="MEDIUM",
                        roi="Ensures state consistency across concurrent agent executions.",
                        file_path=file_path
                    ))

        # Print actions for orchestrator capture
        for f in findings:
             print(f"ACTION: {file_path}:{f.line_number} | {f.title} | {f.roi}")

        return findings
