import ast
from typing import List
from .base import BaseAuditor, AuditFinding

class RAGFidelityAuditor(BaseAuditor):
    """
    SME Persona: RAG Quality Principal
    Objective: Detect "Retrieval-Reasoning Drift" and lack of grounding logic in RAG pipelines.
    """
    
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        
        # Look for RAG patterns (Vector DB calls, RAG frameworks)
        rag_indicators = ['pinecone', 'chromadb', 'alloydb', 'vector', 'retrieval', 'rag', 'langchain', 'llama_index']
        is_rag_code = any(indicator in content.lower() for indicator in rag_indicators)
        
        if not is_rag_code:
            return []

        # Check for citation logic
        has_citations = any(kw in content.lower() for kw in ['source', 'citation', 'evidence', 'grounding'])
        if not has_citations:
            findings.append(AuditFinding(
                category="QUALITY",
                title="Missing RAG Grounding Logic",
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
                        findings.append(AuditFinding(
                            category="QUALITY",
                            title="High Temperature in RAG Pipeline",
                            description=f"Detected temperature={node.value.value}. RAG pipelines should typically use temperature <= 0.2 to minimize creative hallucinations.",
                            impact="MEDIUM",
                            roi="Reduces non-deterministic reasoning errors.",
                            line_number=node.lineno,
                            file_path=file_path
                        ))

        # Check for system instructions boundaries in RAG prompts
        if 'system_instructions' not in content and ('prompt' in content.lower() or 'template' in content.lower()):
            findings.append(AuditFinding(
                category="QUALITY",
                title="Weak RAG Prompt Boundaries",
                description="Prompt templates do not use explicit <system_instructions> or <context> XML-style boundaries.",
                impact="MEDIUM",
                roi="Hardens the agent against instruction override during retrieval.",
                file_path=file_path
            ))

        # Print actions for orchestrator capture
        for f in findings:
             print(f"ACTION: {file_path}:{f.line_number} | {f.title} | {f.roi}")

        return findings
