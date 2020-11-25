import tkinter
import random
import time


class Cell:
    """A class to model a Cell"""

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True, True, True, True]
        self.is_visited = False

    def show(self, canvas):
        global cell_size
        x = self.i * cell_size
        y = self.j * cell_size

        if self.is_visited:
            canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='blue', outline="")

        if self.walls[0]:
            canvas.create_line(x, y, x + cell_size, y, fill='white')
        if self.walls[1]:
            canvas.create_line(x + cell_size, y, x + cell_size, y + cell_size, fill='white')
        if self.walls[2]:
            canvas.create_line(x + cell_size, y + cell_size, x, y + cell_size, fill='white')
        if self.walls[3]:
            canvas.create_line(x, y + cell_size, x, y, fill='white')

    def highlight(self, canvas):
        x = self.i * cell_size
        y = self.j * cell_size

        if self.is_visited:
            canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='green', outline="")

    def check_neighbors(self, grid):
        neighbors = []
        global columns

        if self.j:
            top = grid[index(self.i, self.j - 1)]
            if not top.is_visited:
                neighbors.append(top)
        if self.i < columns - 1:
            right = grid[index(self.i + 1, self.j)]
            if not right.is_visited:
                neighbors.append(right)
        if self.j < rows - 1:
            bottom = grid[index(self.i, self.j + 1)]
            if not bottom.is_visited:
                neighbors.append(bottom)
        if self.i:
            left = grid[index(self.i - 1, self.j)]
            if not left.is_visited:
                neighbors.append(left)

        if len(neighbors) > 0:
            num = random.randint(0, len(neighbors) - 1)
            return neighbors[num]

    def make_a_path(self, canvas):
        global cell_size
        x = self.i * cell_size
        y = self.j * cell_size

        r = cell_size / 4
        f_x = x + r
        f_y = y + r
        canvas.create_oval(f_x, f_y, f_x + cell_size - 2 * r, f_y + cell_size - 2 * r, fill="red")

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


def show_last(grid, canvas):
    global cell_size
    r = cell_size / 4
    f_x = grid[0].i * cell_size + r
    f_y = grid[0].j * cell_size + r
    l_x = grid[-1].i * cell_size + r
    l_y = grid[-1].j * cell_size + r
    canvas.create_oval(f_x, f_y, f_x + cell_size - 2 * r, f_y + cell_size - 2 * r, fill="red")
    canvas.create_oval(l_x, l_y, l_x + cell_size - 2 * r, l_y + cell_size - 2 * r, fill="green")


def setup():
    for j in range(columns):
        for i in range(rows):
            cell = Cell(i, j)
            grid.append(cell)


# Set constant variables for window size
WINDOW_SIZE = 300
cell_size = 20
columns = int(WINDOW_SIZE / cell_size)
rows = int(WINDOW_SIZE / cell_size)
grid = []
stack = []
path = []
k = 0
make = True
new_path = False
start_time = time.time()

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
print("Generating Maze.....")
while len(stack) != 0:
    # Show
    for i in range(len(grid)):
        grid[i].show(sim_canvas)

    current.is_visited = True
    current.highlight(sim_canvas)

    # STEP 1
    Next = current.check_neighbors(grid)
    if Next:
        # STEP 2
        stack.append(current)
        Next.is_visited = True

        # STEP 3
        remove_walls(current, Next)

        # STEP 4
        current = Next

        # If it's the corner Cell, start saving the path
        if current.i == columns - 1 and current.j == rows - 1:
            path = stack.copy()
    else:
        current = stack.pop()

    # Update tkinter window
    sim_window.update()
    #sim_window.after(500)

    # wipe the canvas clean
    if len(stack) != 0:
        sim_canvas.delete('all')


for item in path:
    item.make_a_path(sim_canvas)
    sim_window.update()
    time.sleep(.1)


show_last(grid, sim_canvas)
print("Generation Time: %s seconds" % round((time.time() - start_time), 3))
sim_window.mainloop()
