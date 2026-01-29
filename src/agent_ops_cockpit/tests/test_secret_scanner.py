import re
from agent_ops_cockpit.ops.secret_scanner import SECRET_PATTERNS

def test_google_api_key_pattern():
    key = "AIzaSyD-1234567890abcdefghijklmnopqrstuv"
    assert re.search(SECRET_PATTERNS["Google API Key"], key)

def test_aws_key_pattern():
    key = "AKIA1234567890ABCDEF"
    assert re.search(SECRET_PATTERNS["AWS Access Key"], key)

def test_bearer_token_pattern():
    token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    assert re.search(SECRET_PATTERNS["Generic Bearer Token"], token)

def test_hardcoded_variable_pattern():
    code1 = 'api_key = "sk-1234567890abcdef"'
    code2 = 'client_secret = "secret-key-123456"'
    assert re.search(SECRET_PATTERNS["Hardcoded API Variable"], code1)
    assert re.search(SECRET_PATTERNS["Hardcoded API Variable"], code2)

def test_service_account_pattern():
    json_snippet = '"type": "service_account"'
    assert re.search(SECRET_PATTERNS["GCP Service Account"], json_snippet)
