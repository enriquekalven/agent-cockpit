# 📉 Optimization: Cost & Performance

Efficiency is the difference between a successful agent and an expensive prototype. The Cockpit provides three specialized optimizers to tune your stack.

## 💰 Cost Optimizer
The `CostOptimizer` analyzes your prompt structure and token usage.
- **Context Caching**: Identifies static portions of your prompt (System Instructions + Document Context) greater than 32k tokens and recommends **Vertex AI Context Caching**.
- **Savings**: Context caching can reduce input token costs by up to 90% for long-running sessions.

## 🧠 Memory Optimizer
Large context windows are expensive and slow. The `MemoryOptimizer` implements a **"Leaky Bucket"** eviction policy.
- **Dynamic Summarization**: When context exceeds a threshold, the optimizer summarizes earlier parts of the conversation.
- **Pruning**: Removes low-intent "chatter" tokens while preserving core reasoning context.

## ⚡ Performance Validator (Load Tester)
Ensures your agent can handle high-traffic production environments.
- **Concurrency**: Simulate 10, 50, or 100 concurrent users.
- **SLA Validation**: Measures **p90 Latency** to ensure 90% of your users receive a response within your target threshold (e.g., <2 seconds).
- **Tool Stress**: Validates that external tools don't bottleneck the agent's reasoning loop.

## 🌐 Infrastructure Optimization
Performance isn't just about tokens; it's about the pipes.
- **Cloud Run CPU Boost**: The Cockpit automatically audits for **Startup CPU Boost**, which reduces cold-start latency for Python and NodeJS agents by 50%.
- **GKE Workload Identity**: Optimizes IAM token exchanges by using native K8s service accounts instead of high-latency static keys.

## 🏗️ Language-Specific Tuning
The **Agent Optimizer** (`make audit`) is language-aware:
- **Go**: Identifies standard map usage and recommends `sync.Map` or Mutexes for high-concurrency tool paths.
- **NodeJS**: Proposes the use of native `fetch()` (Node 20+) over heavy external libraries like Axios to reduce memory footprint.
- **Python**: Suggests `FastAPI` concurrency patterns over synchronous `requests` calls.


## 🎯 Model Routing
The Cockpit recommends using **Gemini 2.0 Flash Lite** (`gemini-2.0-flash-lite-001`) for ultra-low latency, high-volume tasks like:
- Query classification
- Output formatting
- Simple data extraction

Use the **ADK Rewind** feature to allow agents to backtrack and self-correct when a tool output is suboptimal.
Reserved **Gemini Pro** only for tasks requiring deep reasoning or multi-step tool orchestration.
