try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.4.5 Sovereign Alignment: Optimized for AWS App Runner (Bedrock)
from tenacity import retry, wait_exponential, stop_after_attempt
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
    DEFAULT_EXCLUSIONS = {'.git', 'node_modules', 'venv', '.venv', '.build_venv', '.pyenv', '__pycache__', 'dist', 'build', '.pytest_cache', '.mypy_cache', 'cockpit_artifacts', 'cockpit_final_report_*.md', 'cockpit_report.html', 'evidence_lake', 'evidence_lake.json', 'cockpit_audit.sarif', 'fleet_dashboard.html', '.agent', '.cockpit', '.gcloud', '.firebase'}

    def __init__(self, root_path: str='.'):
        self.root_path = os.path.abspath(root_path)
        self.ignore_patterns = self._load_gitignore()
        self.cockpit_ignore = self._load_cockpitignore()
        self.config = self._load_config()

    def _load_gitignore(self) -> List[str]:
        patterns = []
        gitignore_path = os.path.join(self.root_path, '.gitignore')
        if os.path.exists(gitignore_path):
            try:
                with open(gitignore_path, 'r', errors='ignore') as f:
                    for line in f:
                        line = line.strip()
                        if line and (not line.startswith('#')):
                            if line.endswith('/'):
                                patterns.append(line + '*')
                            patterns.append(line)
            except Exception:
                pass
        return patterns

    def _load_cockpitignore(self) -> List[str]:
        patterns = []
        ignore_path = os.path.join(self.root_path, '.cockpitignore')
        if os.path.exists(ignore_path):
            try:
                with open(ignore_path, 'r', errors='ignore') as f:
                    for line in f:
                        line = line.strip()
                        if line and (not line.startswith('#')):
                            if line.endswith('/'):
                                patterns.append(line + '*')
                            patterns.append(line)
            except Exception:
                pass
        return patterns

    def _load_config(self) -> dict:
        """
        Simple YAML-lite parser for cockpit.yaml to avoid external dependencies.
        """
        config = {}
        config_path = os.path.join(self.root_path, 'cockpit.yaml')
        if not os.path.exists(config_path):
            return config
        try:
            with open(config_path, 'r', errors='ignore') as f:
                content = f.read()
                entry_match = re.search('entry_point:\\s*[\'\\"]?(.+?)[\'\\"]?\\s*$', content, re.MULTILINE)
                if entry_match:
                    config['entry_point'] = entry_match.group(1).strip()
                threshold_match = re.search('threshold:\\s*(\\d+)', content)
                if threshold_match:
                    config['threshold'] = int(threshold_match.group(1))

                def parse_list(key, text):
                    inline = re.search(f'{key}:\\s*\\[(.*?)\\]', text, re.DOTALL)
                    if inline:
                        items = inline.group(1).split(',')
                        return [i.strip().strip('\'"') for i in items if i.strip()]
                    multi = re.search(f'{key}:\\s*\\n((?:\\s*-\\s*.+\\n?)+)', text)
                    if multi:
                        items = re.findall('^\\s*-\\s*(.+)$', multi.group(1), re.MULTILINE)
                        return [i.strip().strip('\'"') for i in items]
                    return []
                config['exclude'] = parse_list('exclude', content)
                config['targets'] = parse_list('targets', content)
        except Exception:
            pass
        return config

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    def should_ignore(self, path: str) -> bool:
        """
        Determines if a path should be ignored based on defaults, .gitignore, and config.
        """
        path_abs = os.path.abspath(path)
        rel_path = os.path.relpath(path_abs, self.root_path)
        if rel_path == '.':
            return False
        parts = rel_path.split(os.sep)
        for part in parts:
            if part in self.DEFAULT_EXCLUSIONS:
                return True
            for pattern in self.DEFAULT_EXCLUSIONS:
                if fnmatch.fnmatch(part, pattern):
                    return True
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                return True
            if pattern.endswith('/*') and rel_path.startswith(pattern[:-2]):
                return True
        for pattern in self.cockpit_ignore:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                return True
            if pattern.endswith('/*') and rel_path.startswith(pattern[:-2]):
                return True
        user_excludes = self.config.get('exclude', [])
        for pattern in user_excludes:
            if fnmatch.fnmatch(rel_path, pattern):
                return True
            if pattern.endswith('/*') and rel_path.startswith(pattern[:-1]):
                return True
            if pattern.endswith('/') and rel_path.startswith(pattern):
                return True
            if rel_path.startswith(pattern + os.sep):
                return True
        if '{{' in rel_path and '}}' in rel_path:
            return True
        return False

    def walk(self, start_path: Optional[str]=None) -> Generator[str, None, None]:
        """
        Yields file paths while respecting all ignore rules.
        """
        base_search = os.path.abspath(start_path or self.root_path)
        for root, dirs, files in os.walk(base_search):
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
        library_indicators = {'venv', '.venv', 'site-packages', 'node_modules', 'dist', 'build'}
        return any((part in library_indicators for part in parts))

    def find_agent_brain(self) -> str:
        """
        Identifies the core agent file using config, heuristics, and AST analysis.
        v1.4: Supports multi-target discovery and template placeholder awareness.
        """
        if 'targets' in self.config and self.config['targets']:
            candidate = os.path.join(self.root_path, self.config['targets'][0])
            if os.path.exists(candidate):
                return candidate
        if 'entry_point' in self.config:
            candidate = os.path.join(self.root_path, self.config['entry_point'])
            if os.path.exists(candidate):
                return candidate
        priorities = ['src/agent_ops_cockpit/agent.py', 'agent.py', 'agent/agent.py', 'main.py', '__main__.py', 'app.py', 'index.ts', 'index.js', 'main.ts', 'main.js', 'main.go', 'src/agent.py']
        for p in priorities:
            path = os.path.join(self.root_path, p)
            if os.path.exists(path):
                return path
        best_candidate = None
        for file_path in self.walk():
            if not file_path.endswith('.py'):
                continue
            if 'agent_ops_cockpit/ops' in file_path:
                continue
            try:
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read()
                    tree = ast.parse(content)
                    weight = 0
                    if 'vertexai' in content:
                        weight += 10
                    if 'langchain' in content:
                        weight += 5
                    if 'agent_ops_cockpit' in content:
                        weight += 20
                    if 'Agent' in content or 'agent =' in content:
                        weight += 2
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.Import, ast.ImportFrom)):
                            modules = []
                            if isinstance(node, ast.Import):
                                modules = [alias.name for alias in node.names]
                            elif node.module:
                                modules = [node.module]
                            if any((m and ('vertexai' in m or 'langchain' in m or 'google.cloud' in m or ('agent_ops_cockpit' in m)) for m in modules)):
                                weight += 15
                    if weight > 30:
                        return file_path
                    if weight > 0:
                        if not best_candidate or weight > best_candidate[1]:
                            best_candidate = (file_path, weight)
            except Exception:
                continue
        if best_candidate:
            return best_candidate[0]
        return os.path.join(self.root_path, 'agent.py')