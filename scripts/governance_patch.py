import os

def inject_governance(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    if 'governance_portal' in content:
        return False

    # Inject import
    content = "from governance_portal import Governance\n" + content
    
    # Inject call in main or at module level
    if 'def main():' in content:
        content = content.replace('def main():', 'def main():\n    Governance.enforce_runtime_security()')
    elif 'if __name__ == "__main__":' in content:
        content = content.replace('if __name__ == "__main__":', 'if __name__ == "__main__":\n    Governance.enforce_runtime_security()')
    else:
        # Fallback to module level
        content += "\nGovernance.enforce_runtime_security()\n"

    with open(file_path, 'w') as f:
        f.write(content)
    return True

def main():
    target_root = "/Users/enriq/Documents/git/sovereign-fleet-samples"
    count = 0
    for root, dirs, files in os.walk(target_root):
        for file in files:
            if file == "agent.py":
                if inject_governance(os.path.join(root, file)):
                    count += 1
                    print(f"Governed: {os.path.join(root, file)}")
    print(f"Total agents governed: {count}")

if __name__ == "__main__":
    main()
