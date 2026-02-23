import os


def inject_logging(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    if 'import logging' in content:
        return False

    # Inject logging setup
    logging_setup = """
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
"""
    content = logging_setup + content
    
    # Inject an info log in main/functions
    if 'def main():' in content:
         content = content.replace('def main():', "def main():\n    logger.info('🚀 Sovereign Agent Initialized')")
    elif 'class ' in content:
         # Find first method and inject
         import re
         content = re.sub(r'(def .*?\(.*?\):)', r'\1\n        logger.info("Executing sovereign logic")', content, count=1)

    with open(file_path, 'w') as f:
        f.write(content)
    return True

def main():
    target_root = "/Users/enriq/Documents/git/sovereign-fleet-samples"
    count = 0
    for root, _dirs, files in os.walk(target_root):
        for file in files:
            if file.endswith(".py"):
                if inject_logging(os.path.join(root, file)):
                    count += 1
                    print(f"Logged: {os.path.join(root, file)}")
    print(f"Total files logged: {count}")

if __name__ == "__main__":
    main()
