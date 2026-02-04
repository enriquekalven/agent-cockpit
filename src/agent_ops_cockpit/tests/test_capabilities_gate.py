import os
import re
import pytest

def test_capabilities_registry_coverage():
    """
    Meta-Test: Ensures every capability in CAPABILITIES_REGISTRY.md 
    has a valid test file and at least one test function.
    """
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    registry_path = os.path.join(root, "CAPABILITIES_REGISTRY.md")
    
    assert os.path.exists(registry_path), "CAPABILITIES_REGISTRY.md is missing!"
    
    with open(registry_path, "r") as f:
        content = f.read()
    
    # Regex to find | CAP-XXX | Name | Description | TestPath | ...
    # Match the table rows, extracting the value in the 4th column (test path)
    pattern = re.compile(r"\| \*\*CAP-\d+\*\* \| [^|]+ \| [^|]+ \| `([^`]+)` \|")
    matches = pattern.findall(content)
    
    assert len(matches) > 0, "No capabilities found in registry!"
    
    missing_tests = []
    for test_file in matches:
        test_path = os.path.join(root, "src", "agent_ops_cockpit", "tests", test_file)
        
        if not os.path.exists(test_path):
            missing_tests.append(f"{test_file} (File not found at {test_path})")
            continue
            
        with open(test_path, "r") as tf:
            test_content = tf.read()
            if "def test_" not in test_content:
                missing_tests.append(f"{test_file} (No test functions found)")
                
    if missing_tests:
        pytest.fail(f"Capability coverage gaps detected:\n" + "\n".join(missing_tests))
    
    print(f"\nVerified {len(matches)} core capabilities have active test suites.")
