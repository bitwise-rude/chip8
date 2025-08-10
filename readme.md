# Chip-8 Simulator in Python

This is a Chip-8 simulator written in Python, implementing almost all Chip-8 instructions. It provides a simple but functional way to run and play classic Chip-8 games.

## Features

- Implements most Chip-8 opcodes with accurate instruction handling
- Simple graphical output using Pygame
- Keyboard input mapped to keypad keys
- Includes two built-in playable games:
  - `TAHNK.ch8`
  - `UFO.ch8`
- Modular design with separate files for file loading, interpreter, and display (visuals)

## Project Structure

- `file_manager.py`: Handles loading ROM files into memory
- `main.py`: Entry point to start the simulator and load games
- `interpreter.py`: Contains the main Chip-8 interpreter logic and opcode execution
- `visuals.py`: Manages the display, drawing sprites, and input handling using Pygame

## Usage

Run `main.py` to start the simulator. You can load the included ROMs (`TAHNK.ch8` or `UFO.ch8`) and start playing immediately.

## Next Steps

The next planned step for this project is to explore building other kinds of emulators, broadening the scope beyond Chip-8.

---

Thanks for checking out the project! Feel free to contribute or suggest improvements.

