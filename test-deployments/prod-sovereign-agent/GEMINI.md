# Coding Agent Guide

**If your context window is limited:** Read this Table of Contents, then fetch only the sections you need.

## Table of Contents

### Part 1: ADK Cheatsheet
1. [Core Concepts & Project Structure](#1-core-concepts--project-structure)
2. [Agent Definitions (`LlmAgent`)](#2-agent-definitions-llmagent)
3. [Orchestration with Workflow Agents](#3-orchestration-with-workflow-agents)
4. [Multi-Agent Systems & Communication](#4-multi-agent-systems--communication)
5. [Building Custom Agents (`BaseAgent`)](#5-building-custom-agents-baseagent)
6. [Models Configuration](#6-models-configuration)
7. [Tools: The Agent's Capabilities](#7-tools-the-agents-capabilities)
8. [Context, State, and Memory](#8-context-state-and-memory)
9. [Callbacks](#9-callbacks)

### Part 2: Development Workflow
- [DESIGN_SPEC.md - Your Primary Reference](#designspecmd---your-primary-reference)
- [Phase 1: Understand the Spec](#phase-1-understand-the-spec)
- [Phase 2: Build and Implement](#phase-2-build-and-implement)
- [Phase 3: The Evaluation Loop](#phase-3-the-evaluation-loop-main-iteration-phase)
- [Phase 4: Pre-Deployment Tests](#phase-4-pre-deployment-tests)
- [Phase 5: Deploy to Dev](#phase-5-deploy-to-dev-environment)
- [Phase 6: Production Deployment](#phase-6-production-deployment---choose-your-path)
- [Development Commands](#development-commands)
- [Operational Guidelines](#operational-guidelines-for-coding-agents)

---

# ADK Cheatsheet

---

## 1. Core Concepts & Project Structure

### Essential Primitives

*   **`Agent`**: The core intelligent unit. Can be `LlmAgent` (LLM-driven) or `BaseAgent` (custom/workflow).
*   **`Tool`**: Callable function providing external capabilities (`FunctionTool`, `AgentTool`, etc.).
*   **`Session`**: A stateful conversation thread with history (`events`) and short-term memory (`state`).
*   **`State`**: Key-value dictionary within a `Session` for transient conversation data.
*   **`Runner`**: The execution engine; orchestrates agent activity and event flow.
*   **`Event`**: Atomic unit of communication; carries content and side-effect `actions`.

### Standard Project Layout

```
your_project_root/
├── my_agent/
│   ├── __init__.py
│   ├── agent.py          # Contains root_agent definition
│   ├── tools.py           # Custom tool functions
│   └── .env               # Environment variables
├── requirements.txt
└── tests/
```

---

## 2. Agent Definitions (`LlmAgent`)

### Basic Setup

```python
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    """Returns weather for a city."""
    return {"status": "success", "weather": "sunny", "temp": 72}

my_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    instruction="You help users check the weather. Use the get_weather tool.",
    description="Provides weather information.",  # Important for multi-agent delegation
    tools=[get_weather]
)
```

### Key Configuration Options

```python
from google.genai import types as genai_types
from google.adk.agents import Agent

agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="Your instructions here. Use {state_key} for dynamic injection.",
    description="Description for delegation.",

    # LLM generation parameters
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=1024,
    ),

    # Save final output to state
    output_key="agent_response",

    # Control history sent to LLM
    include_contents='default',  # 'default' or 'none'

    # Delegation control
    disallow_transfer_to_parent=False,
    disallow_transfer_to_peers=False,

    # Sub-agents for delegation
    sub_agents=[specialist_agent],

    # Tools
    tools=[my_tool],

    # Callbacks
    before_agent_callback=my_callback,
    after_agent_callback=my_callback,
    before_model_callback=my_callback,
    after_model_callback=my_callback,
    before_tool_callback=my_callback,
    after_tool_callback=my_callback,
)
```

### Structured Output with Pydantic

> **Warning**: Using `output_schema` disables tool calling and delegation.

```python
from pydantic import BaseModel, Field
from typing import Literal

class Evaluation(BaseModel):
    grade: Literal["pass", "fail"] = Field(description="The evaluation result.")
    comment: str = Field(description="Explanation of the grade.")

evaluator = Agent(
    name="evaluator",
    model="gemini-2.0-flash",
    instruction="Evaluate the input and provide structured feedback.",
    output_schema=Evaluation,
    output_key="evaluation_result",
)
```

### Instruction Best Practices

```python
# Use dynamic state injection
instruction = """
You are a {role} assistant.
User preferences: {user_preferences}

Rules:
- Always use tools when available
- Never make up information
"""

# Constrain tool usage
instruction = """
You help with research.
ONLY use google_search when the user explicitly asks for current information.
For general knowledge, answer directly.
"""
```

---

## 3. Orchestration with Workflow Agents

Workflow agents provide deterministic control flow without LLM orchestration.

### SequentialAgent

Executes sub-agents in order. State changes propagate to subsequent agents.

```python
from google.adk.agents import SequentialAgent, Agent

summarizer = Agent(
    name="summarizer",
    model="gemini-2.0-flash",
    instruction="Summarize the input.",
    output_key="summary"
)

question_gen = Agent(
    name="question_generator",
    model="gemini-2.0-flash",
    instruction="Generate questions based on: {summary}"
)

pipeline = SequentialAgent(
    name="pipeline",
    sub_agents=[summarizer, question_gen],
)
```

### ParallelAgent

Executes sub-agents concurrently. Use distinct `output_key`s to avoid race conditions.

```python
from google.adk.agents import ParallelAgent, SequentialAgent, Agent

fetch_a = Agent(name="fetch_a", ..., output_key="data_a")
fetch_b = Agent(name="fetch_b", ..., output_key="data_b")

merger = Agent(
    name="merger",
    instruction="Combine data_a: {data_a} and data_b: {data_b}"
)

pipeline = SequentialAgent(
    name="full_pipeline",
    sub_agents=[
        ParallelAgent(name="fetchers", sub_agents=[fetch_a, fetch_b]),
        merger
    ]
)
```

### LoopAgent

Repeats sub-agents until `max_iterations` or an event with `escalate=True`.

```python
from google.adk.agents import LoopAgent

refinement_loop = LoopAgent(
    name="refinement_loop",
    sub_agents=[evaluator, refiner, escalation_checker],
    max_iterations=5,
)
```

---

## 4. Multi-Agent Systems & Communication

### Communication Methods

1.  **Shared State**: Agents read/write `session.state`. Use `output_key` for convenience.

2.  **LLM Delegation**: Agent transfers control to a sub-agent based on reasoning.
    ```python
    coordinator = Agent(
        name="coordinator",
        instruction="Route to sales_agent for sales, support_agent for help.",
        sub_agents=[sales_agent, support_agent],
    )
    ```

3.  **AgentTool**: Invoke another agent as a tool (parent stays in control).
    ```python
    from google.adk.tools import AgentTool

    root = Agent(
        name="root",
        tools=[AgentTool(specialist_agent)],
    )
    ```

### Delegation vs AgentTool

```python
# Delegation: transfers control, sub-agent talks to user
root = Agent(name="root", sub_agents=[specialist])

# AgentTool: parent calls specialist, gets result, summarizes for user
root = Agent(name="root", tools=[AgentTool(specialist)])
```

---

## 5. Building Custom Agents (`BaseAgent`)

For custom orchestration logic beyond workflow agents.

```python
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from typing import AsyncGenerator

class ConditionalRouter(BaseAgent):
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # Read state
        user_type = ctx.session.state.get("user_type", "regular")

        # Custom routing logic
        if user_type == "premium":
            agent = self.premium_agent
        else:
            agent = self.regular_agent

        # Run selected agent
        async for event in agent.run_async(ctx):
            yield event

class EscalationChecker(BaseAgent):
    """Stops a LoopAgent when condition is met."""
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        result = ctx.session.state.get("evaluation")
        if result and result.get("grade") == "pass":
            yield Event(author=self.name, actions=EventActions(escalate=True))
        else:
            yield Event(author=self.name)
```

---

## 6. Models Configuration

### Google Gemini (Default)

```python
# AI Studio (dev)
# Set: GOOGLE_API_KEY, GOOGLE_GENAI_USE_VERTEXAI=False

# Vertex AI (prod)
# Set: GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, GOOGLE_GENAI_USE_VERTEXAI=True

agent = Agent(model="gemini-2.0-flash", ...)
```

### Other Models via LiteLLM

```python
from google.adk.models.lite_llm import LiteLlm

agent = Agent(model=LiteLlm(model="openai/gpt-4o"), ...)
agent = Agent(model=LiteLlm(model="anthropic/claude-3-haiku-20240307"), ...)
agent = Agent(model=LiteLlm(model="ollama_chat/llama3:instruct"), ...)
```

---

## 7. Tools: The Agent's Capabilities

### Function Tool Basics

```python
from google.adk.tools import ToolContext

def search_database(
    query: str,
    limit: int,
    tool_context: ToolContext  # Optional, for state access
) -> dict:
    """Searches the database for records matching the query.

    Args:
        query: The search query string.
        limit: Maximum number of results to return.

    Returns:
        dict with 'status' and 'results' keys.
    """
    # Access state if needed
    user_id = tool_context.state.get("user_id")

    # Tool logic here
    results = db.search(query, limit=limit, user=user_id)

    return {"status": "success", "results": results}
```

**Tool Rules:**
- Use clear docstrings (sent to LLM)
- Type hints required, NO default values
- Return a dict (JSON-serializable)
- Don't mention `tool_context` in docstring

### ToolContext Capabilities

```python
def my_tool(query: str, tool_context: ToolContext) -> dict:
    # Read/write state
    tool_context.state["key"] = "value"

    # Trigger escalation (stops LoopAgent)
    tool_context.actions.escalate = True

    # Artifacts
    tool_context.save_artifact("file.txt", part)
    data = tool_context.load_artifact("file.txt")

    # Memory search
    results = tool_context.search_memory("query")

    return {"status": "success"}
```

### Built-in Tools

```python
from google.adk.tools import google_search
from google.adk.tools.load_web_page import load_web_page
from google.adk.code_executors import BuiltInCodeExecutor

# Google Search grounding
agent = Agent(tools=[google_search], ...)

# Web page loading
agent = Agent(tools=[load_web_page], ...)

# Code execution
agent = Agent(code_executor=BuiltInCodeExecutor(), ...)
```

### Tool Confirmation

```python
from google.adk.tools import FunctionTool

# Simple confirmation
sensitive_tool = FunctionTool(delete_record, require_confirmation=True)

# Conditional confirmation
def needs_approval(amount: float, **kwargs) -> bool:
    return amount > 1000

transfer_tool = FunctionTool(transfer_money, require_confirmation=needs_approval)
```

---

## 8. Context, State, and Memory

### State Prefixes

```python
# Session-specific (default)
state["booking_step"] = 2

# User-persistent (across sessions)
state["user:preferred_language"] = "en"

# App-wide (all users)
state["app:total_queries"] = 1000

# Temporary (current invocation only)
state["temp:intermediate_result"] = data
```

### Session Service Options

```python
from google.adk.sessions import InMemorySessionService
# For dev: InMemorySessionService()
# For prod: VertexAiSessionService(), DatabaseSessionService()
```

### Memory (Long-term Knowledge)

```python
from google.adk.memory import InMemoryMemoryService

memory_service = InMemoryMemoryService()
# Add session to memory after conversation
await memory_service.add_session_to_memory(session)
# Search later
results = await memory_service.search_memory(app_name, user_id, "query")
```

---

## 9. Callbacks

### Callback Types

```python
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types as genai_types

# Agent lifecycle
async def before_agent_callback(ctx: CallbackContext) -> None:
    ctx.state["started"] = True

async def after_agent_callback(ctx: CallbackContext) -> genai_types.Content | None:
    # Return None to continue, or Content to override
    return None

# Model interaction
async def before_model_callback(ctx: CallbackContext, request: LlmRequest) -> LlmResponse | None:
    # Return None to continue, or LlmResponse to skip model call
    return None

async def after_model_callback(ctx: CallbackContext, response: LlmResponse) -> LlmResponse | None:
    # Return None to continue, or modified LlmResponse
    return None

# Tool execution
async def before_tool_callback(ctx: CallbackContext, tool_name: str, args: dict) -> dict | None:
    # Return None to continue, or dict to skip tool and use as result
    return None

async def after_tool_callback(ctx: CallbackContext, tool_name: str, result: dict) -> dict | None:
    # Return None to continue, or modified dict
    return None
```

### Common Patterns

```python
# Initialize state before agent runs
async def init_state(ctx: CallbackContext) -> None:
    if "preferences" not in ctx.state:
        ctx.state["preferences"] = {}

agent = Agent(before_agent_callback=init_state, ...)

# Collect data after agent runs
async def collect_sources(ctx: CallbackContext) -> None:
    session = ctx._invocation_context.session
    sources = []
    for event in session.events:
        if event.grounding_metadata:
            sources.extend(event.grounding_metadata.grounding_chunks)
    ctx.state["sources"] = sources

agent = Agent(after_agent_callback=collect_sources, ...)
```

---

## Quick Reference

### Running Agents Programmatically

```python
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

async def run_agent(agent, query: str):
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="app", user_id="user", session_id="session"
    )
    runner = Runner(agent=agent, app_name="app", session_service=session_service)

    async for event in runner.run_async(
        user_id="user",
        session_id="session",
        new_message=genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(text=query)]
        ),
    ):
        if event.is_final_response():
            return event.content.parts[0].text

result = asyncio.run(run_agent(my_agent, "Hello!"))
```

### CLI Commands

```bash
adk web /path/to/project    # Web UI
adk run /path/to/agent      # CLI chat
adk api_server /path/to     # FastAPI server
adk eval agent/ evalset.json  # Run evaluations
```

### Further Reading

- [ADK Documentation](https://google.github.io/adk-docs/llms.txt)
- [ADK Samples](https://github.com/google/adk-samples)


For further reading on ADK, see: https://google.github.io/adk-docs/llms.txt

---

# Agentic Development Workflow

## DESIGN_SPEC.md - Your Primary Reference

**IMPORTANT**: If `DESIGN_SPEC.md` exists in this project, it is your primary source of truth.

Read it FIRST to understand:
- Functional requirements and capabilities
- Success criteria and quality thresholds
- Agent behavior constraints
- Expected tools and integrations

**The spec is your contract.** All implementation decisions should align with it. When in doubt, refer back to DESIGN_SPEC.md.

## Phase 1: Understand the Spec

Before writing any code:
1. Read `DESIGN_SPEC.md` thoroughly
2. Identify the core capabilities required
3. Note any constraints or things the agent should NOT do
4. Understand success criteria for evaluation

## Phase 2: Build and Implement

Implement the agent logic:

1. Write/modify code in `app/`
2. Use `make playground` for interactive testing during development
3. Iterate on the implementation based on user feedback

## Phase 3: The Evaluation Loop (Main Iteration Phase)

This is where most iteration happens. Work with the user to:

1. **Start small**: Begin with 1-2 sample eval cases, not a full suite
2. Run evaluations: `make eval`
3. Discuss results with the user
4. Fix issues and iterate on the core cases first
5. Only after core cases pass, add edge cases and new scenarios
6. Adjust prompts, tools, or agent logic based on results
7. Repeat until quality thresholds are met

**Why start small?** Too many eval cases at the beginning creates noise. Get 1-2 core cases passing first to validate your agent works, then expand coverage.

```bash
make eval
```

Review the output:
- `tool_trajectory_avg_score`: Are the right tools called in order?
- `response_match_score`: Do responses match expected patterns?

**Expect 5-10+ iterations here** as you refine the agent with the user.

### LLM-as-a-Judge Evaluation (Recommended)

For high-quality evaluations, use LLM-based metrics that judge response quality semantically.

**Running with custom config:**
```bash
uv run adk eval ./app <path_to_evalset.json> --config_file_path=<path_to_config.json>
```

Or use the Makefile:
```bash
make eval EVALSET=tests/eval/evalsets/my_evalset.json
```

**Configuration Schema (`test_config.json`):**

**CRITICAL:** The JSON configuration for rubrics **must use camelCase** (not snake_case).

```json
{
  "criteria": {
    "tool_trajectory_avg_score": 1.0,
    "final_response_match_v2": 0.8,
    "rubric_based_final_response_quality_v1": {
      "threshold": 0.8,
      "rubrics": [
        {
          "rubricId": "professionalism",
          "rubricContent": { "textProperty": "The response must be professional and helpful." }
        },
        {
          "rubricId": "safety",
          "rubricContent": { "textProperty": "The agent must NEVER book without asking for confirmation." }
        }
      ]
    }
  }
}
```

**EvalSet Schema (`evalset.json`):**
```json
{
  "eval_set_id": "my_eval_set",
  "eval_cases": [
    {
      "eval_id": "search_test",
      "conversation": [
        {
          "user_content": { "parts": [{ "text": "Find a flight to NYC" }] },
          "final_response": {
            "role": "model",
            "parts": [{ "text": "I found a flight for $500. Want to book?" }]
          },
          "intermediate_data": {
            "tool_uses": [
              { "name": "search_flights", "args": { "destination": "NYC" } }
            ]
          }
        }
      ],
      "session_input": { "app_name": "my_app", "user_id": "user_1", "state": {} }
    }
  ]
}
```

**Key Metrics:**

| Metric | Purpose |
|--------|---------|
| `tool_trajectory_avg_score` | Ensures the right tools were called in the right order |
| `final_response_match_v2` | Uses LLM to check if agent's answer matches ground truth semantically |
| `rubric_based_final_response_quality_v1` | Judges agent against custom rules (tone, safety, confirmation) |
| `hallucinations_v1` | Ensures agent's response is grounded in tool output |

For complete metric definitions, see: `site-packages/google/adk/evaluation/eval_metrics.py`

**Prefer Rubrics over Semantic Matches:**

For complex outputs like executive digests or multi-part responses, `final_response_match_v2` is often too sensitive. `rubric_based_final_response_quality_v1` is far superior because it judges specific qualities (tone, citations, strategic relevance) rather than comparing against a static string.

**The Proactivity Trajectory Gap:**

LLMs are often "too helpful" and will perform extra actions. For example, an agent might call `google_search` immediately after `save_preferences` even when not asked. This causes `tool_trajectory_avg_score` failures. Solutions:
- Include ALL tools the agent might call in your expected trajectory
- Use extremely strict instructions: "Stop after calling save_preferences. Do NOT search."
- Use rubric-based evaluation instead of trajectory matching

**Multi-turn conversations require tool_uses for ALL turns:**

The `tool_trajectory_avg_score` uses EXACT matching. If you don't specify expected tool calls for intermediate turns, the evaluation will fail even if the agent called the right tools.

```json
{
  "conversation": [
    {
      "invocation_id": "inv_1",
      "user_content": { "parts": [{"text": "Find me a flight from NYC to London on 2026-06-01"}] },
      "intermediate_data": {
        "tool_uses": [
          { "name": "search_flights", "args": {"origin": "NYC", "destination": "LON", "departure_date": "2026-06-01"} }
        ]
      }
    },
    {
      "invocation_id": "inv_2",
      "user_content": { "parts": [{"text": "Book the first option for Elias (elias@example.com)"}] },
      "intermediate_data": {
        "tool_uses": [
          { "name": "get_flight_price", "args": {"flight_offer": {"id": "1", "price": {"total": "500.00"}}} }
        ]
      }
    },
    {
      "invocation_id": "inv_3",
      "user_content": { "parts": [{"text": "Yes, confirm the booking"}] },
      "final_response": { "role": "model", "parts": [{"text": "Booking confirmed! Reference: ABC123"}] },
      "intermediate_data": {
        "tool_uses": [
          { "name": "book_flight", "args": {"passenger_name": "Elias", "email": "elias@example.com"} }
        ]
      }
    }
  ]
}
```

**Common eval failure causes:**
- Missing `tool_uses` in intermediate turns → trajectory score fails
- Agent mentions data not in tool output → `hallucinations_v1` fails
- Response not explicit enough → `rubric_based` score drops

**The `before_agent_callback` Pattern (State Initialization):**

Always use a callback to initialize session state variables used in your instruction template (like `{user_preferences}`). This prevents `KeyError` crashes on the first turn before the user has provided data:

```python
async def initialize_state(callback_context: CallbackContext) -> None:
    """Initialize session state with defaults if not present."""
    state = callback_context.state
    if "user_preferences" not in state:
        state["user_preferences"] = {}
    if "feedback_history" not in state:
        state["feedback_history"] = []

root_agent = Agent(
    name="my_agent",
    before_agent_callback=initialize_state,
    instruction="Based on preferences: {user_preferences}...",
    ...
)
```

**Eval-State Overrides (Type Mismatch Danger):**

Be careful with `session_input.state` in your evalset.json. It overrides Python-level initialization and can introduce type errors:

```json
// WRONG - initializes feedback_history as a string, breaks .append()
"state": { "feedback_history": "" }

// CORRECT - matches the Python type (list)
"state": { "feedback_history": [] }
```

This can cause cryptic errors like `AttributeError: 'str' object has no attribute 'append'` in your tool logic.

### Evaluation Gotchas

**App name must match directory name:**
The `App` object's `name` parameter MUST match the directory containing your agent. If your agent is in the `app/` directory, use `name="app"`:

```python
# ✅ CORRECT - matches the "app" directory
app = App(root_agent=root_agent, name="app")

# ❌ WRONG - causes "Session not found" errors
app = App(root_agent=root_agent, name="flight_booking_assistant")
```

If names don't match, you'll get: `Session not found... The runner is configured with app name "X", but the root agent was loaded from ".../app"`

**Evaluating Agents with `google_search` (IMPORTANT):**

`google_search` is NOT a regular tool - it's a **model-internal grounding feature**:

```python
# How google_search works internally:
llm_request.config.tools.append(
    types.Tool(google_search=types.GoogleSearch())  # Injected into model config
)
```

**Key behavior:**
- Custom tools (`save_preferences`, `save_feedback`) → appear as `function_call` in trajectory ✓
- `google_search` → NEVER appears in trajectory ✗ (happens inside the model)
- Search results come back as `grounding_metadata`, not function call/response events

**BUT the evaluator STILL detects it** at the session level:
```json
{
  "error_code": "UNEXPECTED_TOOL_CALL",
  "error_message": "Unexpected tool call: google_search"
}
```

This causes `tool_trajectory_avg_score` to ALWAYS fail for agents using `google_search`.

**Metric compatibility for `google_search` agents:**

| Metric | Usable? | Why |
|--------|---------|-----|
| `tool_trajectory_avg_score` | NO | Always fails due to unexpected google_search |
| `response_match_score` | Maybe | Unreliable for dynamic news content |
| `rubric_based_final_response_quality_v1` | YES | Evaluates output quality semantically |
| `final_response_match_v2` | Maybe | Works for stable expected outputs |

**Evalset best practices for `google_search` agents:**

```json
{
  "eval_id": "news_digest_test",
  "conversation": [{
    "user_content": { "parts": [{"text": "Give me my news digest."}] }
    // NO intermediate_data.tool_uses for google_search - it won't match anyway
  }]
}
```

For custom tools alongside google_search, still include them (but NOT google_search):
```json
{
  "intermediate_data": {
    "tool_uses": [
      { "name": "save_feedback" }  // Custom tools work fine
      // Do NOT include google_search here
    ]
  }
}
```

**Config for `google_search` agents:**

```json
{
  "criteria": {
    // REMOVE this - incompatible with google_search:
    // "tool_trajectory_avg_score": 1.0,

    // Use rubric-based evaluation instead:
    "rubric_based_final_response_quality_v1": {
      "threshold": 0.6,
      "rubrics": [
        { "rubricId": "has_citations", "rubricContent": { "textProperty": "Response includes source citations or references" } },
        { "rubricId": "relevance", "rubricContent": { "textProperty": "Response directly addresses the user's query" } }
      ]
    }
  }
}
```

**Bottom line:** `google_search` is a model feature, not a function tool. You cannot test it with trajectory matching. Use rubric-based LLM-as-judge evaluation to verify the agent produces grounded, cited responses.

**ADK Built-in Tools: Trajectory Behavior Reference**

This applies to ALL Gemini model-internal tools, not just `google_search`:

**Model-Internal Tools (DON'T appear in trajectory):**

| Tool | Type | In Trajectory? | Eval Strategy |
|------|------|----------------|---------------|
| `google_search` | `types.GoogleSearch()` | ❌ No | Rubric-based |
| `google_search_retrieval` | `types.GoogleSearchRetrieval()` | ❌ No | Rubric-based |
| `BuiltInCodeExecutor` | `types.CodeExecution()` | ❌ No | Check output |
| `VertexAiSearchTool` | `types.Retrieval()` | ❌ No | Rubric-based |
| `url_context` | Model-internal | ❌ No | Rubric-based |

These inject into `llm_request.config.tools` as model capabilities:
```python
types.Tool(google_search=types.GoogleSearch())
types.Tool(code_execution=types.ToolCodeExecution())
types.Tool(retrieval=types.Retrieval(...))
```

**Function-Based Tools (DO appear in trajectory):**

| Tool | Type | In Trajectory? | Eval Strategy |
|------|------|----------------|---------------|
| `load_web_page` | FunctionTool | ✅ Yes | `tool_trajectory_avg_score` works |
| Custom tools | FunctionTool | ✅ Yes | `tool_trajectory_avg_score` works |
| AgentTool | Wrapped agent | ✅ Yes | `tool_trajectory_avg_score` works |

These generate `function_call` and `function_response` events:
```python
types.Tool(function_declarations=[...])
```

**Quick Reference - Can I use `tool_trajectory_avg_score`?**
- `google_search` → NO (model-internal)
- `code_executor` → NO (model-internal)
- `VertexAiSearchTool` → NO (model-internal)
- `load_web_page` → YES (FunctionTool)
- Custom functions → YES (FunctionTool)

**Rule of Thumb:**
- If a tool provides grounding/retrieval/execution capabilities built into Gemini → model-internal, won't appear in trajectory
- If it's a Python function you can call → appears in trajectory, can test with `tool_trajectory_avg_score`

**When mixing both types** (e.g., `google_search` + `save_preferences`):
1. Remove `tool_trajectory_avg_score` entirely, OR
2. Only test function-based tools in `tool_uses` and accept the trajectory will be incomplete

**Model thinking mode may bypass tools:**
Models with "thinking" enabled may decide they have sufficient information and skip tool calls. Use `tool_config` with `mode="ANY"` to force tool usage, or switch to a non-thinking model like `gemini-2.0-flash` for predictable tool calling.

**Sub-agents need instances, not function references:**
When using multi-agent systems with `sub_agents`, you must pass **Agent instances**, not factory function references.

```python
# ❌ WRONG - This fails with ValidationError
sub_agents=[
    create_lead_qualifier,   # Function reference - FAILS!
    create_product_matcher,  # Function reference - FAILS!
]

# ✅ CORRECT - Call the factories to get instances
sub_agents=[
    create_lead_qualifier(),   # Instance - WORKS
    create_product_matcher(),  # Instance - WORKS
]
```

**Root cause**: ADK's pydantic validation expects `BaseAgent` instances, not callables. The error message is:
`ValidationError: Input should be a valid dictionary or instance of BaseAgent`

When using `SequentialAgent` with sub-agents that may be reused, create each sub-agent via a factory function (not module-level instances) to avoid "agent already has a parent" errors:

```python
def create_researcher():
    return Agent(name="researcher", ...)

root_agent = SequentialAgent(
    sub_agents=[create_researcher(), create_analyst()],  # Note: calling the functions!
    ...
)
```

**A2A handoffs pass data between agents:**
When using multi-agent systems (SequentialAgent), data flows between sub-agents through the conversation history and context. To ensure proper handoffs:

```python
# Lead Qualifier agent should include score in response
def create_lead_qualifier():
    return Agent(
        name="lead_qualifier",
        instruction="Score leads 1-100. ALWAYS include the score in your response: 'Lead score: XX/100'",
        ...
    )

# Product Matcher receives the score via conversation context
def create_product_matcher():
    return Agent(
        name="product_matcher",
        instruction="Recommend products based on the lead score from the previous agent.",
        ...
    )
```

Verify handoffs in eval by checking that sub-agents reference data from previous agents in their responses.

**Mock mode for external APIs:**
When your agent calls external APIs, add mock mode so evals can run without real credentials:
```python
def call_external_api(query: str) -> dict:
    api_key = os.environ.get("EXTERNAL_API_KEY", "")
    if not api_key or api_key == "dummy_key":
        return {"status": "success", "data": "mock_response"}
    # Real API call here
```

## Custom Infrastructure (Terraform)

**CRITICAL**: When your agent requires custom infrastructure (Cloud SQL, Pub/Sub topics, Eventarc triggers, BigQuery datasets, VPC connectors, etc.), you MUST define it in Terraform - never create resources manually via `gcloud` commands.

### Where to Put Custom Terraform

| Scenario | Location | When to Use |
|----------|----------|-------------|
| Dev-only infrastructure | `deployment/terraform/dev/` | Quick prototyping, single environment |
| CI/CD environments (staging/prod) | `deployment/terraform/` | Production deployments with staging/prod separation |

### Adding Custom Infrastructure

**For dev-only (Option A deployment):**

Create a new `.tf` file in `deployment/terraform/dev/`:

```hcl
# deployment/terraform/dev/custom_resources.tf

# Example: Pub/Sub topic for event processing
resource "google_pubsub_topic" "events" {
  name    = "${var.project_name}-events"
  project = var.dev_project_id
}

# Example: BigQuery dataset for analytics
resource "google_bigquery_dataset" "analytics" {
  dataset_id = "${replace(var.project_name, "-", "_")}_analytics"
  project    = var.dev_project_id
  location   = var.region
}

# Example: Eventarc trigger for Cloud Storage
resource "google_eventarc_trigger" "storage_trigger" {
  name     = "${var.project_name}-storage-trigger"
  location = var.region
  project  = var.dev_project_id

  matching_criteria {
    attribute = "type"
    value     = "google.cloud.storage.object.v1.finalized"
  }
  matching_criteria {
    attribute = "bucket"
    value     = google_storage_bucket.uploads.name
  }

  destination {
    cloud_run_service {
      service = google_cloud_run_v2_service.app.name
      region  = var.region
      path    = "/invoke"
    }
  }

  service_account = google_service_account.app_sa.email
}
```

**For CI/CD environments (Option B deployment):**

Add resources to `deployment/terraform/` (applies to staging and prod):

```hcl
# deployment/terraform/custom_resources.tf

# Resources here are created in BOTH staging and prod projects
# Use for_each with local.deploy_project_ids for multi-environment

resource "google_pubsub_topic" "events" {
  for_each = local.deploy_project_ids
  name     = "${var.project_name}-events"
  project  = each.value
}
```

### IAM for Custom Resources

When adding custom resources, ensure your app service account has the necessary permissions:

```hcl
# Add to deployment/terraform/dev/iam.tf or deployment/terraform/iam.tf

# Example: Grant Pub/Sub publisher permission
resource "google_pubsub_topic_iam_member" "app_publisher" {
  topic   = google_pubsub_topic.events.name
  project = var.dev_project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.app_sa.email}"
}

# Example: Grant BigQuery data editor
resource "google_bigquery_dataset_iam_member" "app_editor" {
  dataset_id = google_bigquery_dataset.analytics.dataset_id
  project    = var.dev_project_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${google_service_account.app_sa.email}"
}
```

### Applying Custom Infrastructure

```bash
# For dev-only infrastructure
make setup-dev-env  # Runs terraform apply in deployment/terraform/dev/

# For CI/CD, infrastructure is applied automatically:
# - On setup-cicd: Terraform runs for staging and prod
# - On git push: CI/CD pipeline runs terraform plan/apply
```

### Common Patterns

**Cloud Storage trigger (Eventarc):**
- Create bucket in Terraform
- Create Eventarc trigger pointing to `/invoke` endpoint
- Grant `eventarc.eventReceiver` role to app service account

**Pub/Sub processing:**
- Create topic and push subscription in Terraform
- Point subscription to `/invoke` endpoint
- Grant `iam.serviceAccountTokenCreator` role for push auth

**BigQuery Remote Function:**
- Create BigQuery connection in Terraform
- Grant connection service account permission to invoke Cloud Run
- Create the remote function via SQL after deployment

**Cloud SQL sessions:**
- Already configured by ASP when using `--session-type cloud_sql`
- Additional tables/schemas can be added via migration scripts

**Secret Manager (for API credentials):**

Instead of passing sensitive keys as environment variables (which can be logged or visible in console), use GCP Secret Manager.

**1. Store secrets via gcloud:**
```bash
# Create the secret
echo -n "YOUR_API_KEY" | gcloud secrets create MY_SECRET_NAME --data-file=-

# Update an existing secret
echo -n "NEW_API_KEY" | gcloud secrets versions add MY_SECRET_NAME --data-file=-
```

**2. Grant access (IAM):**
The agent's service account needs the `Secret Manager Secret Accessor` role:
```bash
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects list --filter="project_id:$PROJECT_ID" --format="value(project_number)")
SA_EMAIL="service-$PROJECT_NUMBER@gcp-sa-aiplatform-re.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/secretmanager.secretAccessor"
```

**3. Use secrets in deployment (Agent Engine):**

Pass secrets during deployment with `--set-secrets`. Note: `make deploy` doesn't support secrets, so run deploy.py directly:
```bash
uv run python -m app.app_utils.deploy --set-secrets "API_KEY=my-api-key,DB_PASS=db-password:2"
```

Format: `ENV_VAR=SECRET_ID` or `ENV_VAR=SECRET_ID:VERSION` (defaults to latest).

In your agent code, access via `os.environ`:
```python
import os
import json

api_key = os.environ.get("API_KEY")
# For JSON secrets:
db_creds = json.loads(os.environ.get("DB_PASS", "{}"))
```

## Phase 4: Pre-Deployment Tests

Once evaluation thresholds are met, run tests before deployment:

```bash
make test
```

If tests fail, fix issues and run again until all tests pass.

## Phase 5: Deploy to Dev Environment

Deploy to the development environment for final testing:

1. **Notify the human**: "Eval scores meet thresholds and tests pass. Ready to deploy to dev?"
2. **Wait for explicit approval**
3. Once approved: `make deploy`

This deploys to the dev GCP project for live testing.

**IMPORTANT**: Never run `make deploy` without explicit human approval.

### Deployment Timeouts

Agent Engine deployments can take 5-10 minutes. If `make deploy` times out:

1. Check if deployment succeeded:
```python
import vertexai
client = vertexai.Client(location="us-central1")
for engine in client.agent_engines.list():
    print(engine.name, engine.display_name)
```

2. If the engine exists, update `deployment_metadata.json` with the engine ID.

## Phase 6: Production Deployment - Choose Your Path

After validating in dev, **ask the user** which deployment approach they prefer:

### Option A: Simple Single-Project Deployment (Recommended for getting started)

**Best for:**
- Personal projects or prototypes
- Teams without complex CI/CD requirements
- Quick deployments to a single environment

**Steps:**
1. Set up infrastructure: `make setup-dev-env`
2. Deploy: `make deploy`

**Pros:**
- Simpler setup, faster to get running
- Single GCP project to manage
- Direct control over deployments

**Cons:**
- No automated staging/prod pipeline
- Manual deployments each time
- No automated testing on push

### Option B: Full CI/CD Pipeline (Recommended for production)

**Best for:**
- Production applications
- Teams requiring staging → production promotion
- Automated testing and deployment workflows

**Prerequisites:**
1. Project must NOT be in a gitignored folder
2. User must provide staging and production GCP project IDs
3. GitHub repository name and owner

Note: `setup-cicd` automatically initializes git if needed.

**Steps:**
1. If prototype, first add Terraform/CI-CD files:
   ```bash
   # Programmatic invocation (requires --cicd-runner with -y to skip prompts)
   uvx agent-starter-pack enhance . \
     --cicd-runner github_actions \
     -y -s
   ```
   Or use the equivalent MCP tool call (`enhance_project`) if available.

2. Ensure you're logged in to GitHub CLI:
   ```bash
   gh auth login  # (skip if already authenticated)
   ```

3. Run setup-cicd with your GCP project IDs (no PAT needed - uses gh auth):
   ```bash
   uvx agent-starter-pack setup-cicd \
     --staging-project YOUR_STAGING_PROJECT \
     --prod-project YOUR_PROD_PROJECT \
     --repository-name YOUR_REPO_NAME \
     --repository-owner YOUR_GITHUB_USERNAME \
     --auto-approve \
     --create-repository
   ```
   Note: The CI/CD runner type is auto-detected from Terraform files created by `enhance`.

4. This creates infrastructure in BOTH staging and production projects
5. Sets up GitHub Actions triggers
6. Push code to trigger deployments

**Pros:**
- Automated testing on every push
- Safe staging → production promotion
- Audit trail and approval workflows

**Cons:**
- Requires 2-3 GCP projects (staging, prod, optionally cicd)
- More initial setup time
- Requires GitHub repository

### Choosing a CI/CD Runner

| Runner | Pros | Cons |
|--------|------|------|
| **github_actions** (Default) | No PAT needed, uses `gh auth`, WIF-based, fully automated | Requires GitHub CLI authentication |
| **google_cloud_build** | Native GCP integration | Requires interactive browser authorization (or PAT + app installation ID for programmatic mode) |

**How authentication works:**
- **github_actions**: The Terraform GitHub provider automatically uses your `gh auth` credentials. No separate PAT export needed.
- **google_cloud_build**: Interactive mode uses browser auth. Programmatic mode requires `--github-pat` and `--github-app-installation-id`.

### After CI/CD Setup: Activating the Pipeline

**IMPORTANT**: `setup-cicd` creates infrastructure but doesn't deploy the agent automatically.

Terraform automatically configures all required GitHub secrets and variables (WIF credentials, project IDs, service accounts, etc.). No manual configuration needed.

#### Step 1: Commit and Push

```bash
git add . && git commit -m "Initial agent implementation"
git push origin main
```

#### Step 2: Monitor Deployment

- **GitHub Actions**: Check the Actions tab in your repository
- **Cloud Build**: `gcloud builds list --project=YOUR_CICD_PROJECT --region=YOUR_REGION`

**Staging deployment** happens automatically on push to main.
**Production deployment** requires manual approval:

```bash
# GitHub Actions (recommended): Approve via repository Actions tab
# Production deploys are gated by environment protection rules

# Cloud Build: Find pending build and approve
gcloud builds list --project=PROD_PROJECT --region=REGION --filter="status=PENDING"
gcloud builds approve BUILD_ID --project=PROD_PROJECT
```

### Troubleshooting CI/CD

| Issue | Solution |
|-------|----------|
| Terraform state locked | `terraform force-unlock LOCK_ID` in deployment/terraform/ |
| Cloud Build authorization pending | Use `github_actions` runner instead |
| GitHub Actions auth failed | Check Terraform completed successfully; re-run `terraform apply` |
| Terraform apply failed | Check GCP permissions and API enablement |
| Resource already exists | Use `terraform import` to import existing resources into state |
| Agent Engine deploy timeout | Deployments take 5-10 min; check status via `gh run view RUN_ID` |

### Monitoring CI/CD Deployments

```bash
# List recent workflow runs
gh run list --repo OWNER/REPO --limit 5

# View run details and job status
gh run view RUN_ID --repo OWNER/REPO

# View specific job logs (when complete)
gh run view --job=JOB_ID --repo OWNER/REPO --log

# Watch deployment in real-time
gh run watch RUN_ID --repo OWNER/REPO
```

## Development Commands

| Command | Purpose |
|---------|---------|
| `make playground` | Interactive local testing |
| `make test` | Run unit and integration tests |
| `make eval` | Run evaluation against evalsets |
| `make eval-all` | Run all evalsets |
| `make lint` | Check code quality |
| `make setup-dev-env` | Set up dev infrastructure (Terraform) |
| `make deploy` | Deploy to dev |

## Testing Your Deployed Agent

After deployment, you can test your agent. The method depends on your deployment target.

### Getting Deployment Info

The deployment endpoint is stored in `deployment_metadata.json` after `make deploy` completes.

### Testing Agent Engine Deployment

Your agent is deployed to Vertex AI Agent Engine.

**Option 1: Using the Testing Notebook (Recommended)**

```bash
# Open the testing notebook
jupyter notebook notebooks/adk_app_testing.ipynb
```

The notebook auto-loads from `deployment_metadata.json` and provides:
- Remote testing via `vertexai.Client`
- Streaming queries with `async_stream_query`
- Feedback registration

**Option 2: Python Script**

```python
import json
import vertexai

# Load deployment info
with open("deployment_metadata.json") as f:
    engine_id = json.load(f)["remote_agent_engine_id"]

# Connect to agent
client = vertexai.Client(location="us-central1")
agent = client.agent_engines.get(name=engine_id)

# Send a message
async for event in agent.async_stream_query(message="Hello!", user_id="test"):
    print(event)
```

**Option 3: Using the Playground**

```bash
make playground
# Open http://localhost:8000 in your browser
```

### Testing Cloud Run Deployment

Your agent is deployed to Cloud Run.

**Option 1: Using the Testing Notebook (Recommended)**

```bash
# Open the testing notebook
jupyter notebook notebooks/adk_app_testing.ipynb
```

**Option 2: Python Script**

```python
import json
import requests

SERVICE_URL = "YOUR_SERVICE_URL"  # From deployment_metadata.json
ID_TOKEN = !gcloud auth print-identity-token -q
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {ID_TOKEN[0]}"}

# Step 1: Create a session
user_id = "test_user"
session_resp = requests.post(
    f"{SERVICE_URL}/apps/app/users/{user_id}/sessions",
    headers=headers,
    json={"state": {}}
)
session_id = session_resp.json()["id"]

# Step 2: Send a message
message_resp = requests.post(
    f"{SERVICE_URL}/run_sse",
    headers=headers,
    json={
        "app_name": "app",
        "user_id": user_id,
        "session_id": session_id,
        "new_message": {"role": "user", "parts": [{"text": "Hello!"}]},
        "streaming": True
    },
    stream=True
)

for line in message_resp.iter_lines():
    if line and line.decode().startswith("data: "):
        print(json.loads(line.decode()[6:]))
```

**Option 3: Using the Playground**

```bash
make playground
# Open http://localhost:8000 in your browser
```

### Deploying Frontend UI with IAP

For authenticated access to your UI (recommended for private-by-default deployments):

```bash
# Deploy frontend (builds on Cloud Build - avoids ARM/AMD64 mismatch on Apple Silicon)
gcloud run deploy SERVICE --source . --region REGION

# Enable IAP
gcloud beta run services update SERVICE --region REGION --iap

# Grant user access
gcloud beta iap web add-iam-policy-binding \
  --resource-type=cloud-run \
  --service=SERVICE \
  --region=REGION \
  --member=user:EMAIL \
  --role=roles/iap.httpsResourceAccessor
```

**Note:** Use `iap web add-iam-policy-binding` for IAP access, not `run services add-iam-policy-binding` (which is for `roles/run.invoker`).

### Testing A2A Protocol Agents

Your agent uses the A2A (Agent-to-Agent) protocol for inter-agent communication.

**Reference the integration tests** in `tests/integration/` for examples of how to call your deployed agent. The tests demonstrate the correct message format and API usage for your specific deployment target.

**A2A Protocol Common Mistakes:**

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Using `content` instead of `text` | `Invalid message format` | Use `parts[].text`, not `parts[].content` |
| Using `input` instead of `message` | `Missing message parameter` | Use `params.message`, not `params.input` |
| Missing `messageId` | `ValidationError` | Include `message.messageId` in every request |
| Missing `role` | `ValidationError` | Include `message.role` (usually "user") |

**A2A Protocol Key Details:**
- Protocol Version: 0.3.0
- Transport: JSON-RPC 2.0
- Required fields: `task_id`, `message.messageId`, `message.role`, `message.parts`
- Part structure: `{text: "...", mimeType: "text/plain"}`

**Testing approaches vary by deployment:**
- **Agent Engine**: Use the testing notebook or Python SDK (see integration tests)
- **Cloud Run**: Use curl with identity token or the testing notebook

**Example: Testing A2A agent on Cloud Run:**

```bash
# Get your service URL from deployment output or Cloud Console
SERVICE_URL="https://your-service-url.run.app"

# Send a test message using A2A protocol
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "message/send",
    "params": {
      "task_id": "test-task-001",
      "message": {
        "messageId": "msg-001",
        "role": "user",
        "parts": [
          {
            "text": "Your test query here",
            "mimeType": "text/plain"
          }
        ]
      }
    },
    "id": "req-1"
  }' \
  "$SERVICE_URL/a2a/app"

# Get the agent card (describes capabilities)
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  "$SERVICE_URL/a2a/app/.well-known/agent-card.json"
```

### Running Load Tests

To run load tests against your deployed agent:

```bash
make load-test
```

This uses Locust to simulate multiple concurrent users.

## Adding Evaluation Cases

To improve evaluation coverage:

1. Add cases to `tests/eval/evalsets/basic.evalset.json`
2. Each case should test a capability from DESIGN_SPEC.md
3. Include expected tool calls in `intermediate_data.tool_uses`
4. Run `make eval` to verify

## Advanced: Batch & Event Processing

### When to Use Batch/Event Processing

Your agent currently runs as an interactive service. However, many use cases require processing large volumes of data asynchronously:

**Batch Processing:**
- **BigQuery Remote Functions**: Process millions of rows with Gemini (e.g., `SELECT analyze(customer_data) FROM customers`)
- **Data Pipeline Integration**: Trigger agent analysis from Dataflow, Spark, or other batch systems

**Event-Driven Processing:**
- **Pub/Sub**: React to events in real-time (e.g., order processing, fraud detection)
- **Eventarc**: Trigger on GCP events (e.g., new file in Cloud Storage)
- **Webhooks**: Accept HTTP callbacks from external systems

### Adding an /invoke Endpoint

Add an `/invoke` endpoint to `app/fast_api_app.py` for batch/event processing. The endpoint auto-detects the input format (BigQuery Remote Function, Pub/Sub, Eventarc, or direct HTTP).

**Core pattern:** Create a `run_agent` helper using `Runner` + `InMemorySessionService` for stateless processing, with a semaphore for concurrency control. Then route by request shape:

```python
@app.post("/invoke")
async def invoke(request: Dict[str, Any]):
    if "calls" in request:        # BigQuery: {"calls": [[row1], [row2]]}
        results = await asyncio.gather(*[run_agent(f"Analyze: {row}") for row in request["calls"]])
        return {"replies": results}
    if "message" in request:      # Pub/Sub: {"message": {"data": "base64..."}}
        payload = base64.b64decode(request["message"]["data"]).decode()
        return {"status": "success", "result": await run_agent(payload)}
    if "type" in request:         # Eventarc: {"type": "google.cloud...", "data": {...}}
        return {"status": "success", "result": await run_agent(str(request["data"]))}
    if "input" in request:        # Direct HTTP: {"input": "prompt"}
        return {"status": "success", "result": await run_agent(request["input"])}
```

**Test locally** with `make local-backend`, then curl each format:
```bash
# BigQuery
curl -X POST http://localhost:8000/invoke -H "Content-Type: application/json" \
  -d '{"calls": [["test input 1"], ["test input 2"]]}'
# Direct
curl -X POST http://localhost:8000/invoke -H "Content-Type: application/json" \
  -d '{"input": "your prompt here"}'
```

**Connect to GCP services:**
```bash
# Pub/Sub push subscription
gcloud pubsub subscriptions create my-sub --topic=my-topic \
    --push-endpoint=https://my-super-agent.run.app/invoke
# Eventarc trigger
gcloud eventarc triggers create my-trigger \
    --destination-run-service=my-super-agent \
    --destination-run-path=/invoke \
    --event-filters="type=google.cloud.storage.object.v1.finalized"
```

**Production tips:** Use semaphores to limit concurrent Gemini calls (avoid 429s), set Cloud Run `--max-instances`, and return per-row errors instead of failing entire batches. See [reference implementation](https://github.com/richardhe-fundamenta/practical-gcp-examples/blob/main/bq-remote-function-agent/customer-advisor/app/fast_api_app.py) for production patterns.

---

## Operational Guidelines for Coding Agents

These guidelines are essential for working on this project effectively.

### Principle 1: Code Preservation & Isolation

When executing code modifications, your paramount objective is surgical precision. You **must alter only the code segments directly targeted** by the user's request, while **strictly preserving all surrounding and unrelated code.**

**Mandatory Pre-Execution Verification:**

Before finalizing any code replacement, verify:

1.  **Target Identification:** Clearly define the exact lines or expressions to be changed, based *solely* on the user's explicit instructions.
2.  **Preservation Check:** Ensure all code, configuration values (e.g., `model`, `version`, `api_key`), comments, and formatting *outside* the identified target remain identical.

**Example:**

*   **User Request:** "Change the agent's instruction to be a recipe suggester."
*   **Original Code:**
    ```python
    root_agent = Agent(
        name="root_agent",
        model="gemini-3-flash-preview",
        instruction="You are a helpful AI assistant."
    )
    ```
*   **Incorrect (VIOLATION):**
    ```python
    root_agent = Agent(
        name="recipe_suggester",
        model="gemini-1.5-flash",  # UNINTENDED - model was not requested to change
        instruction="You are a recipe suggester."
    )
    ```
*   **Correct (COMPLIANT):**
    ```python
    root_agent = Agent(
        name="recipe_suggester",  # OK, related to new purpose
        model="gemini-3-flash-preview",  # PRESERVED
        instruction="You are a recipe suggester."  # OK, the direct target
    )
    ```

**Critical:** Always prioritize the integrity of existing code over rewriting entire blocks.

### Principle 2: Execution Best Practices

*   **Model Selection - CRITICAL:**
    *   **NEVER change the model unless explicitly asked.** If the code uses `gemini-3-flash-preview`, keep it as `gemini-3-flash-preview`. Do NOT "upgrade" or "fix" model names.
    *   When creating NEW agents (not modifying existing), use Gemini 3 series: `gemini-3-flash-preview`, `gemini-3-pro-preview`.
    *   Do NOT use older models (`gemini-2.0-flash`, `gemini-1.5-flash`, etc.) unless the user explicitly requests them.

*   **Location Matters More Than Model:**
    *   If a model returns a 404, it's almost always a `GOOGLE_CLOUD_LOCATION` issue (e.g., needing `global` instead of `us-central1`).
    *   Changing the model name to "fix" a 404 is a violation - fix the location instead.
    *   Some models (like `gemini-3-flash-preview`) require specific locations. Check the error message for hints.

*   **ADK Built-in Tool Imports (Precision Required):**
    *   ADK built-in tools require surgical imports to get the tool instance, not the module:
    ```python
    # CORRECT - imports the tool instance
    from google.adk.tools.load_web_page import load_web_page

    # WRONG - imports the module, not the tool
    from google.adk.tools import load_web_page
    ```
    *   Pass the imported tool directly to `tools=[load_web_page]`, not `tools=[load_web_page.load_web_page]`.

*   **Running Python Commands:**
    *   Always use `uv` to execute Python commands (e.g., `uv run python script.py`)
    *   Run `make install` before executing scripts
    *   Consult `Makefile` and `README.md` for available commands

*   **Troubleshooting:**
    *   **Check the ADK cheatsheet in this file first** - it covers most common patterns
    *   **Need more depth?** Try checking ADK docs and source code.
    *   For framework questions (ADK, LangGraph) or GCP products (Cloud Run), check official documentation
    *   When encountering persistent errors, a targeted Google Search often finds solutions faster

*   **Breaking Infinite Loops:**
    *   **Stop immediately** if you see the same error 3+ times in a row
    *   **Don't retry failed operations** - fix the root cause first
    *   **RED FLAGS**: Lock IDs incrementing, names appending v5→v6→v7, "I'll try one more time" repeatedly
    *   **State conflicts** (Error 409: Resource already exists): Import existing resources with `terraform import` instead of retrying creation
    *   **Tool bugs**: Fix source code bugs before continuing - don't work around them
    *   **When stuck**: Run underlying commands directly (e.g., `terraform` CLI) instead of calling problematic tools
