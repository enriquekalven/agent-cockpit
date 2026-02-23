import os


def cleanup_syntax(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Fix stray commas from bad regex
    new_content = content.replace("(,", "(")
    new_content = new_content.replace("( ,", "(")
    
    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        return True
    return False

def main():
    target_root = "/Users/enriq/Documents/git/sovereign-fleet-samples"
    count = 0
    for root, _dirs, files in os.walk(target_root):
        for file in files:
            if file.endswith(".py"):
                if cleanup_syntax(os.path.join(root, file)):
                    count += 1
                    print(f"Cleaned: {os.path.join(root, file)}")
    print(f"Total files cleaned: {count}")

if __name__ == "__main__":
    main()
