import os
import re

files = [
    'src/agent_ops_cockpit/ops/arch_review.py',
    'src/agent_ops_cockpit/ops/ui_auditor.py',
    'src/agent_ops_cockpit/ops/secret_scanner.py',
    'src/agent_ops_cockpit/ops/rag_audit.py'
]

for fpath in files:
    if not os.path.exists(fpath):
        print(f"⚠️  {fpath} does not exist.")
        continue

    with open(fpath, 'r') as f:
        content = f.read()

    # 1. Add escape import if not there
    if 'from rich.markup import escape' not in content:
        # Find where to insert (after imports or top)
        content = "from rich.markup import escape\n" + content

    # 2. Match console.print(f"ACTION: ...") where string ends at the close of parenthesis
    new_content = re.sub(
        r'console\.print\(\s*(f["\']ACTION:.*?["\'])\s*\)',
        r'console.print(escape(\1))',
        content
    )
    
    # 3. Handle single quote variant specifically if there are double brackets
    if new_content == content:
        # Retry with a more flexible spacing regex
        new_content = re.sub(
            r'console\.print\(\s*(f[\'"].*?ACTION:.*?[\'"])\s*\)',
            r'console.print(escape(\1))',
            content
        )

    if new_content != content:
        with open(fpath, 'w') as f:
            f.write(new_content)
        print(f"✅ Escaped markings in {fpath}")
    else:
         print(f"⚠️  No modifications made for {fpath}")
