import os
import re

def harden_tsx(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    if 'surfaceId' in content:
        return False

    # 1. Add surfaceId to Props interface
    content = re.sub(
        r'interface\s+(\w+)Props\s*\{',
        r'interface \1Props {\n  surfaceId?: string;',
        content
    )

    # 2. Extract surfaceId in function arguments
    # Supports: export function Name({ a, b ... }) or function Name({ a, b ... })
    content = re.sub(
        r'(export\s+)?function\s+(\w+)\s*\(\{\s*([^}]+)\s*\}\s*:\s*\2Props\)',
        r'\1function \2({ surfaceId, \3 }: \2Props)',
        content
    )

    # 3. Inject id={surfaceId} into the first <div> or common root element
    content = re.sub(
        r'return\s*\(\s*<div\s+([^>]*?)>',
        r'return (\n    <div id={surfaceId} \1>',
        content,
        count=1
    )

    # 4. Inject Skeleton/Thinking if "Page" or "View"
    if "Page" in file_path or "View" in file_path:
        if 'isLoading' in content and 'Skeleton' not in content:
            content = content.replace('isLoading &&', 'isLoading && /* UI: Thinking Feedback */ <div className="animate-pulse bg-gray-200 h-4 w-full rounded" /> &&')

    # 5. Inject HITL Gating if "Action" or "Tool"
    if "Action" in file_path or "Tool" in file_path:
        if 'onClick' in content and 'confirm' not in content:
            content = content.replace('onClick={', 'onClick={(e) => { if(!confirm("Sovereign Gate: Approve high-stakes action?")) return; ')

    with open(file_path, 'w') as f:
        f.write(content)
    return True

def main():
    target_root = "/Users/enriq/Documents/git/adk-samples"
    modified_count = 0
    for root, dirs, files in os.walk(target_root):
        if any(d in root for d in [".venv", "node_modules", ".git"]):
            continue
        for file in files:
            if file.endswith(".tsx") and "ui/" not in root:
                if harden_tsx(os.path.join(root, file)):
                    modified_count += 1
                    print(f"Hardened: {file}")

    print(f"Total TSX files hardened for A2UI: {modified_count}")

if __name__ == "__main__":
    main()
