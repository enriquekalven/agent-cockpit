try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError):
    ContextCacheConfig = None
# v1.6.7 Sovereign Alignment: Optimized for AWS App Runner (Bedrock)
from agent_ops_cockpit.telemetry import telemetry
telemetry.track_event_sync("package_import")
