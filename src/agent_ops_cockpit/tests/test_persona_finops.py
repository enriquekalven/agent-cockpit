from agent_ops_cockpit.optimizer import analyze_code

def test_finops_atomic_rag_check():
    """CFO: Optimization for small, atomic retrieval to save tokens."""
    code = "results = vector_db.retrieve(q)\n# Missing optimizations"
    issues = analyze_code(code)
    assert any(issue.id == "atomic_rag" for issue in issues)

def test_finops_tiered_orchestration():
    """CFO: Routing between Pro and Flash models for cost control."""
    code = "client.models.generate_content(model='gemini-1.5-pro', contents=q)"
    issues = analyze_code(code)
    assert any(issue.id == "tiered_orchestration" for issue in issues)

def test_finops_token_density():
    """CFO: Prompt compression to reduce 'Redundant English' waste."""
    code = "system_instruction = 'You are a helpful assistant who is very good at coding'"
    issues = analyze_code(code)
    assert any(issue.id == "prompt_compression" for issue in issues)

def test_finops_quota_management():
    """CFO: Ensuring Exponential Backoff to prevent wasted compute/failure noise."""
    code = "model.generate(q) # Missing backoff"
    issues = analyze_code(code)
    assert any(issue.id == "quota_management" for issue in issues)

def test_finops_context_caching():
    """CFO: Massive cost reduction for high-token contexts."""
    code = '"""' + "A" * 300 + '"""'
    issues = analyze_code(code)
    assert any(issue.id == "context_caching" for issue in issues)

def test_context_engineering_tool_hardening():
    """CFO/Reliability: Poka-Yoke for tool trajectories."""
    code = "def process_tool(task_type: str):\n    pass"
    issues = analyze_code(code, "agent.py")
    assert any(issue.id == "tool_hardening" for issue in issues)

def test_context_engineering_compaction():
    """CFO: Context window efficiency for long threads."""
    code = "class ChatSession:\n    def __init__(self):\n        self.history = []"
    issues = analyze_code(code, "agent.py")
    assert any(issue.id == "context_compaction" for issue in issues)
