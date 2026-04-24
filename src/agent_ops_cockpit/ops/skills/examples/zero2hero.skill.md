# Zero2Hero: Autonomous Release Skill

| name | description | category | revision | tags |
| :--- | :--- | :--- | :--- | :--- |
| zero2hero-release | Automates the end-to-end productionization and release of the AgentOps Cockpit | release | 1 | release,automation,deployment,pypi,firebase |

## Rationalizations

| Excuse | Rebuttal |
| :--- | :--- |
| Manual releases are fine for small updates. | Manual releases are error-prone and frequently skip critical verification steps. Automation ensures consistent quality gates are met every time. |
| Running the full regression suite takes too long. | Skipping tests leads to production regressions. The test suite must be optimized and run in full before any release. |
| I can just update the version in one place. | Version drift between `pyproject.toml`, `package.json`, and source code causes deployment failures. They must be synchronized. |

## Verification

- Verify that `agentops-cockpit sys version` matches the version in `pyproject.toml`.
- Verify that the Autonomous Score is > 90 before proceeding to deployment.
- Verify that the Firebase Hosting deployment completes without errors.
- Verify that the PyPI package is successfully published.

## Instructions for Release Execution

When executing the Zero2Hero release workflow, follow these phase-gate instructions:

### Phase 1: Preparation & Intelligence Sync
1. **Upgrade Dependencies**: Run `uv sync --upgrade` and `npm install`.
2. **Version Alignment**: Ensure `pyproject.toml`, `package.json`, and `config.py` version strings match.
3. **Auth Check**: Verify `firebase login` status and that `PYPI_TOKEN` is available.
4. **Doc Sync**: Run `python3 scripts/sync_docs.py` to update public guides.

### Phase 2: Structural Verification (The Build Gates)
5. **Clean**: Remove `dist/` and `build/` directories.
6. **Lint**: Run `uv run ruff check .` and `npm run lint`.
7. **Core Mission Audit**: Run `pytest src/agent_ops_cockpit/tests/test_capabilities_gate.py`.
8. **Certification**: Run `agentops-cockpit certify` and ensure score > 90.
9. **Full Regression**: Run `PYTHONPATH=src:. uv run pytest`.

### Phase 3: Global Deployment & Publishing
10. **Build Assets**: Run `npm run build`.
11. **Deploy Web**: Run `firebase deploy --only hosting`.
12. **Build Package**: Run `uv build`.
13. **Tag Release**: Commit changes, create git tag, and push to GitHub.
14. **Publish**: Run `uv publish` to push to PyPI.

### Phase 4: Post-Release Verification
15. **Live Check**: Verify the live site and that the new package version is installable.

## Promptfoo Integration

This skill embeds tests to verify that the release process respects the version gate:

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
        "prompt": "Simulate a release where the version in pyproject.toml does not match package.json."
      },
      "assert": [
        {
          "type": "contains",
          "value": "Version mismatch",
          "metric": "Version Alignment Gate"
        }
      ]
    }
  ]
}
```
