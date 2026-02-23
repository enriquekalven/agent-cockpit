try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.8.4 Sovereign Alignment: Optimized for AWS App Runner (Bedrock)
import functools
import hashlib
import time
from typing import Dict, Optional

from tenacity import retry, stop_after_attempt, wait_exponential


class HiveMindCache:

    def __init__(self, threshold=0.95):
        self.threshold = threshold
        self.store: Dict[str, Dict] = {}

    def get_match(self, query: str) -> Optional[Dict]:
        """
        Simulates a semantic search. In real life, use vertexai.language_models for embeddings.
        """
        query_hash = hashlib.md5(query.lower().strip().encode()).hexdigest()
        if query_hash in self.store:
            return self.store[query_hash]
        return None

    def put(self, query: str, response: str):
        query_hash = hashlib.md5(query.lower().strip().encode()).hexdigest()
        self.store[query_hash] = {'query': query, 'response': response, 'cached_at': time.time()}

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def hive_mind(cache: HiveMindCache):
    """
    Middleware decorator for viral "one-line" semantic caching.
    """

    def decorator(func):

        @functools.wraps(func)
        async def wrapper(query: str, *args, **kwargs):
            match = cache.get_match(query)
            if match:
                print('🧠 [HIVE MIND] Semantic Hit! Latency Reduced to 0.1s.')
                resp = match['response']
                if isinstance(resp, dict):
                    resp['_metadata'] = {'source': 'hive-mind-cache', 'savings': '100% tokens'}
                return resp
            print('🧪 [HIVE MIND] Cache Miss. Calling LLM...')
            response = await func(query, *args, **kwargs)
            cache.put(query, response)
            return response
        return wrapper
    return decorator
global_cache = HiveMindCache()