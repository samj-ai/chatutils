import tkinter as tk
from collections import deque

class ASCIIPaint:
    def __init__(self, master, rows=15, cols=40, cell_size=20):
        self.master = master
        master.title("ASCII Art Painter")

        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        # 2D array of characters
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]

        # The currently chosen paint character
        self.current_char = tk.StringVar(value="#")

        # Whether we are in "fill" mode
        self.fill_mode = tk.BooleanVar(value=False)

        # -- Top control frame --
        control_frame = tk.Frame(master)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Current char entry
        tk.Label(control_frame, text="Current char:").pack(side=tk.LEFT)
        tk.Entry(control_frame, textvariable=self.current_char, width=3).pack(side=tk.LEFT, padx=5)

        # Fill toggle button
        self.fill_button = tk.Button(
            control_frame, text="Toggle Fill (OFF)",
            command=self.toggle_fill_mode
        )
        self.fill_button.pack(side=tk.LEFT, padx=5)

        # Export button
        tk.Button(control_frame, text="Export", command=self.export_grid).pack(side=tk.LEFT, padx=5)

        # Copy-to-clipboard button
        tk.Button(control_frame, text="Copy", command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=5)

        # The Tk canvas, white background
        self.canvas = tk.Canvas(
            master,
            width=cols * cell_size,
            height=rows * cell_size,
            bg="white"
        )
        self.canvas.pack(side=tk.BOTTOM)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_click)    # single click
        self.canvas.bind("<B1-Motion>", self.on_drag)    # click+drag
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Draw the entire grid once
        self.full_redraw()

    def toggle_fill_mode(self):
        # Flip fill mode
        self.fill_mode.set(not self.fill_mode.get())
        if self.fill_mode.get():
            self.fill_button.config(text="Toggle Fill (ON)")
        else:
            self.fill_button.config(text="Toggle Fill (OFF)")

    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.fill_mode.get():
                # Perform a BFS fill, then redraw everything once
                self.fill(row, col, self.current_char.get())
                self.full_redraw()
            else:
                # Paint a single cell
                self.grid[row][col] = self.current_char.get()
                self.draw_cell(row, col)
                # Force immediate refresh
                self.master.update_idletasks()

        print(f"Click at row={row}, col={col}")

    def on_drag(self, event):
        # Only paint while dragging if we're NOT in fill mode
        if not self.fill_mode.get():
            col = event.x // self.cell_size
            row = event.y // self.cell_size

            if 0 <= row < self.rows and 0 <= col < self.cols:
                self.grid[row][col] = self.current_char.get()
                self.draw_cell(row, col)
                self.master.update_idletasks()

            print(f"Drag at row={row}, col={col}")

    def on_release(self, event):
        pass

    def fill(self, row, col, new_char):
        """
        Fills a contiguous region of identical old_char cells
        with new_char, starting from (row, col).
        """
        old_char = self.grid[row][col]
        if old_char == new_char:
            return  # No change

        queue = deque([(row, col)])
        while queue:
            r, c = queue.popleft()
            if 0 <= r < self.rows and 0 <= c < self.cols:
                if self.grid[r][c] == old_char:
                    self.grid[r][c] = new_char
                    queue.append((r - 1, c))
                    queue.append((r + 1, c))
                    queue.append((r, c - 1))
                    queue.append((r, c + 1))

    def draw_cell(self, r, c):
        """
        Draw exactly one grid cell (rectangle + optional character text).
        Black outline, black text, white fill so we can see everything.
        """
        x1 = c * self.cell_size
        y1 = r * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Draw the cell outline in black; fill white
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")

        # If not space, draw the character in black
        char = self.grid[r][c]
        if char != ' ':
            self.canvas.create_text(
                (x1 + x2) // 2,
                (y1 + y2) // 2,
                text=char,
                fill="black",
                anchor="center"
            )

    def full_redraw(self):
        """
        Clear the entire canvas and redraw all cells.
        """
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                self.draw_cell(r, c)
        # Force the canvas to repaint immediately
        self.master.update_idletasks()

    def export_grid(self):
        """
        Print out the current grid as ASCII text.
        """
        ascii_art = self.get_ascii_art()
        print("----- ASCII EXPORT -----")
        print(ascii_art)
        print("------------------------")

    def copy_to_clipboard(self):
        """
        Copy the current ASCII art to the system clipboard.
        """
        ascii_art = self.get_ascii_art()
        # Clear the clipboard and append our ASCII art
        self.master.clipboard_clear()
        self.master.clipboard_append(ascii_art)
        print("ASCII art copied to clipboard!")

    def get_ascii_art(self):
        """
        Returns the current ASCII art as a string with newlines.
        """
        lines = []
        for r in range(self.rows):
            line = "".join(self.grid[r])
            lines.append(line)
        return "\n".join(lines)

if __name__ == "__main__":
    root = tk.Tk()
    app = ASCIIPaint(root, rows=15, cols=40, cell_size=20)
    root.mainloop()
