# Build Tools for Volleyball Legends Pro

This directory contains tools for building and packaging Volleyball Legends Pro.

## Files

- **build.py** - Main build script that coordinates all build steps
- **create_icon.py** - Creates the application icon
- **generate_version_info.py** - Generates version info file for the executable
- **make_release.py** - Creates release packages
- **update_readme_version.py** - Updates the README.md with the current version
- **volleyball_legends_pro.spec** - PyInstaller specification file
- **release_readme.txt** - Template for the README.txt included in releases
- **file_version_info.txt** - Generated version info file for embedding in the EXE

## Usage

You should not typically run these scripts directly. Instead, use the build.bat file in the project root:

```
cd [project root]
build.bat
```

## Build Process

The build process:

1. Cleans previous build artifacts
2. Updates version information in the README.md
3. Creates the application icon if it doesn't exist
4. Generates file_version_info.txt for embedding in the executable
5. Runs PyInstaller to compile the application
6. Creates a release package with the compiled executable

## Output

- **dist/VolleyballLegendsPro/** - The compiled application
- **releases/VolleyballLegendsPro_v[VERSION_FULL].zip** - Release package

## Version Handling

The version information is stored in the root `version.py` file:
- VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH - Version components
- VERSION_FULL - Complete version string (X.Y.Z)
- RELEASE_NAME - Product name

All version information is synchronized across:
- Executable file properties
- README.md in project root
- Release package filenames
- Release README.txt 