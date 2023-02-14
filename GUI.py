import tkinter as tk
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox


class GUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.canvas = None
        self.menu = None
        self.master.title("Chip-8 Emulator")
        self.pack()

        self.createWidgets()

    def createWidgets(self):
        self.canvas = tk.Canvas(self, width=640, height=320, bg="white")
        self.canvas.pack(side="top")

        self.menu = tk.Menu(self)
        self.menu.add_command(label="Open", command=self.openFile)
        self.menu.add_command(label="Save", command=self.saveFile)
        self.menu.add_command(label="Exit", command=self.quit)
        self.master.config(menu=self.menu)

    def openFile(self):
        filename = tkFileDialog.askopenfilename()
        if filename:
            print("Open file: ", filename)

    def saveFile(self):
        filename = tkFileDialog.asksaveasfilename()
        if filename:
            print("Save file: ", filename)

    def quit(self):
        if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
            tk.Frame.quit(self)

    def draw_rect(self, x, y, width, height):
        self.canvas.create_rectangle(x, y, x + width, y + height, fill="black")

    def stretch_pixel_array_to_canvas(self, pixel_array):
        # print(len(pixel_array), len(pixel_array[0]))
        for y in range(32):
            for x in range(64):
                # print(y, x)
                if pixel_array[y][x] == 1:
                    self.draw_rect(x * 10, y * 10, 10, 10)

    def update_canvas(self, display):
        self.stretch_pixel_array_to_canvas(display)
        self.canvas.update()


def draw_rect_every_2_seconds(i=0):
    app.draw_rect(0, 0, 10 ** i, 10 ** i)
    i += 1
    app.after(2000, draw_rect_every_2_seconds, i)


if __name__ == "__main__":
    app = GUI()
    app.after(2000, draw_rect_every_2_seconds)
    app.mainloop()
