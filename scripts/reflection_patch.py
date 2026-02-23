import os


def inject_reflection(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    if 'sovereign_reflection' in content:
        return False

    # Inject import
    content = "from reflection_engine import sovereign_reflection\n" + content
    
    # Decorate main runner function or Agent instance
    if 'def run(' in content:
         content = content.replace('def run(', '@sovereign_reflection\ndef run(')
    elif 'def main():' in content:
         content = content.replace('def main():', '@sovereign_reflection\ndef main():')
    
    with open(file_path, 'w') as f:
        f.write(content)
    return True

def main():
    target_root = "/Users/enriq/Documents/git/sovereign-fleet-samples"
    count = 0
    for root, _dirs, files in os.walk(target_root):
        for file in files:
            if file == "agent.py" or file == "fleet_commander.py":
                if inject_reflection(os.path.join(root, file)):
                    count += 1
                    print(f"Reflected: {os.path.join(root, file)}")
    print(f"Total agents reflected: {count}")

if __name__ == "__main__":
    main()
