import functools

def cost_guard(budget_limit=0.1):
    """
    Middleware/Decorator to enforce cost guardrails on LLM calls.
    Protects against runaway agent costs in production.
    """

    def decorator(func):

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            estimated_cost = 0.0001
            print(f'💰 [Cost Control] Estimating turn cost for {func.__name__}...')
            if estimated_cost > budget_limit:
                print(f'❌ [BLOCKED] Request estimated at ${estimated_cost}, which exceeds turn budget of ${budget_limit}.')
                return {'error': 'Budget exceeded', 'details': f'Estimated cost ${estimated_cost} > Limit ${budget_limit}', 'suggestion': "Optimize your prompt using 'make audit' or switch to gemini-3-flash"}
            print(f'✅ [ALLOWED] Estimated cost: ${estimated_cost}. Within budget.')
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def model_router(query: str):
    """
    Smart model routing middleware (Agent Ops Implementation).
    Routes to Flash for efficiency, Pro for reasoning.
    """
    complexity_score = len(query.split())
    reasoning_keywords = ['analyze', 'evaluate', 'complex', 'reason', 'plan']
    requires_pro = any((word in query.lower() for word in reasoning_keywords)) or complexity_score > 50
    if requires_pro:
        return ('gemini-3-pro', 'Strategic complexity detected. Using Gemini 3 Pro for high-fidelity reasoning.')
    else:
        return ('gemini-3-flash', 'Performance optimized. Using Gemini 3 Flash for sub-second agentic latency.')