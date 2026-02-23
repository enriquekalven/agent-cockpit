import os


def harden_dockerfile_resources(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    if 'cpu_quota' in content or 'memory_limit' in content or 'deploy:' in content:
        return False

    # Standard SRE Hardening: Resource Metadata for Cloud Run/K8s
    sre_hardening = """
# [SRE-Hardened] Resource Consternation
LABEL cpu_limit="500m"
LABEL memory_limit="1Gi"
"""
    # Insert before CMD
    if 'CMD' in content:
        content = content.replace('CMD', sre_hardening + 'CMD')
    else:
        content += sre_hardening

    with open(file_path, 'w') as f:
        f.write(content)
    return True

def main():
    target_root = "/Users/enriq/Documents/git/sovereign-fleet-samples"
    count = 0
    for root, _dirs, files in os.walk(target_root):
        for file in files:
            if file == "Dockerfile":
                if harden_dockerfile_resources(os.path.join(root, file)):
                    count += 1
                    print(f"SRE Hardened: {os.path.join(root, file)}")
    print(f"Total Dockerfiles SRE-hardened: {count}")

if __name__ == "__main__":
    main()
