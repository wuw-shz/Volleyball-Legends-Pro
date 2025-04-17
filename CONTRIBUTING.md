# Contributing to Volleyball Legends Pro

Thank you for your interest in contributing to Volleyball Legends Pro! This document provides guidelines to help you get started.

## Development Requirements

- **Python 3.8+** - Python 3.8 or newer is required
- **Windows 10/11** - Windows operating system
- **1920x1080 resolution** - For pixel-perfect detection
- **C++ Build Tools** - For building the C++ components (if modifying [detection](./src/detection/) or [overlay](./src/overlay/))
  - Visual Studio 2019+ with C++ Desktop development workload or
  - MinGW-w64 with GCC 8.1+
- **Git** - For version control

## Development Setup

1. **Clone the repository**
   ```shell
   git clone https://github.com/wuw-shz/Volleyball-Legends-Pro.git
   cd Volleyball-Legends-Pro
   ```

2. **Set up development environment**
   ```shell
   pip install -r requirements.txt
   ```

   Key dependencies include:
   - **numpy** - For numerical operations
   - **pynput** - For keyboard/mouse input handling
   - **pyinstaller** - For building the executable

3. **Run the application**
   ```shell
   python main.py
   ```

4. **(Optional) Install C++ dependencies** if modifying detection or overlay components:
   - Install Visual Studio with C++ Desktop Development workload
   - Open the solution files in the src/detection and src/overlay directories

## Project Structure

- **assets/** - Icons and other assets
- **src/** - Source code
  - **detection/** - C++ code for pixel detection
  - **overlay/** - C++ code for visual overlay
  - **macros/** - Game mechanics macros
    - **serve/** - Different serve types (Normal, Advanced, Skill)
    - **jumpset.py** - Jump set mechanics
    - **jumpspike.py** - Jump spike execution
    - **resets.py** - Character reset functions
  - **listeners/** - Input event listeners
  - **ui/** - User interface components
  - **sharedMemory/** - Inter-process communication
- **tools/** - Development tools
  - **build/** - Build and packaging scripts
- Main files:
  - **main.py** - Application entry point
  - **controller.py** - Input controller
  - **WASD.py** - Movement controls
  - **version.py** - Version information

## Development Workflow

1. **Create a new branch** for your feature or bugfix
   ```shell
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and test thoroughly
   - Follow existing code style
   - Test with different screen resolutions if possible
   - Update documentation as needed

3. **Run in development mode** to verify changes
   ```shell
   python main.py
   ```

4. **Build and test** the executable
   ```shell
   ./"! build.bat"
   ```

5. **Commit your changes** with clear messages
   ```shell
   git add .
   git commit -m "Add feature: your feature description"
   ```

6. **Submit a pull request** with a clear description of changes

## Versioning

When updating the version:

1. Modify `version.py` with the new version number:
   ```python
   VERSION_MAJOR = 1  # Major version (breaking changes)
   VERSION_MINOR = 0  # Minor version (new features)
   VERSION_PATCH = 0  # Patch version (bug fixes)
   
   VERSION_FULL = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
   RELEASE_NAME = "Volleyball Legends Pro"
   ```

2. Run `! build.bat` to update version information and build
   ```shell
   ./"! build.bat"
   ```

## Code Style Guidelines

- Use descriptive variable and function names
- Follow PEP 8 guidelines for Python code
- Add comments for complex logic
- Keep functions small and focused
- Write docstrings for public functions
- Use consistent indentation (4 spaces for Python)
- Organize imports alphabetically

## Testing

Test your changes with:
- Different Roblox character styles (especially Sanu)
- Various serve/spike/set situations
- Edge cases (e.g., UI scaling, window resizing)
- Different match scenarios
- Test in both development and compiled modes

## Documentation

When making significant changes:
- Update docstrings for modified functions
- Update README.md if user-facing features change
- Add comments to explain complex logic
- Update CONTRIBUTING.md if development processes change

## Submitting Pull Requests

1. Ensure all tests pass
2. Update documentation if needed
3. Include a clear title and description
4. Reference any related issues
5. Be responsive to feedback and requests for changes

Thank you for contributing! 