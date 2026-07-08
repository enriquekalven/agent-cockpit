# FinOps Skill

| name | description | category | revision | tags |
| :--- | :--- | :--- | :--- | :--- |
| finops-efficiency | Ensures agent uses cost-effective intelligence patterns | finops | 1 | cost,caching,token-density |

## Rationalizations

| Excuse | Rebuttal |
| :--- | :--- |
| I need full context for every turn to maintain accuracy. | Full context is expensive. Use Context Caching for static prompts > 10k tokens. |
| The best model (Pro) is always needed for my tasks. | Use smaller models (Flash) for routing and simple tasks; reserve reasoning models for complex analysis. |

## Verification

- Verify that `ContextCacheConfig` is used for prompts larger than 10k tokens.
- Verify that the agent uses `gemini-2.5-flash` for non-reasoning tasks.
- Run Promptfoo tests to ensure the agent does not produce excessively long responses when a summary is requested.

## Promptfoo Integration

```json
{
  "prompts": ["{{prompt}}"],
  "providers": [
    {
      "id": "python:src/agent_ops_cockpit/eval/promptfoo_provider.py",
      "config": {
        "pythonExecutable": "python3"
      }
    }
  ],
  "tests": [
    {
      "vars": {
        "prompt": "Summarize the history of the internet in 50 words or less."
      },
      "assert": [
        {
          "type": "javascript",
          "value": "output.split(' ').length <= 60",
          "metric": "Token Brevity"
        }
      ]
    }
  ]
}
```

## Evolve Remediation Pattern

When Cockpit detects large static prompts without caching, it suggests injecting `ContextCacheConfig`:

```python
# ❌ INSECURE/EXPENSIVE: Monolithic prompt without caching
# agent = Agent(instruction="Very long prompt...")

# ✅ SECURE/EFFICIENT: Context Caching
from google.adk.agents import Agent
from google.adk.agents.context_cache_config import ContextCacheConfig

agent = Agent(
    instruction="Very long prompt...",
    context_cache_config=ContextCacheConfig(ttl_seconds=300)
)
```
