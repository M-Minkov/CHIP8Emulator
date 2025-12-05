import time
from pathlib import Path

from GUI import GUI
from chip8emulator import Chip8

DEFAULT_ROM = Path("ROMs/IBM_Logo.ch8")


class Main:
    def __init__(self, rom_path=None):
        self.CPU = Chip8()
        self.application = GUI(self.CPU, on_rom_loaded=self.load_rom, on_reset=self.reload_rom)
        self.current_rom = None
        self.last_tick = time.perf_counter()
        initial_rom = rom_path or (str(DEFAULT_ROM) if DEFAULT_ROM.exists() else None)
        if initial_rom:
            try:
                self.load_rom(initial_rom)
            except Exception:
                pass
        self.application.after(1, self.run)
        self.application.mainloop()

    def load_rom(self, path):
        self.CPU.load_rom_from_path(path)
        self.current_rom = path
        self.application.update_window_title(path)

    def reload_rom(self):
        if self.current_rom:
            self.CPU.reload_current_rom()
        elif DEFAULT_ROM.exists():
            self.load_rom(str(DEFAULT_ROM))

    def run(self):
        now = time.perf_counter()
        delta_ms = (now - self.last_tick) * 1000.0
        self.last_tick = now
        self.CPU.update(delta_ms)
        self.application.update_canvas(self.CPU.Display)
        self.application.after(1, self.run)


if __name__ == "__main__":
    Main()