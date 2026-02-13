from tenacity import retry, wait_exponential, stop_after_attempt
try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.4.5 Sovereign Alignment: Optimized for AWS App Runner (Bedrock)
import os

class Config:
    """
    Centralized Configuration for AgentOps Cockpit.
    Improvement #6: Centralized Configuration
    """
    VERSION = "1.6.2"
    DEFAULT_AGENT_PATH = "src/agent_ops_cockpit/agent.py"
    REPO_URL = "https://github.com/enriquekalven/agent-ui-starter-pack"
    
    # Audit Modes
    QUICK_EXTENSIONS = ('.py', '.ts', '.js', '.go', '.json', '.yaml', '.prompt', '.md', 'toml')
    
    # Registry Settings
    PUBLIC_PYPI_URL = "https://pypi.org/simple"
    
    @staticmethod
    def get_python_path():
        cockpit_src = os.path.dirname(os.path.abspath(__file__))
        cockpit_root = os.path.dirname(cockpit_src)
        return f"{cockpit_src}{os.pathsep}{cockpit_root}"

config = Config()
