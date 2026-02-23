import os


def fix_dockerfile(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    if 'USER appuser' in content:
        return False

    # Standard hardening: Add appuser
    hardening = """
# [Sovereign-Hardened] Non-Root User
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
USER appuser
"""
    # Inject before the final CMD or ENTRYPOINT or at the end
    if 'CMD' in content:
        content = content.replace('CMD', hardening + 'CMD')
    elif 'ENTRYPOINT' in content:
        content = content.replace('ENTRYPOINT', hardening + 'ENTRYPOINT')
    else:
        content += hardening

    with open(file_path, 'w') as f:
        f.write(content)
    return True

def main():
    target_root = "/Users/enriq/Documents/git/sovereign-fleet-samples"
    count = 0
    for root, _dirs, files in os.walk(target_root):
        for file in files:
            if file == "Dockerfile":
                if fix_dockerfile(os.path.join(root, file)):
                    count += 1
                    print(f"Hardened: {os.path.join(root, file)}")
    print(f"Total Dockerfiles hardened: {count}")

if __name__ == "__main__":
    main()
