import os
import sys
import subprocess
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "../.."))
sys.path.insert(0, project_root)

from version import VERSION_FULL

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True)
    return result.returncode

def clean_directories():
    print("Cleaning previous builds...")
    
    paths_to_clean = [
        os.path.join(project_root, "dist/VolleyballLegendsPro"),
        os.path.join(project_root, "build/volleyball_legends_pro")
    ]
    
    for path in paths_to_clean:
        if os.path.exists(path):
            try:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    time.sleep(1)
                    if sys.platform == 'win32':
                        run_command(f'rmdir /s /q "{path}"')
                    else:
                        run_command(f'rm -rf "{path}"')
                    
                    print(f"Removed {path}")
            except Exception as e:
                print(f"Warning: Could not clean {path}: {e}")

def build_application():
    print("\nPreparing build...")
    
    print("Updating documentation with current version...")
    update_script = os.path.join(script_dir, "update_readme_version.py")
    if run_command(f"python \"{update_script}\"") != 0:
        print("Warning: Failed to update README.md version")
        return False
    
    print("Creating application icon...")
    app_icon_script = os.path.join(script_dir, "create_icon.py")
    if run_command(f"python \"{app_icon_script}\"") != 0:
        print("Error: Failed to create application icon.")
        return False
    
    print("Generating version information...")
    generate_script = os.path.join(script_dir, "generate_version_info.py")
    if run_command(f"python \"{generate_script}\"") != 0:
        print("Failed to generate version information")
        return False
    
    print("\nBuilding application...")
    spec_file = os.path.join(script_dir, "volleyball_legends_pro.spec")
    if run_command(f"pyinstaller \"{spec_file}\" --noconfirm") != 0:
        print("Build failed")
        return False
    
    print("\nBuild completed successfully!")
    return True

def create_release():
    print("\nCreating release package...")
    
    time.sleep(2)
    
    dist_dir = os.path.join(project_root, "dist/VolleyballLegendsPro")
    if not os.path.exists(dist_dir):
        print("Error: Build folder does not exist.")
        return False
    
    release_script = os.path.join(script_dir, "make_release.py")
    if run_command(f"python \"{release_script}\"") != 0:
        print("Release packaging failed")
        return False
    
    print(f"\nRelease v{VERSION_FULL} created successfully!")
    return True

if __name__ == "__main__":
    os.chdir(project_root)
    
    print(f"=== Volleyball Legends Pro Build Script v{VERSION_FULL} ===\n")
    print(f"Project root: {project_root}")
    print(f"Build tools: {script_dir}\n")
    
    clean_directories()
    
    if build_application():
        create_release()
    
    print("\nBuild process completed.")
    input("Press Enter to exit...") 