import os

def inject_mcp_gate(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    if 'mcp_tool_gate' in content:
        return False

    # Inject import
    content = "from mcp_gate import mcp_tool_gate\n" + content
    
    # Simple heuristic: decorate any function that looks like a tool (e.g. scrape, update, search, delete)
    import re
    tool_keywords = ["scrape", "update", "search", "delete", "dispatch", "exec"]
    patched = False
    for kw in tool_keywords:
        pattern = r'(def ' + kw + r'.*?\(.*?\):)'
        if re.search(pattern, content):
            content = re.sub(pattern, r'@mcp_tool_gate(require_confirmation=True)\n\1', content)
            patched = True
    
    if patched:
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    target_root = "/Users/enriq/Documents/git/sovereign-fleet-samples"
    count = 0
    for root, dirs, files in os.walk(target_root):
        for file in files:
            if file.endswith(".py") and file != "mcp_gate.py":
                if inject_mcp_gate(os.path.join(root, file)):
                    count += 1
                    print(f"MCP Gated: {os.path.join(root, file)}")
    print(f"Total tools gated: {count}")

if __name__ == "__main__":
    main()
