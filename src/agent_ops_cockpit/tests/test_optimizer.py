from agent_ops_cockpit.optimizer import analyze_code

def test_analyze_openai_missing_cache():
    code = "import openai\nclient = openai.OpenAI()"
    issues = analyze_code(code)
    assert any(issue.id == "openai_caching" for issue in issues)

def test_analyze_anthropic_missing_orchestrator():
    code = "import anthropic\nclient = anthropic.Anthropic()"
    issues = analyze_code(code)
    assert any(issue.id == "anthropic_orchestration" for issue in issues)

def test_analyze_microsoft_missing_workflow():
    code = "from autogen import UserProxyAgent, AssistantAgent"
    issues = analyze_code(code)
    assert any(issue.id == "ms_workflows" for issue in issues)

def test_analyze_aws_missing_action_groups():
    code = "import boto3\nbedrock = boto3.client('bedrock-agent-runtime')"
    issues = analyze_code(code)
    assert any(issue.id == "aws_action_groups" for issue in issues)

def test_analyze_copilotkit_missing_shared_state():
    code = "import copilotkit\n# Some logic without state sync"
    issues = analyze_code(code)
    assert any(issue.id == "copilot_state" for issue in issues)

def test_analyze_model_routing_pro_only():
    code = "model = 'gemini-1.5-pro'"
    issues = analyze_code(code)
    assert any(issue.id == "model_routing" for issue in issues)

def test_analyze_missing_semantic_cache():
    code = "def chat(): pass"
    issues = analyze_code(code)
    assert any(issue.id == "semantic_caching" for issue in issues)

def test_analyze_context_caching():
    code = '"""' + "A" * 300 + '"""'
    issues = analyze_code(code)
    assert any(issue.id == "context_caching" for issue in issues)

def test_analyze_infrastructure_optimizations():
    # Cloud Run
    cr_code = "# Running on Cloud Run"
    cr_issues = analyze_code(cr_code)
    assert any(issue.id == "cr_startup_boost" for issue in cr_issues)
    
    # GKE
    gke_code = "# Running on GKE with Kubernetes"
    gke_issues = analyze_code(gke_code)
    assert any(issue.id == "gke_identity" for issue in gke_issues)

def test_analyze_language_optimizations():
    # Go
    go_code = "state := make(map[string]int)"
    go_issues = analyze_code(go_code, "main.go")
    assert any(issue.id == "go_concurrency" for issue in go_issues)
    
    # NodeJS
    js_code = "import axios from 'axios'"
    js_issues = analyze_code(js_code, "app.ts")
    assert any(issue.id == "node_native_fetch" for issue in js_issues)
def test_analyze_langgraph_optimizations():
    code = "from langgraph.graph import StateGraph"
    issues = analyze_code(code)
    assert any(issue.id == "langgraph_persistence" for issue in issues)
    assert any(issue.id == "langgraph_recursion" for issue in issues)
