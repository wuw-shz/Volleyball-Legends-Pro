# Volleyball Legends Pro v1.0

Volleyball Legends Pro is a specialized Roblox automation tool was created to help with Roblox [Volleyball Legends](https://www.roblox.com/games/73956553001240/Volleyball-Legends) mechanics. It offers pixel-perfect timing for spikes, jump sets, and serves.

## Features

- **Real-time pixel detection** for precise timing of serves and tosses
- **Multiple serve modes**: Normal, Advanced, and Skill
- **Overlay visualization** that displays a center line and current serve mode
- **Keyboard and mouse macros** for various volleyball actions:
  - Toss and serve automation
  - Jump set assistance
  - Jump spike timing
  - Reset Character functionality

## Requirements

- **Windows OS**
- **1920x1080** screen resolution
- **Sanu** or another style (Recommended **Sanu** style)

## Usage

1. **Download** the latest release from the [GitHub Releases page](https://github.com/wuw-shz/Volleyball-Legends-Pro/releases)
2. **Extract** the zip file to a location of your choice
3. **Run** `VolleyballLegendsPro.exe` from the extracted folder
4. The application will automatically detect the Roblox window and overlay its interface
5. Use keyboard shortcuts to activate different macros

### Macro Controls

| Action | Key/Button | Description |
|--------|------------|-------------|
| Cycle Serve Mode | Z | Switch between Normal, Advanced, and Skill serve modes |
| Reset Serve State (USELESS) | F1 | Reset the serve state variables |
| Reset Character | F4 | Execute the reset macro |
| Toss | Left Mouse Button | When serving is active, triggers the toss action |
| Jump Set | Mouse Button X1 (Side Button) | Executes the jump set macro |
| Jump Spike | Mouse Button X2 (Side Button) | Executes the jump spike macro |

The application automatically detects when to serve based on pixel color detection in the Roblox window. When the correct pixel color is detected during serving, the system will automatically trigger the serve action with precise timing.

## Components

The project is structured into several key components:

#### Core Components
- [**main.py**](./main.py) - Main application entry point that starts all necessary processes
- [**controller.py**](./controller.py) - Keyboard and mouse controller for simulating user input
- [**WASD.py**](./WASD.py) - Movement controls

#### Detection
- [**Detection.exe**](./src/detection/) - C++ application that performs pixel-based detection of game state
- Monitors specific screen regions to detect serve opportunities

#### Overlay
- [**Overlay.exe**](./src/overlay/) - C++ application that provides visual feedback over the Roblox window
- Shows a center line and current serve mode status

#### Macros
- [**serves.py**](./src/macros/serves.py) - Handles different serve types ([Normal](./src/macros/serve/normal.py), [Advanced](./src/macros/serve/advanced.py), [Skill](./src/macros/serve/skill.py))
- [**jumpset.py**](./src/macros/jumpset.py) - Manages jump set mechanics
- [**jumpspike.py**](./src/macros/jumpspike.py) - Controls jump spike timing and execution
- [**resets.py**](./src/macros//resets.py) - Resets player state

#### Shared Memory
- [**sharedMemory.py**](./src/sharedMemory/SharedMemory.py) <-> [**SharedMemory.cpp**](./src/sharedMemory/SharedMemory.cpp)
- Used for inter-process communication between Python and C++ components

## Notes

- Designed specifically for Roblox [Volleyball Legends](https://www.roblox.com/games/73956553001240/Volleyball-Legends)
- Automatically activates when the Roblox window is in focus
- Uses pixel color detection for timing critical actions

## Disclaimer

This tool is for educational purposes only. Use of automation tools may violate Roblox's terms of service. Use at your own risk. 