import tkinter as tk

def paint(event):
    x, y = event.x, event.y
    canvas.create_oval(x-2, y-2, x+2, y+2)

root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200, bg='white')
canvas.pack()
canvas.bind("<B1-Motion>", paint)
root.mainloop()
