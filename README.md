# CHIP8Emulator

Modernized Python implementation of a classic Chip-8 interpreter. The project is split between an isolated CPU core (`Chip8`) and a Tkinter powered front-end (`GUI`) so that the emulator logic and presentation stay decoupled.

## Features

- Accurate 35-opcode Chip-8 interpreter with configurable clock speed
- Dedicated timing loop that keeps delay and sound timers stepping at 60 Hz
- Keyboard bridge that maps a standard QWERTY layout onto the Chip-8 hex keypad
- Canvas-based renderer with dynamic scaling and instant ROM reloads
- Simple ROM picker with graceful error handling

## Requirements

- Python 3.10+
- Tkinter (bundled with most desktop Python distributions)

## Running The Emulator

```bash
python application.py
```

The app attempts to boot `ROMs/IBM Logo.ch8` automatically. Use `File → Open ROM...` to select any `.ch8` file, or `File → Reload ROM` to reset the currently loaded program.

## Controls

| Chip-8 | Keyboard |
| --- | --- |
| 1 2 3 C | 1 2 3 4 |
| 4 5 6 D | Q W E R |
| 7 8 9 E | A S D F |
| A 0 B F | Z X C V |

## Architecture

- `chip8emulator.py`: Pure interpreter that handles memory, opcodes, timers, stack, keypad state, and framebuffer updates.
- `GUI.py`: Tkinter frame responsible for drawing the 64×32 display, keyboard events, and file menu actions; it never touches CPU internals directly, instead calling the small public API.
- `main.py`: Thin coordinator that wires `Chip8` and `GUI` together, schedules CPU cycles, and tracks the currently loaded ROM path.

## ROMs

Sample programs live under `ROMs/`. Drop additional `.ch8` files in that folder (or anywhere on disk) and open them via the menu. The emulator keeps the last-loaded ROM in memory so you can reset it instantly without digging through the file dialog again.

## Troubleshooting

- The ROM menu does nothing: confirm the Python process has permission to read the file path you selected.
- Black screen: some games wait for key input at startup. Press a mapped key or reload the ROM.
- Window freezes: make sure only one instance of `application.py` is running. Tkinter trips up when multiple processes share the same interpreter.
