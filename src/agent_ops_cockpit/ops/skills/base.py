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

class GovernanceSkill(abc.ABC):
    """
    A Governance Skill is a fusion of Andrew Ng's 'Skill' concept and Cockpit 'Auditors'.
    It contains both the readable guideline for the LLM and the executable logic for verification.
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

    def to_markdown(self) -> str:
        """
        Generates the Context Hub compatible markdown representation.
        """
        table = "| name | description | category | revision | tags |\n"
        table += "| :--- | :--- | :--- | :--- | :--- |\n"
        table += f"| {self.metadata.name} | {self.metadata.description} | {self.metadata.category} | {self.metadata.revision} | {','.join(self.metadata.tags)} |\n"
        
        return f"{table}\n\n# {self.metadata.name} Guideline\n\n(Logic-backed skill)"
