import time
from typing import Dict, Any, List

class MemoryOptimizer:
    """
    Optimizes agent memory usage by implementing eviction policies and size limits.
    Helps prevent 'Large System Instruction' bloat over long conversations.
    """
    
    def __init__(self, max_items: int = 50, ttl_seconds: int = 3600):
        self.max_items = max_items
        self.ttl_seconds = ttl_seconds
        self.memory: Dict[str, Dict[str, Any]] = {}

    def add_event(self, event_id: str, data: Any):
        """Adds an event to memory with a timestamp."""
        # Eviction logic: If full, remove oldest
        if len(self.memory) >= self.max_items:
            oldest_key = min(self.memory.keys(), key=lambda k: self.memory[k]['timestamp'])
            del self.memory[oldest_key]
            
        self.memory[event_id] = {
            "data": data,
            "timestamp": time.time()
        }

    def get_optimized_context(self) -> List[Any]:
        """Returns memory filtered by TTL and sorted by recency."""
        current_time = time.time()
        valid_items = [
            item['data'] for item in self.memory.values()
            if (current_time - item['timestamp']) < self.ttl_seconds
        ]
        return valid_items

    def compress_summaries(self, items: List[str]) -> str:
        """
        Placeholder for LLM-based summarization to compress memory.
        In a real scenario, this would call a Flash model to summarize history.
        """
        return f"Summary of {len(items)} items..."

# Global Instance for the Cockpit
agent_memory_manager = MemoryOptimizer(max_items=20, ttl_seconds=1800)
