from tenacity import retry, wait_exponential, stop_after_attempt
from tenacity import retry, wait_exponential, stop_after_attempt
from tenacity import retry, wait_exponential, stop_after_attempt
import pytest
import os
import re

def get_repo_root():
    """Get the absolute path to the repository root."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def test_mobile_media_queries_exist():
    """Verify that mobile media queries exist in the frontend files."""
    root = get_repo_root()
    css_path = os.path.join(root, 'src/index.css')
    with open(css_path, 'r') as f:
        content = f.read()
    assert '@media (max-width: 768px)' in content
    assert 'flex-direction: column' in content

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def test_component_responsive_styles():
    """Verify that key components have responsive style blocks."""
    root = get_repo_root()
    files_to_check = ['src/docs/DocLayout.tsx', 'src/components/Home.tsx', 'src/components/ReportSamples.tsx', 'src/components/OperationalJourneys.tsx', 'src/docs/DocHome.tsx']
    media_query_pattern = re.compile('@media\\s*\\(max-width:\\s*768px\\)')
    for rel_path in files_to_check:
        file_path = os.path.join(root, rel_path)
        assert os.path.exists(file_path), f'{file_path} does not exist'
        with open(file_path, 'r') as f:
            content = f.read()
        assert media_query_pattern.search(content), f'Missing mobile media query in {rel_path}'

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def test_mobile_navigation_enabled():
    """Verify that mobile navigation toggle is present in DocLayout."""
    root = get_repo_root()
    layout_path = os.path.join(root, 'src/docs/DocLayout.tsx')
    with open(layout_path, 'r') as f:
        content = f.read()
    assert 'mobile-toggle' in content
    assert 'Menu' in content
    assert 'X' in content
    assert 'isSidebarOpen' in content
if __name__ == '__main__':
    pytest.main([__file__])