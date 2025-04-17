import os
import zipfile
import datetime
from version import VERSION, RELEASE_NAME

DIST_DIR = "dist/VolleyballLegendsPro"
OUTPUT_DIR = "releases"

def create_readme():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    with open('release_readme.txt', 'r') as f:
        readme_content = f.read()
    
    readme_content = readme_content.replace('{VERSION}', VERSION)
    readme_content = readme_content.replace('{DATE}', date_str)
    
    readme_path = os.path.join(DIST_DIR, 'README.txt')
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    return readme_path

def create_release_package():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    now = datetime.datetime.now()
    zip_filename = f"{OUTPUT_DIR}/{RELEASE_NAME.replace(' ', '')} v{VERSION}.zip"

    if os.path.exists(zip_filename):
        os.remove(zip_filename)

    create_readme()
    
    print(f"Creating release package: {zip_filename}")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(DIST_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, DIST_DIR)
                print(f"Adding: {arcname}")
                zipf.write(file_path, arcname)
    
    print(f"Release package created successfully: {zip_filename}")
    return zip_filename

if __name__ == "__main__":
    if not os.path.exists(DIST_DIR):
        print(f"Error: Build directory {DIST_DIR} not found. Run PyInstaller first.")
        exit(1)
    
    zip_file = create_release_package()
    print(f"Release package is ready at: {zip_file}")