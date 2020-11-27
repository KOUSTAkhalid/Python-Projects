import tkinter
import random
import keyboard


class Snake:
    """A class to model the whole Snake."""

    def __init__(self, col, row):
        """Initialize attributes"""
        self.snake_size = 3
        self.x = random.randint(self.snake_size, (col - self.snake_size))
        self.y = random.randint(self.snake_size, (row - self.snake_size))

        # Generates snake in the specific coordinates
        self.snake_cord = [[self.x, self.y],[self.x, self.y+1],[self.x, self.y+2]]

        """
        for i in range(self.s_init_size - 1):
            rand_x = random.randint(-1, 1)
            if rand_x == 0:
                rand_y = random.choice([-1, 1])
            else:
                rand_y = 0

            self.snake_cord.append([self.x + rand_x, self.y + rand_y])
        """


    def show(self, canvas):
        global cell_size

        for unit in self.snake_cord:
            x = unit[0] * cell_size
            y = unit[1] * cell_size
            canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='black')

    def move(self, direction):
        direc = 0
        t = -1

        # for each direction
        if direction == "up":
            direc = 1
            t = -1
        elif direction == "down":
            direc = 1
            t = 1
        elif direction == "right":
            direc = 0
            t = 1
        elif direction == "left":
            direc = 0
            t = -1

        # Update snake coordinates
        new_cord = self.snake_cord[0].copy()
        new_cord[direc] = self.snake_cord[0][direc] + t
        self.snake_cord.insert(0,new_cord)
        del self.snake_cord[self.snake_size:]

        # If Snake is out of playground (x axis)
        if self.snake_cord[0][0] < 0:
            self.snake_cord[0][0] = columns-1
        elif self.snake_cord[0][0] >= columns:
            self.snake_cord[0][0] = 0

        # If Snake is out of playground (y axis)
        if self.snake_cord[0][1] < 0:
            self.snake_cord[0][1] = rows-1
        elif self.snake_cord[0][1] >= rows:
            self.snake_cord[0][1] = 0

class Apple:
    """A class to model an apple for the snake."""

    def __init__(self):
        self.x = random.randint(0, columns-1)
        self.y = random.randint(0, rows-1)
        self.is_eaten = True

    def new_apple(self, canvas, s):
        """Generate a new apple each time it was eaten."""
        if self.is_eaten:
            while True:
                self.x = random.randint(0, columns-1)
                self.y = random.randint(0, rows-1)

                for item in s.snake_cord:
                    if [self.x,self.y] == item:
                        break
                    else:
                        continue
                break

            # make apple is not eaten

    def show_apple(self, canvas):
        x = self.x * cell_size
        y = self.y * cell_size
        canvas.create_oval(x, y, x + cell_size, y + cell_size, fill='red')

class Cell:
    """A class to model the whole ground."""

    def __init__(self, i, j):
        """Initialize attributes"""
        self.i = i
        self.j = j

    def show(self, canvas):
        global cell_size
        x = self.i * cell_size
        y = self.j * cell_size

        #canvas.create_rectangle(x, y, x+cell_size, y+cell_size, fill='white')

def key_event():
    global key_direction
    if keyboard.is_pressed('up'):  # if key 'up' is pressed
        return "up"
    elif keyboard.is_pressed('down'):  # if key 'down' is pressed
        return "down"
    elif keyboard.is_pressed('right'):  # if key 'right' is pressed
        return "right"
    elif keyboard.is_pressed('left'):  # if key 'left' is pressed
        return "left"
    else:
        return key_direction

def check_collision(s):
    if s.snake_cord[0] in s.snake_cord[1:]:
        return True
    else:
        return False

def check_food(s, a):
    if s.snake_cord[1] == [a.x, a.y]:
        s.snake_size += 1
        return True
    else:
        return False


# Set constant variables for window size
WINDOW_SIZE = 400
cell_size = 20
columns = int(WINDOW_SIZE / cell_size)
rows = int(WINDOW_SIZE / cell_size)
grid = []
collide = False
key_direction = "up"

# Snake Variables
speed = 100

# Create the tkinter window and canvas
sim_window = tkinter.Tk()
sim_window.title("Maze GENERATOR")
sim_window.resizable(0, 0)
sim_canvas = tkinter.Canvas(sim_window, width=WINDOW_SIZE, height=WINDOW_SIZE, highlightthickness=0, bg='white')
sim_canvas.pack(side=tkinter.LEFT)

# setup Ground
for j in range(columns):
    for i in range(rows):
        cell = Cell(i, j)
        grid.append(cell)

# Create apple
apple = Apple()


while True:
    # Generate Snake
    snake = Snake(columns, rows)
    collide = False
    key_direction = 'up'

    # Run the simulation
    while not collide:
        # delete screen
        sim_canvas.delete('all')

        # Show playGround
        for i in range(columns*rows):
            grid[i].show(sim_canvas)

        # Show Snake
        snake.show(sim_canvas)

        # Check keyboard
        key_direction = key_event()

        # Move Snake
        snake.move(key_direction)

        # check if apple was eaten, if it is create a new one
        if check_food(snake, apple):
            apple.new_apple(sim_canvas, snake)
        apple.show_apple(sim_canvas)

        # Check collusion
        collide = check_collision(snake)

        # Update tkinter window
        sim_window.update()

        # Speed of simulation
        sim_window.after(speed)


    choice = input("GAME OVER!! play again (y/n): ")
    if choice != 'y':
        print("\nThanks for playing!!"
              "\n\nThis game was made by: ---KOUSTA KHALID---")
        break