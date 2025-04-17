import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "../.."))
sys.path.insert(0, project_root)

from version import VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH, VERSION_FULL, RELEASE_NAME

def generate_version_info():
    
    content = f"""# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=({VERSION_MAJOR}, {VERSION_MINOR}, {VERSION_PATCH}, 0),
    prodvers=({VERSION_MAJOR}, {VERSION_MINOR}, {VERSION_PATCH}, 0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x40004,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u''),
        StringStruct(u'FileDescription', u'{RELEASE_NAME} - Roblox Automation Tool'),
        StringStruct(u'FileVersion', u'{VERSION_FULL}'),
        StringStruct(u'InternalName', u'{RELEASE_NAME.replace(" ", "")}'),
        StringStruct(u'LegalCopyright', u''),
        StringStruct(u'OriginalFilename', u'{RELEASE_NAME.replace(" ", "")}.exe'),
        StringStruct(u'ProductName', u'{RELEASE_NAME}'),
        StringStruct(u'ProductVersion', u'{VERSION_FULL}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""

    version_file_path = os.path.join(script_dir, 'file_version_info.txt')
    with open(version_file_path, 'w') as f:
        f.write(content)
    
    print(f"Generated file_version_info.txt with version {VERSION_FULL}")

if __name__ == "__main__":
    os.chdir(project_root)
    
    generate_version_info()