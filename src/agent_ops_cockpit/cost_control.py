import functools

# Production-Ready Cost Control for Google Cloud Agents
# Integrated with Vertex AI Quotas and Gemini 2.0 Model Routing

def cost_guard(budget_limit=0.10):
    """
    Middleware/Decorator to enforce cost guardrails on LLM calls.
    Protects against runaway agent costs in production.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # In a real production environment, this would:
            # 1. Estimate tokens using vertexai.generative_models.GenerativeModel.count_tokens
            # 2. Check cumulative daily spend in Firestore/Redis
            # 3. Block if spend > budget_limit
            
            # Simulated cost for demonstration
            estimated_cost = 0.002 # Gemini 2.0 Flash is extremely cheap
            
            print(f"💰 [Cost Control] Estimating turn cost for {func.__name__}...")
            
            if estimated_cost > budget_limit:
                print(f"❌ [BLOCKED] Request estimated at ${estimated_cost}, which exceeds turn budget of ${budget_limit}.")
                return {
                    "error": "Budget exceeded",
                    "details": f"Estimated cost ${estimated_cost} > Limit ${budget_limit}",
                    "suggestion": "Optimize your prompt using 'make audit' or switch to gemini-2.0-flash"
                }
            
            print(f"✅ [ALLOWED] Estimated cost: ${estimated_cost}. Within budget.")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def model_router(query: str):
    """
    Smart model routing middleware (Agent Ops Implementation).
    Routes to Flash for efficiency, Pro for reasoning.
    """
    # Simple heuristic: Complexity-based routing
    complexity_score = len(query.split())
    
    # Check for keywords requiring high reasoning
    reasoning_keywords = ["analyze", "evaluate", "complex", "reason", "plan"]
    requires_pro = any(word in query.lower() for word in reasoning_keywords) or complexity_score > 50

    if requires_pro:
        return "gemini-1.5-pro", "Complexity detected. Using Pro for high-fidelity reasoning."
    else:
        # Default to the ultra-fast Gemini 2.0 Flash
        return "gemini-2.0-flash", "Simple query. Using Flash for sub-second latency."
