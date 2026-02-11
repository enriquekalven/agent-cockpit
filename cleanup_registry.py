import json
import os

reg_path = '.cockpit/gemini_enterprise_registry.json'
if os.path.exists(reg_path):
    with open(reg_path, 'r') as f:
        content = f.read()
    
    # Cleanup formatting
    content = content.replace('}{', '}\n{')
    lines = content.strip().split('\n')
    
    new_lines = []
    seen_ids = set()
    for line in lines:
        try:
            data = json.loads(line)
            # If it's a generic 'agent' ID, and we know it's my-super-agent, rename it
            if data.get('id') == 'sovereign-agent' or data.get('id') == 'sovereign-main':
                 # Use the display name or just rename to my-super-agent if it matches the current lab
                 if 'Super Agent' in data.get('display_name', ''):
                      data['id'] = 'sovereign-my-super-agent'
                      data['display_name'] = '🚀 Gemini Enterprise: My Super Agent (ADK)'
            
            if data['id'] not in seen_ids:
                new_lines.append(json.dumps(data))
                seen_ids.add(data['id'])
        except Exception:
            pass
            
    with open(reg_path, 'w') as f:
        f.write('\n'.join(new_lines) + '\n')
    print("✅ Registry cleaned and upgraded.")
