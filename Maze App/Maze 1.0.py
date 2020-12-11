import tkinter
import webbrowser
import random
from tkinter import messagebox
from tkinter import *
import os

#---------------------------------App Class-------------------------------
class MyApp(object):
    """My app Class"""

    # Thanks to https://stackoverflow.com/questions/62168137/tkinter-flush-buttons-next-to-each-other
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Maze 1.0")

        # Set constant variables for window size
        self.canvas_size = 500
        cell_size = int(self.canvas_size/20)
        self.columns = 30
        self.rows = 30

        # Maze variables
        self.grid = []

        self.Maze_frame = tkinter.LabelFrame(text="Maze", width=self.canvas_size+20, height=self.canvas_size+25)
        self.Menu_frame = tkinter.LabelFrame(text="Generator", width=300, height=200)
        self.Solving_frame = tkinter.LabelFrame(text="Solver", width=300, height=200)
        self.Info_frame = tkinter.LabelFrame(text="Info", width=300, height=210)
        #self.Maze_frame.pack()

        self.Maze_frame.place(x=310, y=5)
        self.Menu_frame.place(x=10, y=5)
        self.Solving_frame.place(x=10, y=160)
        self.Info_frame.place(x=10, y=320)

        self.show_maze()
        self.show_menu()
        self.show_solving()
        self.show_info()


    def show_menu(self):
        self.var1 = tkinter.StringVar()
        self.var1.set("None")
        non = tkinter.StringVar()
        non.set("None")
        var = tkinter.StringVar()
        var.set("30")
        spnbx_min = 20
        spnbx_max = 40

        def cut():
            self.columns = int(col_spnbx.get())
            print(self.columns)

        col_lbl = tkinter.Label(self.Menu_frame, text="Number of columns (" + str(spnbx_min) + "-" + str(spnbx_max) + "): ")
        col_spnbx = tkinter.Spinbox(self.Menu_frame, from_=spnbx_min, to=spnbx_max, textvariable=var, command=(lambda:cut()))
        rws_lbl = tkinter.Label(self.Menu_frame, state = "disabled", text="Number of rows (" + str(spnbx_min) + "-" + str(spnbx_max) + "): ")
        rws_spnbx = tkinter.Spinbox(self.Menu_frame,state = "disabled", from_=spnbx_min, to=spnbx_max)

        radio_btn = tkinter.LabelFrame(self.Menu_frame,text="Algorithms", width=298, height=50)
        DFS_btn = tkinter.Radiobutton(radio_btn,variable = self.var1, text="Recursive BackTracker        ", value="DFS")
        Binaryt_btn = tkinter.Radiobutton(radio_btn,variable = self.var1, text="Binary Tree              ", value="Binary")

        button_Frame = tkinter.Frame(self.Menu_frame, width=298, height=50)
        g = tkinter.Button(button_Frame, text="Generate", width=10, height=2, command= (lambda: self.generate(self.var1, False, True)))
        s = tkinter.Button(button_Frame, text="Simulate", width=10, height=2, command= (lambda: self.generate(self.var1, True, True)))
        c = tkinter.Button(button_Frame, text="Clear", width=10, height=2, command= (lambda: self.generate(non, False, True)))

        col_lbl.grid(column=0,row=0, sticky='NW')
        col_spnbx.grid(column=1,row=0, sticky='NW')
        rws_lbl.grid(column=0,row=1, sticky='NW')
        rws_spnbx.grid(column=1,row=1, sticky='NW')

        radio_btn.grid(column=0,row=2,columnspan=2, sticky='NW')
        DFS_btn.grid(column=0,row=0,columnspan=1, sticky='NW')
        Binaryt_btn.grid(column=1,row=0,columnspan=1, sticky='NW')

        button_Frame.grid(column=0, row=3, columnspan=2, sticky='NW')
        g.place(relx=0.2, rely=0.5, anchor=CENTER)
        s.place(relx=0.5, rely=0.5, anchor=CENTER)
        c.place(relx=0.8, rely=0.5, anchor=CENTER)

    def show_solving(self):
        self.var2 = tkinter.StringVar(None, "B")
        col_lbl = tkinter.Label(self.Solving_frame, text="Choose an Algorithm and Press Solve.                             ")
        col_lbl.grid(column=0, row=0, sticky='NW')

        radio_btn = tkinter.LabelFrame(self.Solving_frame,text="Algorithms", width=298, height=50)
        DFS_btn = tkinter.Radiobutton(radio_btn,variable = self.var2, text="DFS :Depth-first search", value="DFS")
        BFS_btn = tkinter.Radiobutton(radio_btn,variable = self.var2, text="BFS :Breadth-first search                                              ", value="BFS")

        radio_btn.grid(column=0,row=2,columnspan=2, sticky='NW')
        #DFS_btn.place(relx=0.2, rely=0.5, anchor=W)
        #BFS_btn.place(relx=0.6, rely=0.5, anchor=W)
        DFS_btn.grid(column=0,row=0,columnspan=1, sticky='NW')
        BFS_btn.grid(column=0,row=1,columnspan=1, sticky='NW')

        button_Frame = tkinter.Frame(self.Solving_frame, width=298, height=50)
        ss = tkinter.Button(button_Frame, text="Solve", width=10, height=2, command= (lambda: self.generate(self.var2, False, False)))
        s = tkinter.Button(button_Frame, text="Simulate", width=10, height=2, command= (lambda: self.generate(self.var2, True, False)))

        button_Frame.grid(column=0, row=3, columnspan=2, sticky='NW')
        ss.place(relx=0.3, rely=0.5, anchor=CENTER)
        s.place(relx=0.7, rely=0.5, anchor=CENTER)

    def show_info(self):

        def visit_profile():
            webbrowser.open('https://www.linkedin.com/in/khalidkousta/')

        mytext = "This is Maze 1.0 App, Thanks for using my App,\n" \
                 "This App was made by KHALID KOUSTA\n" \
                 "\nENJOY!!"
        info_lbl = tkinter.Label(self.Info_frame,text=mytext)
        info_lbl.place(x=10, y=40, anchor="w")

        ss = tkinter.Button(self.Info_frame, text="Visite Profile", width=10, height=2, command=(lambda: visit_profile()))
        ss.place(relx=0.45, rely=0.6, anchor=CENTER)

        info_lbl = tkinter.Label(self.Info_frame,text="Last update ###11/12/2020###")
        info_lbl.place(relx=0.45, rely=0.99, anchor='s')


    def show_maze(self):
        pass

    def generate(self, ctype, simulation, generat):
        # ---------------------------------Cell Class------------------------------
        class Cell:
            """A class to model a Cell"""

            def __init__(self, i, j):
                self.i = i
                self.j = j
                self.walls = [True, True, True, True]
                self.is_visited = False

            def show(self, canvas):
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

                if self.i == 0 and 0 < self.j < rows:
                    self.walls[0] = False
                    grid[index(self.i, self.j - 1)].walls[2] = False
                elif self.j == 0 and 0 < self.i < columns:
                    self.walls[3] = False
                    grid[index(self.i - 1, self.j)].walls[1] = False
                else:
                    # neighbors = random.choice([grid[index(self.i, self.j - 1)],grid[index(self.i - 1, self.j)]])
                    num = random.choice([0, 3])
                    self.walls[num] = False
                    if num == 0:
                        grid[index(self.i, self.j - 1)].walls[2] = False
                    else:
                        grid[index(self.i - 1, self.j)].walls[1] = False

                # return neighbors

            def check_neighbors(self, grid):
                neighbors = []

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

        # ------------------------------------------------------------------------
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

                if self.i:
                    left = maze[index(self.i - 1, self.j)]
                    if not left.is_visited and not left.walls[1]:
                        roads.append(left)
                if self.j:
                    top = maze[index(self.i, self.j - 1)]
                    if not top.is_visited and not top.walls[2]:
                        roads.append(top)
                if self.i < columns - 1:
                    right = maze[index(self.i + 1, self.j)]
                    if not right.is_visited and not right.walls[3]:
                        roads.append(right)
                if self.j < rows - 1:
                    bottom = maze[index(self.i, self.j + 1)]
                    if not bottom.is_visited and not bottom.walls[0]:
                        roads.append(bottom)

                if roads:
                    return roads
                else:
                    return None

        #---------------------------------------------------------------------
        class Goal:
            """A class to generate a random Goal"""

            def __init__(self):
                self.i = random.randint(0, columns - 1)
                self.j = random.randint(0, rows - 1)

            def show_goal(self, canvas):
                r = 5
                x = self.i * cell_size + r
                y = self.j * cell_size + r
                fx = self.i * cell_size + cell_size - r
                fy = self.j * cell_size + cell_size - r

                canvas.create_oval(x, y, fx, fy, fill='green')

            def show_start(self, canvas):
                r = 5
                x = self.i * cell_size + r
                y = self.j * cell_size + r
                fx = self.i * cell_size + cell_size - r
                fy = self.j * cell_size + cell_size - r

                canvas.create_oval(x, y, fx, fy, fill='red')
        #---------------------------------------------------------------------

        def is_win(m, g):
            if [m.i, m.j] == [g.i, g.j]:
                return True
            else:
                return False

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

        def setup_grid(Cell):
            for j in range(columns):
                for i in range(rows):
                    cell = Cell(i, j)
                    grid.append(cell)

        # Initialize variables
        columns = self.columns
        rows =  self.columns
        cell_size = round(self.canvas_size/self.columns,5)

        # Create the tkinter canvas
        sim_canvas = tkinter.Canvas(self.Maze_frame, width=self.canvas_size - 1, height=self.canvas_size - 1,
                                    highlightthickness=1, highlightbackground="black", bg='white')
        sim_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)


        if generat:
            # setup grid
            grid = []
            setup_grid(Cell)

            if ctype.get() == "DFS":
                current = grid[0]
                stack = []
                stack.append(current)
                if simulation:
                    print("Your choice is Recursive BackTracker Algorithm with Simulation")
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
                        else:
                            current = stack.pop()

                        # Update tkinter window
                        sim_window.update()
                        # sim_window.after(100)

                        # wipe the canvas clean
                        if len(stack) != 0:
                            sim_canvas.delete('all')
                else:
                    print("Your choice is Recursive BackTracker Algorithm without Simulation")
                    while len(stack) != 0:
                        current.is_visited = True
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
                        else:
                            current = stack.pop()

                    # Show
                    for i in range(len(grid)):
                        grid[i].show(sim_canvas)

            elif ctype.get() == "Binary":
                if simulation:
                        print("Your choice is Binary Tree Algorithm with simulation")
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
                            # sim_window.after(speed)
                else:
                    print("Your choice is Binary Tree Algorithm without Simulation")
                    for unit in range(1, len(grid)):
                        # Remove walls if there is
                        grid[unit].remove_walls(grid)

                        # new is old
                        old = grid[unit]

                    # Set Up playGround
                    for i in range(columns * rows):
                        grid[i].show(sim_canvas)
            else:
                print("Please choose an Algorithm")
                for i in range(columns * rows):
                    grid[i].show(sim_canvas)
            self.grid = grid.copy()

            # Show goal ans starting position
            self.goal = Goal()
            self.start = Goal()
            self.goal.show_goal(sim_canvas)
            self.start.show_start(sim_canvas)

        else:
            if ctype.get() == "DFS":
                if simulation:
                    print("Your choice is DFS Algorithm with Simulation")
                else:
                    print("Your choice is DFS Algorithm without Simulation")

            elif ctype.get() == "BFS":
                # Initialize Solving parameters
                mice = [Mouse(self.grid[index(self.start.i, self.start.j)])]
                mice[0].stack.append(self.grid[index(self.start.i, self.start.j)])
                self.grid[index(self.start.i, self.start.j)].is_visited = True
                GAME = False

                new_mice = []
                old_mice = []

                if simulation:
                    print("Your choice is BFS Algorithm with Simulation")
                    while not GAME:
                        print(len(mice))
                        # delete screen
                        sim_canvas.delete('all')

                        # Show maze
                        for i in range(columns * rows):
                            self.grid[i].show(sim_canvas)

                        # Highlight the goal
                        self.goal.show_goal(sim_canvas)

                        for mouse in mice:
                            # Check road
                            choice = mouse.check_roads(self.grid)

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

                            # Update tkinter window
                            sim_window.update()

                            # Show mice
                            mouse.show_mouse(sim_canvas)
                            # Check if reached
                            GAME = is_win(mouse, self.goal)
                            if GAME:
                                winner = mouse
                                break

                            # save hidden mice to a list
                            if not mouse.visible:
                                old_mice.append(mice.index(mouse))

                        # delete hidden mice
                        del mice[:len(old_mice)]
                        old_mice = []

                        mice.extend(new_mice)

                        # Update tkinter window
                        sim_window.update()

                else:
                    print("Your choice is BFS Algorithm without Simulation")
                    while not GAME:
                        # Highlight the goal
                        self.goal.show_goal(sim_canvas)

                        for mouse in mice:
                            # Check road
                            choice = mouse.check_roads(self.grid)

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
                            GAME = is_win(mouse, self.goal)
                            if GAME:
                                winner = mouse
                                break

                    # Update tkinter window
                    sim_window.update()

                # delete screen
                sim_canvas.delete('all')

                # Show maze
                for i in range(columns * rows):
                    self.grid[i].show(sim_canvas)

                # Show solution
                for unit in winner.stack:
                    unit.mark_as_solution(sim_canvas)

            else:
                print("Please choose an Algorithm")

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        os._exit(0)


#----------------------------------------------------------------------
if __name__ == "__main__":
    # Create the tkinter window
    sim_window = Tk()
    sim_window.protocol("WM_DELETE_WINDOW", on_closing)
    sim_window.geometry("840x540")
    sim_window.resizable(False, False)
    app = MyApp(sim_window)
    # Loop
    sim_window.mainloop()
