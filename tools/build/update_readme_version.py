import os
import sys
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "../.."))
sys.path.insert(0, project_root)

from version import VERSION_FULL, RELEASE_NAME

def update_readme_version():
    try:
        readme_path = os.path.join(project_root, 'README.md')
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = re.sub(
            r'^# Volleyball Legends Pro v[\d\.]+',
            f'# {RELEASE_NAME} v{VERSION_FULL}',
            content,
            flags=re.MULTILINE
        )
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"Updated README.md with version {VERSION_FULL}")
        return True
    except Exception as e:
        print(f"Error updating README.md: {e}")
        return False

if __name__ == "__main__":
    os.chdir(project_root)
    
    update_readme_version() 