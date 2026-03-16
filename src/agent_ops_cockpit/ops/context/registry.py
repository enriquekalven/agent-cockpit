import json
import os
import re
from typing import Any, Dict, List


class ContextRegistry:
    """
    Manages the indexing of Cockpit knowledge files (public/*.md, docs/*.md).
    """
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        self.registry_path = os.path.join(workspace_path, '.cockpit', 'context_registry.json')

    def parse_metadata_table(self, content: str) -> Dict[str, Any]:
        """
        Extracts metadata from the Mandated Table format:
        | name | description | category | revision | tags |
        """
        # Look for the table pattern
        table_pattern = r'\| name \| description \| category \| revision \| tags \|\n\| :--- \| :--- \| :--- \| :--- \| :--- \|\n\| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|'
        match = re.search(table_pattern, content)
        if match:
            return {
                "name": match.group(1).strip(),
                "description": match.group(2).strip(),
                "category": match.group(3).strip(),
                "revision": int(match.group(4).strip()),
                "tags": [t.strip() for t in match.group(5).split(',')]
            }
        return {}

    def build_registry(self) -> List[Dict[str, Any]]:
        docs = []
        search_dirs = [
            os.path.join(self.workspace_path, 'public'),
            os.path.join(self.workspace_path, 'docs')
        ]
        
        for sdir in search_dirs:
            if not os.path.exists(sdir):
                continue
                
            for root, _, files in os.walk(sdir):
                for file in files:
                    if file.endswith('.md'):
                        fpath = os.path.join(root, file)
                        with open(fpath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        metadata = self.parse_metadata_table(content)
                        if metadata:
                            entry = {
                                **metadata,
                                "path": os.path.relpath(fpath, self.workspace_path),
                                "content": content[:2000] # Cap content for index
                            }
                            docs.append(entry)
        
        # Save registry
        os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(docs, f, indent=4)
            
        return docs

    def load_registry(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
