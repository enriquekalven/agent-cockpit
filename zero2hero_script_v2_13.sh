#!/bin/bash
set -e
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:./node_modules/.bin:$PATH"

echo "Running Phase 1..."
uv sync --upgrade
npm install
PYTHONPATH=src uv run cockpit fleet watch || echo "Fleet watch flagged changes. Continuing..."
PYTHONPATH=src uv run cockpit sys version
grep version pyproject.toml
uv --version
npm --version

echo "Running Phase 2..."
PYTHONPATH=src:. uv run pytest
PYTHONPATH=src uv run cockpit certify

echo "Running Phase 3..."
python3 scripts/sync_docs.py || true
npm run build
firebase deploy --only hosting
uv build

echo "Tagging & Pushing..."
git add .
git commit -m "chore: release v2.0.13" || echo "No changes to commit"
git push origin main || echo "Nothing to push"
git tag v2.0.13 || echo "Tag already exists"
git push origin main --tags

echo "Publishing to PyPI..."
if [ -z "$PYPI_TOKEN" ]; then
  echo "Error: PYPI_TOKEN not set!"
  exit 1
fi
uv publish --token $PYPI_TOKEN

echo "✅ zero2hero complete!"
