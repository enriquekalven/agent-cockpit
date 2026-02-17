import os

files_to_fix = []
with open('files_to_fix.txt', 'r') as f:
    files_to_fix = [line.strip() for line in f if line.strip()]

versions_to_replace = {
    '1.6.7': '1.8.4',
    '1.6.6': '1.8.4',
    '1.3.5': '1.8.4'
}

for file_path in files_to_fix:
    if not os.path.exists(file_path):
        continue
    if any(file_path.endswith(ext) for ext in ['.pyc', '.png', '.exe', '.gz', '.zip', '.pyo', '.so', '.dylib']):
        continue
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        for old, new in versions_to_replace.items():
            content = content.replace(old, new)
            
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
