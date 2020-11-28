import tkinter
import random

class Cell:
    """A class to model a Cell"""

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True, True, True, True]

    def show(self, canvas):
        global cell_size
        x = self.i * cell_size
        y = self.j * cell_size

        if self.walls[0]:
            canvas.create_line(x, y, x + cell_size, y, fill='black')
        if self.walls[1]:
            canvas.create_line(x + cell_size, y, x + cell_size, y + cell_size, fill='black')
        if self.walls[2]:
            canvas.create_line(x + cell_size, y + cell_size, x, y + cell_size, fill='black')
        if self.walls[3]:
            canvas.create_line(x, y + cell_size, x, y, fill='black')

    def remove_walls(self, grd):

        if self.i == 0 and 0 < self.j < rows :
            self.walls[0] = False
            grid[index(self.i, self.j - 1)].walls[2] = False
        elif self.j == 0 and 0 < self.i < columns:
            self.walls[3] = False
            grid[index(self.i - 1, self.j)].walls[1] = False
        else:
            #neighbors = random.choice([grid[index(self.i, self.j - 1)],grid[index(self.i - 1, self.j)]])
            num = random.choice([0,3])
            self.walls[num] = False
            if num == 0:
                grid[index(self.i, self.j-1)].walls[2] = False
            else:
                grid[index(self.i-1, self.j)].walls[1] = False

        #return neighbors

    def highlight(self, canvas):
        x = self.i * cell_size
        y = self.j * cell_size

        canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='green', outline="")

def index(i, j):
    return i + j * columns

def setup_grid():
    for j in range(columns):
        for i in range(rows):
            cell = Cell(i, j)
            grid.append(cell)


# Set constant variables for window size
WINDOW_SIZE = 500
cell_size = 20
columns = int(WINDOW_SIZE / cell_size)
rows = int(WINDOW_SIZE / cell_size)

# Initialize cells grid
grid = []
old = []
new = []

# Initialize simulation
speed = 2

# Create the tkinter window and canvas
sim_window = tkinter.Tk()
sim_window.title("Maze GENERATOR")
sim_window.resizable(0, 0)
sim_canvas = tkinter.Canvas(sim_window, width=WINDOW_SIZE, height=WINDOW_SIZE, highlightthickness=0, bg='white')
sim_canvas.pack(side=tkinter.LEFT)

# setup grid
setup_grid()
old = grid[0]

# Run the simulation
print("WELCOME to maze Generator Binary Tree based algorithm.")
print("\n-----Generating Maze.....-----")
if input("do you wanna see The Simulation (y/n): ") == 'y':
    for unit in range(1, len(grid)):
        # delete screen
        sim_canvas.delete('all')

        # Highlight the cell
        grid[unit].highlight(sim_canvas)

        # Set Up playGround
        for i in range(columns * rows):
            grid[i].show(sim_canvas)

        # Remove walls if there is
        grid[unit].remove_walls(grid)

        # new is old
        old = grid[unit]

        # Update tkinter window
        sim_window.update()

        # Speed of simulation
        #sim_window.after(speed)
else:
    for unit in range(1, len(grid)):
        # Remove walls if there is
        grid[unit].remove_walls(grid)

        # new is old
        old = grid[unit]

    # Set Up playGround
    for i in range(columns * rows):
        grid[i].show(sim_canvas)

sim_window.update()
print("\nTHANKS!! for using this App <3 <3")
print("==== made by: KOUSTA KHALID ====")
sim_window.mainloop()
