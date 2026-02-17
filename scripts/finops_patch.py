import os
import re

def inject_caching(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    if 'context_cache_config' in content:
        return False

    # Heuristic: Find LlmAgent or Agent instantiation
    # Pattern: Agent( ... ) or LlmAgent( ... )
    if 'Agent(' in content or 'LlmAgent(' in content:
        # Pattern to find the closing parenthesis of the Agent call and inject the config
        # This is a bit complex for a regex, let's try a simpler replacement if it's following a common pattern
        new_config = '    context_cache_config={"ttl_seconds": 600, "min_tokens": 2048},\n'
        
        # Inject before the closing bracket if it's multi-line
        if ')' in content:
             content = re.sub(
                r'((Agent|LlmAgent)\(.*?)\)',
                r'\1,\n' + new_config + '    )',
                content,
                flags=re.DOTALL
            )
             with open(file_path, 'w') as f:
                f.write(content)
             return True
    return False

def main():
    target_root = "/Users/enriq/Documents/git/sovereign-fleet-samples"
    count = 0
    for root, dirs, files in os.walk(target_root):
        for file in files:
            if file.endswith(".py"):
                if inject_caching(os.path.join(root, file)):
                    count += 1
                    print(f"Cached: {file}")
    print(f"Total agents cached: {count}")

if __name__ == "__main__":
    main()
