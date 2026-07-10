"""Unit tests for the AST Structural Drift Detector Engine."""
import os
import shutil
import tempfile
import pytest
from agent_ops_cockpit.ops.architecture.drift import CodeDriftDetector


def test_drift_detector_layout_agnostic():
    code1 = """
def process_data(x: int):
    # This is a comment
    print(x)
    return x + 1
"""
    # Same code, but with different comments, extra whitespace, and docstring added!
    code2 = """
def process_data(x: int):
    \"\"\"This is a docstring.\"\"\"

    print(x)

    # Completely different comment
    return x + 1
"""
    tmpdir = tempfile.mkdtemp()
    try:
         fpath = os.path.join(tmpdir, "service.py")
         with open(fpath, "w", encoding="utf-8") as f:
              f.write(code1)
              
         detector = CodeDriftDetector(tmpdir)
         h1 = detector.compute_file_hash(fpath)
         
         with open(fpath, "w", encoding="utf-8") as f:
              f.write(code2)
              
         h2 = detector.compute_file_hash(fpath)
         
         import ast
         from agent_ops_cockpit.ops.architecture.drift import ASTStructuralHasher
         tree1 = ast.parse(code1)
         hasher1 = ASTStructuralHasher()
         hasher1.visit(tree1)
         
         tree2 = ast.parse(code2)
         hasher2 = ASTStructuralHasher()
         hasher2.visit(tree2)
         
         print("\nTOKENS 1:", "".join(hasher1.structural_tokens))
         print("\nTOKENS 2:", "".join(hasher2.structural_tokens))
         
         assert h1 is not None
         assert h2 is not None
         # Should be IDENTICAL hashes because structure didn't drift!
         assert h1 == h2
         
         # Now, modify the ACTUAL logic!
         code3 = """
def process_data(x: int):
    print(x)
    return x + 2 # Logic drifted!
"""
         with open(fpath, "w", encoding="utf-8") as f:
              f.write(code3)
              
         h3 = detector.compute_file_hash(fpath)
         assert h3 != h1

    finally:
         shutil.rmtree(tmpdir)


def test_drift_detector_snapshot_and_detect():
    tmpdir = tempfile.mkdtemp()
    try:
         os.makedirs(os.path.join(tmpdir, "src"))
         fpath1 = os.path.join(tmpdir, "src", "app.py")
         with open(fpath1, "w", encoding="utf-8") as f:
              f.write("a = 1")
              
         detector = CodeDriftDetector(tmpdir)
         detector.save_attestation(["src/app.py"])
         
         # Detect - should be ZERO drift!
         drift = detector.detect_drift()
         assert len(drift) == 0
         
         # Modify the code
         with open(fpath1, "w", encoding="utf-8") as f:
              f.write("a = 2")
              
         drift2 = detector.detect_drift()
         assert "src/app.py" in drift2
         assert drift2["src/app.py"] == "drifted"
         
         # Delete the file
         os.remove(fpath1)
         drift3 = detector.detect_drift()
         assert "src/app.py" in drift3
         assert drift3["src/app.py"] == "missing"

    finally:
         shutil.rmtree(tmpdir)
