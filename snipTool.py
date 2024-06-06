import tkinter as tk
from tkinter import Canvas
from box import Box

class SnipToolFactory:
    def createNewSnip(self):
        snipTool = SnipTool()
        snipTool.mainloop()
        return snipTool.box


class SnipTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        self.canvas = Canvas(self, cursor="tcross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        self.canvas.bind("<Button-2>", self.cancel)
        self.canvas.bind("<Button-3>", self.cancel)
        
        self.attributes("-transparentcolor", "white")
        self.attributes("-alpha", 0.5)
        self.attributes("-fullscreen", True)
        self.box = None

    def cancel(self, event):
        self.destroy()

    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')
            
    def on_drag(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_release(self, event):
        if self.rect:
            end_x = self.canvas.canvasx(event.x)
            end_y = self.canvas.canvasy(event.y)
            screenBox = self.createBox(self.start_x, self.start_y, end_x, end_y)
            
            if screenBox.isPoint():
                return
            
            self.box = screenBox
            self.destroy()

    def createBox(self, start_x, start_y, end_x, end_y):
        x1 = min(start_x, end_x)
        y1 = min(start_y, end_y)
        x2 = max(start_x, end_x)
        y2 = max(start_y, end_y)
        return Box((x1, y1), (x2, y2))


if __name__ == "__main__":
    app = SnipToolFactory()
    box = app.createNewSnip()
    print(box.getResolution())