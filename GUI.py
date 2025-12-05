import tkinter as tk
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox
from pathlib import Path

KEY_MAPPING = {
    "1": 0x1,
    "2": 0x2,
    "3": 0x3,
    "4": 0xC,
    "q": 0x4,
    "w": 0x5,
    "e": 0x6,
    "r": 0xD,
    "a": 0x7,
    "s": 0x8,
    "d": 0x9,
    "f": 0xE,
    "z": 0xA,
    "x": 0x0,
    "c": 0xB,
    "v": 0xF
}


class GUI(tk.Frame):
    def __init__(self, chip8, master=None, scale=10, on_rom_loaded=None, on_reset=None):
        if master is None:
            master = tk.Tk()
        tk.Frame.__init__(self, master)
        self.chip8 = chip8
        self.scale = scale
        self.on_rom_loaded = on_rom_loaded
        self.on_reset = on_reset
        self.canvas = None
        self.menu = None
        self.master.title("Chip-8 Emulator")
        self.pack()
        self.createWidgets()
        self.bind_all("<KeyPress>", self.handle_key_press)
        self.bind_all("<KeyRelease>", self.handle_key_release)

    def createWidgets(self):
        width = 64 * self.scale
        height = 32 * self.scale
        self.canvas = tk.Canvas(self, width=width, height=height, bg="#1A1A1A", highlightthickness=0)
        self.canvas.pack(side="top")

        self.menu = tk.Menu(self.master)
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Open ROM...", command=self.openFile)
        file_menu.add_command(label="Reload ROM", command=self.saveFile)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="File", menu=file_menu)
        self.master.config(menu=self.menu)

    def openFile(self):
        filename = tkFileDialog.askopenfilename(filetypes=[("CHIP-8 ROM", "*.ch8"), ("All Files", "*.*")])
        if not filename:
            return
        try:
            if self.on_rom_loaded:
                self.on_rom_loaded(filename)
            else:
                self.chip8.load_rom_from_path(filename)
            self.update_window_title(filename)
        except Exception as exc:
            tkMessageBox.showerror("ROM Load Failed", str(exc))

    def saveFile(self):
        try:
            if self.on_reset:
                self.on_reset()
            else:
                self.chip8.reload_current_rom()
        except Exception as exc:
            tkMessageBox.showerror("Reload Failed", str(exc))

    def quit(self):
        if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
            tk.Frame.quit(self)

    def draw_rect(self, x, y, width, height, fill="white"):
        self.canvas.create_rectangle(x, y, x + width, y + height, fill=fill, outline="", tags="pixel")

    def stretch_pixel_array_to_canvas(self, pixel_array):
        # print(len(pixel_array), len(pixel_array[0]))
        self.canvas.delete("pixel")
        for y in range(32):
            for x in range(64):
                # print(y, x)
                color = "white" if pixel_array[y][x] == 1 else "black"
                self.draw_rect(x * self.scale, y * self.scale, self.scale, self.scale, fill=color)

    def update_canvas(self, display):
        self.stretch_pixel_array_to_canvas(display)
        self.canvas.update_idletasks()

    def update_window_title(self, path):
        name = Path(path).name
        self.master.title(f"Chip-8 Emulator - {name}")

    def handle_key_press(self, event):
        key = event.keysym.lower()
        if key in KEY_MAPPING:
            self.chip8.set_key_state(KEY_MAPPING[key], True)

    def handle_key_release(self, event):
        key = event.keysym.lower()
        if key in KEY_MAPPING:
            self.chip8.set_key_state(KEY_MAPPING[key], False)
