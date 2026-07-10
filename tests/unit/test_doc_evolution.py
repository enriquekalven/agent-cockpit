"""Unit tests for the DocEvolutionEngine ground-truth parsing."""
import os
import shutil
import tempfile
import pytest
from agent_ops_cockpit.ops.architecture.doc_evolution import DocEvolutionEngine


def test_extract_current_cli_commands():
    tmpdir = tempfile.mkdtemp()
    try:
         os.makedirs(os.path.join(tmpdir, "src", "agent_ops_cockpit", "cli"))
         main_py_code = """
@app.command("search")
def search_node(): pass

@context_app.command("build")
def build_node(): pass

app.add_typer(context_app, name="context")
app.add_typer(fleet_app, name="fleet")
"""
         with open(os.path.join(tmpdir, "src", "agent_ops_cockpit", "cli", "main.py"), "w", encoding="utf-8") as f:
              f.write(main_py_code)
              
         engine = DocEvolutionEngine(tmpdir)
         commands = engine.extract_current_cli_commands()
         
         assert "cockpit context" in commands
         assert "cockpit fleet" in commands
         assert "Command: search" in commands
         assert "Command: build" in commands
    finally:
         shutil.rmtree(tmpdir)
