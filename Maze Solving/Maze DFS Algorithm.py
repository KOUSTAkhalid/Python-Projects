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

        if self.is_visited and not GAME:
            canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='green', outline="")

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
            num = random.choice([0,3])
            self.walls[num] = False
            if num == 0:
                grid[index(self.i, self.j-1)].walls[2] = False
            else:
                grid[index(self.i-1, self.j)].walls[1] = False

    def highlight(self, canvas):
        x = self.i * cell_size
        y = self.j * cell_size

        canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='green', outline="")

    def mark_as_solution(self, canvas):
        r = 5
        x = self.i * cell_size + r
        y = self.j * cell_size + r
        fx = self.i * cell_size + cell_size - r
        fy = self.j * cell_size + cell_size - r

        canvas.create_oval(x, y, fx, fy, fill='red')

def index(i, j):
    return i + j * columns

def setup_grid():
    for j in range(columns):
        for i in range(rows):
            cell = Cell(i, j)
            grid.append(cell)


# Set constant variables for window size
WINDOW_SIZE = 600
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


# -----------------------------Create the Maze-----------------------------
print("WELCOME to maze Generator Binary Tree based algorithm.")
print("\n--------Generating Maze--------")
if input("do you wanna see The Simulation (y/n): ") == 'y':
    start_time = time.time()
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

        # Update tkinter window
        sim_window.update()

        # Speed of simulation
        #sim_window.after(speed)
else:
    start_time = time.time()
    for unit in range(1, len(grid)):
        # Remove walls if there is
        grid[unit].remove_walls(grid)

        # new is old
        old = grid[unit]

    # Set Up playGround
    for i in range(columns * rows):
        grid[i].show(sim_canvas)

sim_window.update()
print("Generation Time: %s seconds" % round((time.time() - start_time),3))

# -----------------------------Solve the Maze-----------------------------

class Mouse:
    """A class to model a Cell, which will solve the Maze"""

    def __init__(self):
        self.i = 0
        self.j = 0

    def show_mouse(self, canvas):
        r = 5
        x = self.i * cell_size + r
        y = self.j * cell_size + r
        fx = self.i * cell_size + cell_size - r
        fy = self.j * cell_size + cell_size - r

        canvas.create_oval(x, y, fx, fy, fill='red')

    def move(self, direc):

        if self.i == direc.i:
            mv = direc.j - self.j
            self.j += mv
        if self.j == direc.j:
            mv = direc.i - self.i
            self.i += mv

    def check_roads(self, maze):
        roads = []

        if self.i :
            left = maze[index(self.i-1, self.j)]
            if not left.is_visited and not left.walls[1]:
                roads.append(left)
        if self.j:
            top = maze[index(self.i, self.j-1)]
            if not top.is_visited and not top.walls[2]:
                roads.append(top)
        if self.i < columns-1:
            right = maze[index(self.i + 1, self.j)]
            if not right.is_visited and not right.walls[3]:
                roads.append(right)
        if self.j < rows-1:
            bottom = maze[index(self.i, self.j + 1)]
            if not bottom.is_visited and not bottom.walls[0]:
                roads.append(bottom)

        if roads:
            choice = random.choice(roads)
            return choice


class Goal:
    """A class to generate a random Goal"""
    def __init__(self):
        self.i = random.randint(int(columns/2), columns)
        self.j = random.randint(int(rows/2), rows)

    def show_goal(self, canvas):
        r = 5
        x = self.i * cell_size + r
        y = self.j * cell_size + r
        fx = self.i * cell_size + cell_size - r
        fy = self.j * cell_size + cell_size - r

        canvas.create_oval(x, y, fx, fy, fill='green')

def is_win(m, g):
    if [m.i,m.j] == [g.i,g.j]:
        return True
    else:
        return False

# Initialize Solving parameters
mouse = Mouse()
goal = Goal()
stack = []
GAME = False

# Highlight the goal
goal.show_goal(sim_canvas)

# Update tkinter window
sim_window.update()

# Solving loop
input("\nPress ENTER to start solving the maze.... ")
print("\n--------Solving Maze--------")
if input("do you wanna see The Simulation (y/n): ") == 'y':
    start_time = time.time()
    while not GAME:
        # delete screen
        sim_canvas.delete('all')

        # Show maze
        for i in range(columns * rows):
            grid[i].show(sim_canvas)

        # Highlight the mouse
        mouse.show_mouse(sim_canvas)

        # Highlight the goal
        goal.show_goal(sim_canvas)

        # Check if reached
        GAME = is_win(mouse, goal)

        # Check road
        choice = mouse.check_roads(grid)
        if choice:
            # Mark cell as visited
            choice.is_visited = True

            # add cell to stack
            stack.append(grid[index(mouse.i, mouse.j)])

            # Move to next cell
            mouse.move(choice)
        else:
            current = stack.pop()
            mouse.i,mouse.j = current.i,current.j

        # Update tkinter window
        sim_window.update()

        # Speed of simulation
        # sim_window.after(speed)
else:
    start_time = time.time()
    while not GAME:
        # Check if reached
        GAME = is_win(mouse, goal)

        # Check road
        choice = mouse.check_roads(grid)
        if choice:
            # Mark cell as visited
            choice.is_visited = True

            # add cell to stack
            stack.append(grid[index(mouse.i, mouse.j)])

            # Move to next cell
            mouse.move(choice)
        else:
            current = stack.pop()
            mouse.i, mouse.j = current.i, current.j

# delete screen
sim_canvas.delete('all')

# Show maze
for i in range(columns * rows):
    grid[i].show(sim_canvas)

# Show solution
for unit in stack:
    unit.mark_as_solution(sim_canvas)



print("Solving Time: %s seconds" % round((time.time() - start_time),3))
print("\n\nTHANKS!! for using this App <3 <3")
print("==== made by: KOUSTA KHALID ====")
sim_window.mainloop()
