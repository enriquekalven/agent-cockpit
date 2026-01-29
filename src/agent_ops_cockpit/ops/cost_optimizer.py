import time

class CostOptimizer:
    """
    Tracks token usage and provides cost optimization recommendations in real-time.
    Can be hooked into model call wrappers.
    """
    
    PRICES = {
        "gemini-1.5-pro": {"input": 3.50 / 1_000_000, "output": 10.50 / 1_000_000},
        "gemini-1.5-flash": {"input": 0.075 / 1_000_000, "output": 0.30 / 1_000_000},
    }

    def __init__(self):
        self.usage_history = []

    def log_usage(self, model: str, input_tokens: int, output_tokens: int):
        cost = (input_tokens * self.PRICES.get(model, {}).get("input", 0) +
                output_tokens * self.PRICES.get(model, {}).get("output", 0))
        
        self.usage_history.append({
            "timestamp": time.time(),
            "model": model,
            "input": input_tokens,
            "output": output_tokens,
            "cost": cost
        })

    def get_savings_opportunities(self) -> str:
        pro_usage = sum(1 for log in self.usage_history if log['model'] == 'gemini-1.5-pro')
        total_cost = sum(log['cost'] for log in self.usage_history)
        
        if pro_usage > 0:
            potential_savings = total_cost * 0.9 # Heuristic: Flash is ~10x cheaper
            return f"Found {pro_usage} Pro calls. Swapping to Flash could save ~${potential_savings:.4f}."
        return "Budget is healthy. No immediate savings found."

# Global Instance
cost_tracker = CostOptimizer()
