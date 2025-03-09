import tkinter as tk

def paint(event):
    x, y = event.x, event.y
    # Draw a small circle at the cursor
    canvas.create_oval(x-2, y-2, x+2, y+2, fill='black')
    # Force immediate refresh (some macOS builds need this)
    root.update_idletasks()

root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200, bg='white')
canvas.pack()

# Bind "mouse is moving while left button is held"
canvas.bind("<B1-Motion>", paint)

root.mainloop()

