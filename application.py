from GUI import *
from chip8emulator import *


class Application:
    def __init__(self):
        self.application = GUI()
        self.CPU = Chip8()
        self.application.after(1, self.run)
        self.application.mainloop()

    def run(self):
        self.CPU.update(1000//60)
        self.application.update_canvas(self.CPU.Display)
        self.application.after(1000//60, self.run)


app = Application()