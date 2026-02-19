import os
import json

class DogFoodOrchestrator:
    """
    Orchestrates the 10-iteration hardening of the 15+ industry repos.
    Goal: Evolve Cockpit by identifying cross-ecosystem debt.
    """
    def __init__(self, dogfood_path):
        self.dogfood_path = dogfood_path
        self.repos = [d for d in os.listdir(dogfood_path) if os.path.isdir(os.path.join(dogfood_path, d))]
    
    def run_pre_flight_analysis(self):
        """Analyze the DNA of our dogfood fleet."""
        stats = {
            "total_repos": len(self.repos),
            "by_language": {"python": 0, "typescript": 0, "dotnet": 0, "other": 0},
            "by_provider": {"google": 0, "openai": 0, "anthropic": 0, "microsoft": 0, "aws": 0}
        }
        
        for repo in self.repos:
            repo_path = os.path.join(self.dogfood_path, repo)
            # Detect Language
            files = [f for f in os.listdir(repo_path) if os.path.isfile(os.path.join(repo_path, f))]
            if any(f.endswith(".py") for f in files) or os.path.exists(os.path.join(repo_path, "requirements.txt")):
                stats["by_language"]["python"] += 1
            if any(f.endswith(".ts") or f.endswith(".tsx") for f in files) or os.path.exists(os.path.join(repo_path, "package.json")):
                stats["by_language"]["typescript"] += 1
            if any(f.endswith(".cs") or f.endswith(".csproj") for f in files):
                stats["by_language"]["dotnet"] += 1
                
            # Detect Provider Intent
            low_repo = repo.lower()
            if "google" in low_repo or "adk" in low_repo:
                stats["by_provider"]["google"] += 1
            elif "openai" in low_repo:
                stats["by_provider"]["openai"] += 1
            elif "claude" in low_repo or "anthropic" in low_repo or "skills" in low_repo:
                stats["by_provider"]["anthropic"] += 1
            elif "microsoft" in low_repo or "agent365" in low_repo or "dotnet" in low_repo:
                stats["by_provider"]["microsoft"] += 1
            elif "aws" in low_repo or "bedrock" in low_repo or "amazon" in low_repo:
                stats["by_provider"]["aws"] += 1
            
        return stats

if __name__ == "__main__":
    orch = DogFoodOrchestrator("/Users/enriq/Documents/git/agent-cockpit/dogfood")
    results = orch.run_pre_flight_analysis()
    print(json.dumps(results, indent=2))
