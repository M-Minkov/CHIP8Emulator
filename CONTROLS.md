# Chip-8 Controls

The Chip-8 keypad is a 4×4 hex grid:

```
1 2 3 C
4 5 6 D
7 8 9 E
A 0 B F
```

This emulator maps the keypad onto a QWERTY keyboard:

| Chip-8 | Keyboard |
| --- | --- |
| 1 2 3 C | 1 2 3 4 |
| 4 5 6 D | Q W E R |
| 7 8 9 E | A S D F |
| A 0 B F | Z X C V |

### Quick Tips

- `5` (mapped to `W`) is commonly used as Start/Fire.
- `2/4/6/8` (`2`, `Q`, `E`, `S`) often act as up/left/right/down.
- Corner buttons (`1/4/7` or `3/6/9`) become secondary actions in some ROMs.
- Open `Help → Chip-8 Controls` in the app at any time to pop up this layout while playing.
