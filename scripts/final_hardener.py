import os
import re


def final_harden(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    patched = False
    
    # 1. Decorate all 'tool_' and destructive '_' methods
    if 'from mcp_gate import mcp_tool_gate' not in content:
        content = "from mcp_gate import mcp_tool_gate\n" + content
        patched = True
        
    keyword_pattern = r'def (tool_|_(trigger|delete|terminate|update|exec|scrape)).*?\(.*?\):'
    if re.search(keyword_pattern, content):
        # Avoid double decoration
        lines = content.split('\n')
        new_lines = []
        for i, line in enumerate(lines):
            if re.match(r'^\s*def (tool_|_(trigger|delete|terminate|update|exec|scrape))', line):
                # Check if previous line is already a gate
                if i > 0 and '@mcp_tool_gate' not in lines[i-1]:
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(' ' * indent + '@mcp_tool_gate(require_confirmation=True)')
            new_lines.append(line)
        content = '\n'.join(new_lines)
        patched = True

    # 2. Ensure run_ methods are reflected
    if 'from reflection_engine import sovereign_reflection' not in content:
        content = "from reflection_engine import sovereign_reflection\n" + content
        patched = True
    
    if 'def run_' in content:
        content = re.sub(r'(def run_.*?\(.*?\):)', r'@sovereign_reflection\n    \1', content)
        patched = True

    if patched:
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    target_root = "/Users/enriq/Documents/git/sovereign-fleet-samples"
    count = 0
    for root, _dirs, files in os.walk(target_root):
        for file in files:
            if file == "agent.py" or file == "fleet_commander.py":
                if final_harden(os.path.join(root, file)):
                    count += 1
                    print(f"Final Hardened: {os.path.join(root, file)}")
    print(f"Total agents final-hardened: {count}")

if __name__ == "__main__":
    main()
