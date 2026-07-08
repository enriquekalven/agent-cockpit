# AST-Aware Dependency Management Skill

| name | description | category | revision | tags |
| :--- | :--- | :--- | :--- | :--- |
| ast-dependency-management | Instructs Cockpit to use AST analysis for targeted dependency installation | optimization | 1 | ast,dependencies,preflight,optimization |

## Rationalizations

| Excuse | Rebuttal |
| :--- | :--- |
| I just run `uv sync` or `pip install -r requirements.txt`. | This installs unneeded packages and wastes time/bandwidth. Use AST to find what is actually imported and install only those. |
| Mapping imports to package names is complex. | Focus on common high-impact libraries (e.g., `vertexai`, `langchain`, `google-genai`) and fallback to standard resolution only when ambiguous. |
| It takes too long to scan all files. | Only scan the core agent files and detected "Brain" files to keep it fast. |

## Verification

- Verify that the AST scan identifies all top-level external imports in the agent files.
- Verify that the dependency installer only invokes installation for packages not already present in the environment.
- Verify that no execution occurs if zero new packages are needed.

## Instructions for Cockpit Execution

When running audits, evolution, or certification, Cockpit should follow these steps for dependency resolution:
1. **Scan**: Walk the AST of all discovered Agent Brain files and Python sources.
2. **Extract**: Collect all `ast.Import` and `ast.ImportFrom` names.
3. **Filter**: Remove standard library modules and local project modules.
4. **Install**: Use `uv add` or `pip install` ONLY for the detected external packages that are missing.

## Promptfoo Integration

This skill embeds tests to verify that the AST dependency manager correctly identifies imports:

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
        "prompt": "Verify that a file containing 'import vertexai' triggers installation of 'google-cloud-aiplatform'."
      },
      "assert": [
        {
          "type": "contains",
          "value": "google-cloud-aiplatform",
          "metric": "Correct Mapping"
        }
      ]
    }
  ]
}
```
