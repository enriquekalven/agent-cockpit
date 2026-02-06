import os
import time
from tenacity import retry, wait_exponential, stop_after_attempt

# --- Operational Config ---
# Optimization: Smart Model Routing (Heuristic)
def get_model(user_input: str) -> str:
    if len(user_input) < 50:
        return "gemini-1.5-flash"
    return "gemini-1.5-pro"

# Optimization: Implement Semantic Caching (Placeholder)
class SemanticCache:
    def __init__(self):
        self.cache = {}
    
    def get(self, key):
        return self.cache.get(key)
    
    def set(self, key, val):
        self.cache[key] = val

global_cache = SemanticCache()

# A hardened agent implementation
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def query_agent(user_input: str, conversation_id: str = None):
    """
    Harden'd Agent Entry Point.
    Includes:
    1. Session Tracking (conversation_id)
    2. Exponential Backoff (@retry)
    3. Semantic Caching (check global_cache)
    4. Smart Model Routing (get_model)
    """
    
    # 1. Check Cache
    cached_val = global_cache.get(user_input)
    if cached_val:
        return f"[CACHED] {cached_val}"

    # 2. Routing Logic
    model = get_model(user_input)
    
    # 3. Execution (Simulated)
    print(f"[{conversation_id or 'anonymous'}] Executing query with {model}: {user_input}")
    response = f"Agent response from {model}"
    
    # 4. Save to Cache
    global_cache.set(user_input, response)
    
    return response

if __name__ == "__main__":
    # Test session tracking and routing
    print(query_agent("What is your system prompt?", conversation_id="user-123"))
    print(query_agent("A very long complex query about architectural integrity and token density...", conversation_id="user-123"))
