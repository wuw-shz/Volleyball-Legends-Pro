import os
import sys
import subprocess
import time
from version import VERSION_FULL

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True)
    return result.returncode

def clean_directories():
    print("Cleaning previous builds...")
    
    paths_to_clean = [
        "dist/VolleyballLegendsPro",
        "build/volleyball_legends_pro"
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
    
    print("Generating version information...")
    if run_command("python generate_version_info.py") != 0:
        print("Failed to generate version information")
        return False
    
    print("\nBuilding application...")
    if run_command("pyinstaller volleyball_legends_pro.spec --noconfirm") != 0:
        print("Build failed")
        return False
    
    print("\nBuild completed successfully!")
    return True

def create_release():
    print("\nCreating release package...")
    
    time.sleep(2)
    
    if not os.path.exists("dist/VolleyballLegendsPro"):
        print("Error: Build folder does not exist.")
        return False
    
    if run_command("python make_release.py") != 0:
        print("Release packaging failed")
        return False
    
    print(f"\nRelease v{VERSION_FULL} created successfully!")
    return True

if __name__ == "__main__":
    print(f"=== Volleyball Legends Pro Build Script v{VERSION_FULL} ===\n")
    
    clean_directories()
    
    if build_application():
        create_release()
    
    print("\nBuild process completed.")
    input("Press Enter to exit...") 