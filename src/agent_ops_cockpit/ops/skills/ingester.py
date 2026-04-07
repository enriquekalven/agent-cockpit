import json
import os
from typing import Dict, List
from agent_ops_cockpit.ops.skills.base import GovernanceSkill, SkillMetadata

class ContextIngester:
    """
    Parses standard Addy Osmani SKILL.md files and serializes their constraints
    into Cockpit's internal watchlist.json and policies.json.
    """
    
    def __init__(self, cockpit_dir: str):
        self.cockpit_dir = os.path.abspath(cockpit_dir)
        self.ops_dir = os.path.join(self.cockpit_dir, "src", "agent_ops_cockpit", "ops")
        self.watchlist_path = os.path.join(self.ops_dir, "watchlist.json")
        self.policies_path = os.path.join(self.ops_dir, "policies.json")

    def ingest_skill(self, content: str, name: str) -> SkillMetadata:
        """
        Takes a SKILL.md file, parses verification/rationalizations,
        and injects them into the BM25 Context Store files.
        """
        metadata = GovernanceSkill.parse_skill_md(content, filename=name)
        
        # 1. Write behavioral policies to policies.json
        if os.path.exists(self.policies_path):
            with open(self.policies_path, "r") as f:
                try:
                    policies = json.load(f)
                except Exception:
                    policies = {}
        else:
            policies = {}
            
        new_rules = []
        for rat in metadata.rationalizations:
            new_rules.append(f"Fight excuse: '{rat['excuse']}' -> {rat['rebuttal']}")
        for gate in metadata.verification_gates:
            new_rules.append(f"Require verification: {gate}")
            
        policies[metadata.name] = {
            "description": metadata.description,
            "rules": new_rules
        }
        
        with open(self.policies_path, "w") as f:
            json.dump(policies, f, indent=2)

        # 2. Write to Watchlist index
        if os.path.exists(self.watchlist_path):
            with open(self.watchlist_path, "r") as f:
                try:
                    watchlist = json.load(f)
                except Exception:
                    watchlist = {}
        else:
            watchlist = {}
            
        watchlist[f"skill:{metadata.name}"] = {
            "category": "agent-skills-behavioral",
            "constraints": new_rules
        }
        
        with open(self.watchlist_path, "w") as f:
            json.dump(watchlist, f, indent=2)
            
        return metadata

