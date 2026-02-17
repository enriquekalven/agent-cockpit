import os
import re

def fix_mcp_schema(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    if 'FunctionTool' not in content:
        # Check if it's using raw functions in Agent(tools=[...])
        if 'Agent(' in content and 'tools=[' in content:
            # Wrap tools with FunctionTool and confirmation
            # This is complex to regex perfectly, but let's try a heuristic
             content = re.sub(
                 r'tools=\[(.*?)\]',
                 r'tools=[FunctionTool(\1, require_confirmation=True)]',
                 content
             )
             if 'from google.adk.tools import FunctionTool' not in content:
                 content = "from google.adk.tools import FunctionTool\n" + content
             
             with open(file_path, 'w') as f:
                 f.write(content)
             return True
    return False

def main():
    target_root = "/Users/enriq/Documents/git/sovereign-fleet-samples"
    count = 0
    for root, dirs, files in os.walk(target_root):
        for file in files:
            if file == "agent.py":
                if fix_mcp_schema(os.path.join(root, file)):
                    count += 1
                    print(f"MCP Schema Fixed: {os.path.join(root, file)}")
    print(f"Total agents with hardened MCP schema: {count}")

if __name__ == "__main__":
    main()
