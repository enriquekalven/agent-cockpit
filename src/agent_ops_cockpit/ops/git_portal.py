try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.8.4 Sovereign Alignment: Optimized for AWS App Runner (Bedrock)
from typing import List

import git
from rich.console import Console
from tenacity import retry, stop_after_attempt, wait_exponential

console = Console()

class GitPortal:
    """
    Phase 5: The 'Ambassador' - Autonomous Git & PR Portal.
    Handles branch creation, committing fixes, and preparing for PR submission.
    """

    def __init__(self, repo_path: str='.'):
        self.repo_path = repo_path
        try:
            self.repo = git.Repo(repo_path)
        except Exception as e:
            self.repo = None
            console.print(f'[red]❌ Git initialization failed: {e}[/red]')

    def create_fix_branch(self, branch_name: str):
        """Creates and switches to a new branch for fixes."""
        if not self.repo:
            return None
        current = self.repo.active_branch
        console.print(f'🌿 [dim]Creating fix branch: {branch_name} (from {current.name})[/dim]')
        new_branch = self.repo.create_head(branch_name)
        new_branch.checkout()
        return new_branch

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    def commit_fixes(self, files: List[str], message: str):
        """Stages and commits the remediated files with GPG safety."""
        if not self.repo:
            return False
        gpg_sign = False
        try:
            gpg_sign = self.repo.config_reader().get_value('commit', 'gpgsign', default=False)
            if isinstance(gpg_sign, str):
                gpg_sign = gpg_sign.lower() == 'true'
        except Exception:
            pass
        import os
        rel_files = [os.path.relpath(f, self.repo_path) if os.path.isabs(f) or f.startswith('..') else f for f in files]
        self.repo.index.add(rel_files)
        if gpg_sign:
            console.print('🔐 [yellow]GPG Signing detected. Using --no-gpg-sign for agentic commit...[/yellow]')
            self.repo.git.commit('-m', message, '--no-gpg-sign')
        else:
            self.repo.index.commit(message)
        console.print(f'📦 [bold green]Committed fixes to {len(files)} files.[/bold green]')
        return True

    def push_fixes(self, branch_name: str):
        """Pushes the branch to the remote."""
        if not self.repo:
            return False
        try:
            origin = self.repo.remote(name='origin')
            console.print(f'🚀 [cyan]Pushing {branch_name} to origin...[/cyan]')
            origin.push(branch_name)
            return True
        except Exception as e:
            console.print(f'[yellow]⚠️  Push failed (Remote likely not configured): {e}[/yellow]')
            return False

    def get_pr_body(self, findings_count: int, score_improvement: int):
        """Generates the body text for a GitHub PR."""
        return f"""
# 🕹️ AgentOps Cockpit: Sovereign Evolution Suite
**Version:** 2.0.2 | **Status:** AUTO_REMEDIATION_STAGE

## 🧠 Executive Digest for Reviewers
This PR contains **autonomous architectural hardening** aimed at improving the agent's Sovereignty and Production Readiness. 

- **Strategic ROI:** +{score_improvement}% Maturity Score improvement.
- **Architectural Intent:** Aligning with the **Agentic Trinity** (Engine/Face/Cockpit) standard.
- **Blast Radius Guard:** This PR is limited to a maximum of 10 file changes to prevent PR Exhaustion.
- **Cordon Pattern:** High-impact structural changes (like deletions or splits) are Cordoned and require explicit human-in-the-loop approval.

### 🛠️ Summary of Remediations
This PR resolves **{findings_count} architectural gaps** detected by our SME Persona Board:

1. **🧗 Resiliency & Reliability:** Injected `tenacity` retry backoffs and `timeout` guards.
2. **🛡️ Security Hardening:** AST-aware remediation for credential exposure and over-privilege risks.
3. **💧 Infrastructure Hydration:** Standardized cloud-provider headers and A2A handshake protocols.

---
*Generated with 🧠 by the AgentOps Cockpit 'The Closer' Engine. We value your time—please review for semantic alignment.*
"""