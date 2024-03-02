import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
from ttkbootstrap import Style
from PIL import ImageGrab


class Whiteboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Whiteboard")
        self.master.resizable(False, False)
        self.style = Style(theme="pulse")
        self.canvas = tk.Canvas(self.master, width=1200, height=600, bg="white")
        self.canvas.pack()
        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(side='top', pady=10)

        # Button configuration
        buttons = {
            "Clear": ("light.TButton", self.clear_canvas),
            "Save": ("primary.TButton", self.save_image),
            "Eraser": ("danger.TButton", self.toggle_eraser)
        }

        for color, (style, command) in buttons.items():
            ttk.Button(self.button_frame, text=color.capitalize(),
                       command=command, style=style).pack(side="left", padx=5, pady=5)

        # Drawing variables
        self.draw_color = "black"
        self.eraser_mode = False  # Track if eraser mode is active
        self.line_width = tk.DoubleVar(value=5)
        self.old_x, self.old_y = None, None

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_line)
        self.canvas.bind("<B1-Motion>", self.draw_line)

        # Line weight scale
        ttk.Label(self.button_frame, text="Line Weight:").pack(side="left", padx=5, pady=5)
        self.line_weight_scale = ttk.Scale(self.button_frame, from_=1, to=20, orient="horizontal",
                                           variable=self.line_width)
        self.line_weight_scale.pack(side="left", padx=5, pady=5)
        self.line_weight_scale.bind("<<ScaleSelected>>", self.change_line_weight)

        # Color palette button
        ttk.Button(self.button_frame, text="Choose Color", command=self.choose_color).pack(side="left", padx=5, pady=5)

        # Bind Ctrl+S for saving
        self.master.bind("<Control-s>", self.save_image)

    def start_line(self, event):
        self.old_x, self.old_y = event.x, event.y

    def draw_line(self, event):
        if self.old_x and self.old_y:
            if self.eraser_mode:  # If eraser mode is active, draw with background color
                draw_color = self.canvas["bg"]
            else:
                draw_color = self.draw_color

            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=self.line_width.get(), fill=draw_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.old_x, self.old_y = event.x, event.y

    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.draw_color)
        if color[1]:
            self.draw_color = color[1]

    def clear_canvas(self):
        self.canvas.delete("all")

    def change_line_weight(self, event=None):
        pass  # No need for change_line_weight function, line width is updated directly from the scale

    def save_image(self, event=None):
        filename = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("All Files", "*.*")])
        if filename:
            x = self.master.winfo_rootx() + self.canvas.winfo_x()
            y = self.master.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(filename)

    def toggle_eraser(self):
        self.eraser_mode = not self.eraser_mode


if __name__ == "__main__":
    root = tk.Tk()
    whiteboard = Whiteboard(root)
    root.mainloop()
