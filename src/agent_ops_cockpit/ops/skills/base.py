import abc
from typing import Dict, List

from pydantic import BaseModel


class SkillMetadata(BaseModel):
    name: str
    description: str
    category: str
    revision: int = 1
    tags: List[str] = []
    critical_score: float = 0.5  # Default weight for BM25
    rationalizations: List[Dict[str, str]] = []
    verification_gates: List[str] = []

class GovernanceSkill(abc.ABC):
    """
    A Governance Skill is a fusion of Andrew Ng's 'Skill' concept and Cockpit 'Auditors'.
    It contains both the readable guideline for the LLM and the executable logic for verification.
    Extended to map Addy Osmani's 'Anti-Rationalization' and 'Verification' workflows.
    """
    
    def __init__(self, metadata: SkillMetadata):
        self.metadata = metadata

    @abc.abstractmethod
    async def verify(self, context: Dict) -> Dict:
        """
        Execute the verification logic.
        Returns a result dict with 'status', 'score', and 'findings'.
        """
        pass

    @classmethod
    def parse_skill_md(cls, content: str, filename: str = "unknown") -> SkillMetadata:
        """
        Parses a SKILL.md format file containing Process, Rationalizations, and Verification.
        """
        lines = content.splitlines()
        name = filename.replace(".md", "").replace("SKILL", "custom-skill")
        description = "Imported custom skill"
        category = "agent-skills"
        rationalizations = []
        verification_gates = []
        
        current_section = None
        for line in lines:
            lower = line.lower().strip()
            if lower.startswith("## rationalizations") or lower.startswith("### rationalizations"):
                current_section = "rationalizations"
            elif lower.startswith("## verification") or lower.startswith("### verification"):
                current_section = "verification"
            elif lower.startswith("## ") or lower.startswith("### "):
                current_section = "other"
                
            if current_section == "rationalizations" and "|" in line and "Rationalization" not in line:
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 2:
                    rationalizations.append({"excuse": parts[0], "rebuttal": parts[1]})
                    
            elif current_section == "verification" and line.startswith("- "):
                verification_gates.append(line.replace("- ", "").strip())
                
        return SkillMetadata(
            name=name,
            description=description,
            category=category,
            rationalizations=rationalizations,
            verification_gates=verification_gates
        )

    def to_markdown(self) -> str:
        """
        Generates the Context Hub compatible markdown representation.
        """
        table = "| name | description | category | revision | tags |\n"
        table += "| :--- | :--- | :--- | :--- | :--- |\n"
        table += f"| {self.metadata.name} | {self.metadata.description} | {self.metadata.category} | {self.metadata.revision} | {','.join(self.metadata.tags)} |\n"
        
        md = f"{table}\n\n# {self.metadata.name} Guideline\n\n(Logic-backed skill)"
        if self.metadata.rationalizations:
            md += "\n\n## Anti-Rationalization Rebuttals\n"
            for r in self.metadata.rationalizations:
                md += f"- **Excuse**: {r['excuse']}\n  - **Rebuttal**: {r['rebuttal']}\n"
        if self.metadata.verification_gates:
            md += "\n\n## Verification Requirements\n"
            for gate in self.metadata.verification_gates:
                md += f"- {gate}\n"
                
        return md
