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
WINDOW_SIZE = 400
cell_size = 20
columns = int(WINDOW_SIZE / cell_size)
rows = int(WINDOW_SIZE / cell_size)

# Initialize cells grid
grid = []
old = []
new = []

# Initialize simulation
speed = 100

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

    def __init__(self, g):
        self.i = g.i
        self.j = g.j
        self.stack = []
        self.visible = True

    def show_mouse(self, canvas):
        if self.visible:
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
            return roads
        else:
            return None

class Goal:
    """A class to generate a random Goal"""
    def __init__(self):
        self.i = random.randint(int(columns/2), columns-1)
        self.j = random.randint(int(rows/2), rows-1)

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
mice = [Mouse(grid[0])]
mice[0].stack.append(grid[0])
grid[0].is_visited = True

# If you want to start in a random position incomment this ana comment the last 3 lines
"""
randd = random.choice(grid)
mice = [Mouse(randd)]
mice[0].stack.append(randd)
randd.is_visited = True
"""

goal = Goal()
stack = []
GAME = False

new_mice = []

# Highlight the goal
goal.show_goal(sim_canvas)

# Show start position
mice[0].show_mouse(sim_canvas)

# Update tkinter window
sim_window.update()

# Solving loop
input("\nPress ENTER to start solving the maze.... ")
print("\n--------Solving Maze--------")

if input("do you wanna see The Simulation (y/n): ") == 'y':
    start_time = time.time()
    #----------Solving Algorithm----------
    while not GAME:
        print(len(mice))
        # delete screen
        sim_canvas.delete('all')

        # Show maze
        for i in range(columns * rows):
            grid[i].show(sim_canvas)

        # Highlight the goal
        goal.show_goal(sim_canvas)


        for mouse in mice:
            # Check road
            choice = mouse.check_roads(grid)

            # if there are any non visited roads
            if choice:
                if len(choice) > 1:
                    # delete old mouse, and mark cell as visited
                    mouse.visible = False

                    # for each road available create a new mouse

                    for unit in choice:
                        # create new mouse
                        mm = Mouse(unit)
                        mm.stack.append(unit)
                        mm.stack.extend(mouse.stack)
                        new_mice.append(mm)

                        # mark cell as visited
                        unit.is_visited = True
                else:
                    # delete old mouse, and mark cell as visited
                    mouse.visible = False

                    # create new mouse
                    new_mice.append(Mouse(choice[0]))

                    # mark cell as visited
                    choice[0].is_visited = True

                    # add to stack
                    mouse.stack.append(choice[0])
                    new_mice[-1].stack.extend(mouse.stack)
            else:
                # delete old mouse, and mark cell as visited
                mouse.visible = False

        mice.extend(new_mice)

        # Show mice
        for mouse in mice:
            mouse.show_mouse(sim_canvas)
            # Check if reached
            GAME = is_win(mouse, goal)
            if GAME:
                winner = mouse
                break

        # simulation speed
        sim_window.after(50)

        # Update tkinter window
        sim_window.update()

else:
    start_time = time.time()
    while not GAME:
        # Highlight the goal
        goal.show_goal(sim_canvas)

        for mouse in mice:
            # Check road
            choice = mouse.check_roads(grid)

            # if there are any non visited roads
            if choice:
                if len(choice) > 1:
                    # delete old mouse, and mark cell as visited
                    mouse.visible = False

                    # for each road available create a new mouse

                    for unit in choice:
                        # create new mouse
                        mm = Mouse(unit)
                        mm.stack.append(unit)
                        mm.stack.extend(mouse.stack)
                        new_mice.append(mm)

                        # mark cell as visited
                        unit.is_visited = True
                else:
                    # delete old mouse, and mark cell as visited
                    mouse.visible = False

                    # create new mouse
                    new_mice.append(Mouse(choice[0]))

                    # mark cell as visited
                    choice[0].is_visited = True

                    # add to stack
                    mouse.stack.append(choice[0])
                    new_mice[-1].stack.extend(mouse.stack)
            else:
                # delete old mouse, and mark cell as visited
                mouse.visible = False

        mice.extend(new_mice)

        # Show mice
        for mouse in mice:
            # Check if reached
            GAME = is_win(mouse, goal)
            if GAME:
                winner = mouse
                break

        # Update tkinter window
        sim_window.update()
#---------------------------------------





# delete screen
sim_canvas.delete('all')

# Show maze
for i in range(columns * rows):
    grid[i].show(sim_canvas)

# Show solution
for unit in winner.stack:
    unit.mark_as_solution(sim_canvas)


print("Solving Time: %s seconds" % round((time.time() - start_time),3))
print("\n\nTHANKS!! for using this App <3 <3")
print("==== made by: KOUSTA KHALID ====")
sim_window.mainloop()
