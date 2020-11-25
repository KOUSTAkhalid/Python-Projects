from PIL import Image, ImageGrab
import tkinter
import random
import subprocess
import io

class Cell:
    """A class to model a Cell"""

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True, True, True, True]
        self.is_visited = False

    def show(self, canvas):
        global cell_size
        x = self.i*cell_size
        y = self.j*cell_size

        if self.is_visited:
            canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='brown', outline="")

        if self.walls[0]:
            canvas.create_line( x            , y            , x + cell_size, y            , fill='white')
        if self.walls[1]:
            canvas.create_line( x + cell_size, y            , x + cell_size, y + cell_size, fill='white')
        if self.walls[2]:
            canvas.create_line( x + cell_size, y + cell_size, x            , y + cell_size, fill='white')
        if self.walls[3]:
            canvas.create_line( x            , y + cell_size, x            , y            , fill='white')

    def highlight(self, canvas):
        x = self.i*cell_size
        y = self.j*cell_size

        if self.is_visited:
            canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='red', outline="")

    def check_neighbors(self, grid):
        neighbors = []
        global columns

        if self.j:
            top    = grid[index(self.i    , self.j - 1)]
            if not top.is_visited:
                neighbors.append(top)
        if self.i < columns-1:
            right  = grid[index(self.i + 1, self.j    )]
            if not right.is_visited:
                neighbors.append(right)
        if self.j < rows-1:
            bottom = grid[index(self.i    , self.j + 1)]
            if not bottom.is_visited:
                neighbors.append(bottom)
        if self.i:
            left   = grid[index(self.i - 1, self.j    )]
            if not left.is_visited:
                neighbors.append(left)

        if len(neighbors) > 0:
            num = random.randint(0, len(neighbors)-1)
            return neighbors[num]


def index(i, j):
    return i + j * columns

def remove_walls(a, b):
    x = a.i - b.i
    if x == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif x == -1:
        a.walls[1] = False
        b.walls[3] = False

    y = a.j - b.j
    if y == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif y == -1:
        a.walls[2] = False
        b.walls[0] = False


def setup():
    for j in range(columns):
        for i in range(rows):
            cell = Cell(i, j)
            grid.append(cell)


# Set constant variables for window size
WINDOW_SIZE = 400
cell_size = 20
columns = int(WINDOW_SIZE/cell_size)
rows = int(WINDOW_SIZE/cell_size)
grid = []
stack = []
k = 0
make = True

# Create the tkinter window and canvas
sim_window = tkinter.Tk()
sim_window.title("Maze GENERATOR")
sim_window.resizable(0, 0)
sim_canvas = tkinter.Canvas(sim_window, width=WINDOW_SIZE, height=WINDOW_SIZE, highlightthickness=0, bg='black')
sim_canvas.pack(side=tkinter.LEFT)

# setup grid
setup()
current = grid[0]
stack.append(current)

# Run the simulation
while make :
    # Show
    # STEP 1
    current.is_visited = True
    for i in range(len(grid)):
        grid[i].show(sim_canvas)

    # STEP 2
    Next = current.check_neighbors(grid)
    current.highlight(sim_canvas)

    if Next:
        stack.append(current)
        Next.is_visited = True

        # STEP 3
        remove_walls(current, Next)

        # STEP 4
        current = Next
    else:
        #go_back(stack)
        if len(stack) == 0:
            make = False

        else:
            current = stack.pop()
            current.is_visited = True

    # Update tkinter window
    sim_window.update()
    #sim_window.after(100)

    # wipe the canvas clean
    if make:
        sim_canvas.delete('all')

sim_window.mainloop()