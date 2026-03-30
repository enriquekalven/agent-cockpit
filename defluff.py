import os, re

dir_to_scan = '.'

# Define replacement mappings with case sensitivity considerations
replacements = [
    (re.compile(r'\bSovereign\b', re.IGNORECASE), 'Autonomous'),
    (re.compile(r'\bSovereignty\b', re.IGNORECASE), 'Autonomy'),
    (re.compile(r'\bhive mind\b', re.IGNORECASE), 'distributed cache'),
    (re.compile(r'\bHive Mind\b', re.IGNORECASE), 'Distributed Cache'),
    (re.compile(r'\bAgentic Trinity\b', re.IGNORECASE), 'Governance Framework'),
    (re.compile(r'\bSentinel Oversight\b', re.IGNORECASE), 'System Oversight'),
    (re.compile(r'\bSME Judgment\b', re.IGNORECASE), 'Domain Evaluation'),
    (re.compile(r'\bMaster SME Personas\b', re.IGNORECASE), 'Specialized Auditors'),
    (re.compile(r'\bMaster SME\b', re.IGNORECASE), 'Specialized Auditor'),
    (re.compile(r'\bCognitive Load\b', re.IGNORECASE), 'Execution Overhead'),
    (re.compile(r'\bCognitive\b', re.IGNORECASE), 'Reasoning'),
    (re.compile(r'\bAI Magic\b', re.IGNORECASE), 'Automation'),
]

for root, _, fs in os.walk(dir_to_scan):
    if '.git' in root or '.gemini' in root or 'node_modules' in root or 'dist' in root or 'build' in root or 'dogfood_repos' in root:
        continue
    for f in fs:
        if f.endswith(('.md', '.tsx', '.ts', '.html', '.yml', '.yaml', '.py', '.json', '.txt', '.sql', '.sh')):
            p = os.path.join(root, f)
            with open(p, 'r') as file:
                try:
                    content = file.read()
                except UnicodeDecodeError:
                    continue
            
            orig_content = content
            for pattern, replacement in replacements:
                 content = pattern.sub(replacement, content)
            
            if content != orig_content:
                with open(p, 'w') as file:
                    file.write(content)
                print(f"Defluffed: {p}")

print("Defluff complete.")
