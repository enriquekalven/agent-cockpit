import os
import fnmatch
import ast
import re
from typing import List, Optional, Generator

class DiscoveryEngine:
    """
    Centralized discovery engine for AgentOps Cockpit.
    Respects .gitignore, handles default exclusions, and identifies the agentic 'brain'.
    """
    DEFAULT_EXCLUSIONS = {
        ".git", "node_modules", "venv", ".venv", "__pycache__", 
        "dist", "build", ".pytest_cache", ".mypy_cache", 
        "cockpit_artifacts", "cockpit_final_report_*.md", "cockpit_report.html",
        "evidence_lake", "evidence_lake.json", "cockpit_audit.sarif", "fleet_dashboard.html",
        ".agent"
    }

    def __init__(self, root_path: str = "."):
        self.root_path = os.path.abspath(root_path)
        self.ignore_patterns = self._load_gitignore()
        self.cockpit_ignore = self._load_cockpitignore()
        self.config = self._load_config()

    def _load_gitignore(self) -> List[str]:
        patterns = []
        gitignore_path = os.path.join(self.root_path, ".gitignore")
        if os.path.exists(gitignore_path):
            try:
                with open(gitignore_path, "r", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            if line.endswith("/"):
                                patterns.append(line + "*")
                            patterns.append(line)
            except Exception:
                pass
        return patterns

    def _load_cockpitignore(self) -> List[str]:
        # Improvement #3: .cockpitignore Support
        patterns = []
        ignore_path = os.path.join(self.root_path, ".cockpitignore")
        if os.path.exists(ignore_path):
            try:
                with open(ignore_path, "r", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            if line.endswith("/"):
                                patterns.append(line + "*")
                            patterns.append(line)
            except Exception:
                pass
        return patterns

    def _load_config(self) -> dict:
        """
        Simple YAML-lite parser for cockpit.yaml to avoid external dependencies.
        """
        config = {}
        config_path = os.path.join(self.root_path, "cockpit.yaml")
        if not os.path.exists(config_path):
            return config

        try:
            with open(config_path, "r", errors="ignore") as f:
                content = f.read()
                # Parse entry_point
                entry_match = re.search(r"entry_point:\s*['\"]?(.+?)['\"]?\s*$", content, re.MULTILINE)
                if entry_match:
                    config["entry_point"] = entry_match.group(1).strip()
                
                # Parse threshold
                threshold_match = re.search(r"threshold:\s*(\d+)", content)
                if threshold_match:
                    config["threshold"] = int(threshold_match.group(1))

                # Parse exclude list
                exclude_block = re.search(r"exclude:\s*\[(.*?)\]", content, re.DOTALL)
                if exclude_block:
                    items = exclude_block.group(1).split(",")
                    config["exclude"] = [i.strip().strip("'\"") for i in items if i.strip()]
                else:
                    # Handle multi-line list
                    exclude_block = re.search(r"exclude:\s*\n((?:\s*-\s*.+\n?)+)", content)
                    if exclude_block:
                        items = re.findall(r"^\s*-\s*(.+)$", exclude_block.group(1), re.MULTILINE)
                        config["exclude"] = [i.strip().strip("'\"") for i in items]
        except Exception:
            pass
        return config

    def should_ignore(self, path: str) -> bool:
        """
        Determines if a path should be ignored based on defaults, .gitignore, and config.
        """
        path_abs = os.path.abspath(path)
        rel_path = os.path.relpath(path_abs, self.root_path)
        
        if rel_path == ".":
            return False
        
        parts = rel_path.split(os.sep)
        
        # 1. Check default exclusions
        for part in parts:
            if part in self.DEFAULT_EXCLUSIONS:
                return True
            for pattern in self.DEFAULT_EXCLUSIONS:
                if fnmatch.fnmatch(part, pattern):
                    return True

        # 2. Check .gitignore patterns
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                return True
            # Handle directory patterns
            if pattern.endswith("/*") and rel_path.startswith(pattern[:-2]):
                return True

        # 2.1 Check .cockpitignore patterns (Improvement #3)
        for pattern in self.cockpit_ignore:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                return True
            if pattern.endswith("/*") and rel_path.startswith(pattern[:-2]):
                return True

        # 3. Check cockpit.yaml exclusions
        user_excludes = self.config.get("exclude", [])
        for pattern in user_excludes:
            if fnmatch.fnmatch(rel_path, pattern):
                return True

        return False

    def walk(self, start_path: Optional[str] = None) -> Generator[str, None, None]:
        """
        Yields file paths while respecting all ignore rules.
        """
        base_search = os.path.abspath(start_path or self.root_path)
        for root, dirs, files in os.walk(base_search):
            # Prune directories in-place to avoid unnecessary traversal
            dirs[:] = [d for d in dirs if not self.should_ignore(os.path.join(root, d))]
            
            for file in files:
                file_path = os.path.join(root, file)
                if not self.should_ignore(file_path):
                    yield file_path

    def is_library_file(self, path: str) -> bool:
        """
        Detects if a file belongs to a third-party library (venv, site-packages, etc.)
        """
        path_abs = os.path.abspath(path)
        rel_path = os.path.relpath(path_abs, self.root_path)
        parts = rel_path.split(os.sep)
        library_indicators = {"venv", ".venv", "site-packages", "node_modules", "dist", "build"}
        return any(part in library_indicators for part in parts)

    def find_agent_brain(self) -> str:
        """
        Identifies the core agent file using config, heuristics, and AST analysis.
        """
        # Phase 1: Explicit Config
        if "entry_point" in self.config:
            candidate = os.path.join(self.root_path, self.config["entry_point"])
            if os.path.exists(candidate):
                return candidate

        # Phase 2: High-Priority Heuristics
        priorities = [
            'src/agent_ops_cockpit/agent.py', 
            'agent.py', 
            'agent/agent.py',
            'main.py', 
            '__main__.py',
            'app.py',
            'index.ts',
            'index.js',
            'main.ts',
            'main.js',
            'main.go',
            'src/agent.py'
        ]
        for p in priorities:
            path = os.path.join(self.root_path, p)
            if os.path.exists(path):
                return path

        # Phase 3: AST Reasoning
        best_candidate = None
        for file_path in self.walk():
            # Only scan python files for brain detection
            if not file_path.endswith(".py"):
                continue
            
            # Avoid scanning the cockpit codebase itself if possible, but keep it as candidate
            if "agent_ops_cockpit/ops" in file_path:
                continue

            try:
                with open(file_path, "r", errors="ignore") as f:
                    content = f.read()
                    tree = ast.parse(content)
                    
                    # Weighting system for brain detection
                    weight = 0
                    if "vertexai" in content:
                        weight += 10
                    if "langchain" in content:
                        weight += 5
                    if "agent_ops_cockpit" in content:
                        weight += 20
                    if "Agent" in content or "agent =" in content:
                        weight += 2
                    
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.Import, ast.ImportFrom)):
                            modules = []
                            if isinstance(node, ast.Import):
                                modules = [alias.name for alias in node.names]
                            else:
                                if node.module:
                                    modules = [node.module]
                            
                            if any(m and ('vertexai' in m or 'langchain' in m or 'google.cloud' in m or 'agent_ops_cockpit' in m) for m in modules):
                                weight += 15
                    
                    if weight > 30: # Very strong confidence
                        return file_path
                    if weight > 0:
                        if not best_candidate or weight > best_candidate[1]:
                            best_candidate = (file_path, weight)
            except Exception:
                continue
        
        if best_candidate:
            return best_candidate[0]
            
        return os.path.join(self.root_path, "agent.py") # Final fallback
