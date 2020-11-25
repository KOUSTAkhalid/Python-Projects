# Classes Challenge 40: Epidemic Outbreak GUI App


import math
import random
import tkinter
import matplotlib
import matplotlib.pyplot as plt

class Simulation:
    """A class to control a simulation and facilitate the spread of a disease."""

    def __init__(self):
        """Initialize attributes"""
        self.day_number = 1

        # Get simulation initial conditions from the user

        # Population size must be a perfect square for this program
        print("To simulate an epidemic outbreak, we must know the population size.")
        self.population_size = int(input("---Enter the population size: "))

        # Convert users population size to nearest perfect square for visual purposes
        root = math.sqrt(self.population_size)  # For example, if population_size is 79, root = 8.8881

        # User did not enter a perfect square for the population
        if root - int(root) != 0:  # 8.8881 - 8 != 0
            root = round(root, 0)  # round(8.8881, 0) = 9.0
            self.grid_size = int(root)  # grid_size = 9
            self.population_size = self.grid_size**2  # population_size = 81 THE CLOSEST PERFECT SQUARE
            print("Rounding population size to " + str(self.population_size) + " for visual purposes.")
        # The user did enter a perfect square for the population
        else:
            self.grid_size = int(root)

        print("\nWE must first start by infecting a portion of the population.")
        self.infection_percent = float(input("---Enter the percentage(0-100) of the population to initially infect: "))
        self.infection_percent /= 100

        print("\nWE must know the risk a person has to contract the disease when exposed.")
        self.infection_probability = float(input("---Enter the probability (0-100) that a person gets infected when "
                                                 "exposed to the disease: "))

        print("\nWE must know how long the infection will last when exposed.")
        self.infection_duration = int(input("---Enter the duration in (days) of the infection: "))

        print("\nWe must know the mortality rate of those infected.")
        self.mortality_rate = float(input("---Enter the mortality rate (0-100) of the infection: "))

        print("\nWE must know how long to run the simulation.")
        self.sim_days = int(input("---Enter the number of days to simulate: "))


class Person:
    """A class to model an individual person."""

    def __init__(self):
        """Initialize attributes"""
        self.is_infected = False  # Person starts healthy, not infected
        self.is_dead = False  # person starts alive
        self.days_infected = 0  # keeps track of days infected for individual person

    def infect(self, simulation):
        """Infect a person based on sim conditions"""
        if random.randint(0, 100) < simulation.infection_probability:
            # random number generated must be less than infection probability to infect
            self.is_infected = True

    def heal(self):
        """Heals a person from an infection"""
        self.is_infected = False
        self.days_infected = 0

    def die(self):
        """Kill a person"""
        self.is_dead = True

    def update(self, simulation):
        """Update an individual person if the person is not dead. check if they are infected, If they are,
        increase the days infected count, then check if they should die or be healed """
        # Check if the person is not dead before updating
        if not self.is_dead:
            # Check if the person is infected
            if self.is_infected:
                self.days_infected += 1
                if random.randint(0, 100) < simulation.mortality_rate:
                    self.die()
                elif self.days_infected >= simulation.infection_duration:
                    self.heal()


class Population:
    """A class to model a whole population of person objects"""

    def __init__(self, simulation):
        """Initialize attributes"""

        # A list of N lists: NxN
        self.population = []  # A list to hold all Persons in the population.

        # Loop through the needed number of rows
        for i in range(simulation.grid_size):
            row = []
            # Loop through the needed of person objects for each row
            for j in range(simulation.grid_size):
                person = Person()
                row.append(person)
            # The entire row is complete, append it to the population
            self.population.append(row)

    def initial_infection(self, simulation):
        """Infect an initial portion of the population based on initial conditions of the sim"""
        # Infect the infection_percent*population_size gives the total number to infect.
        # Round to 0 decimals and cast to int so it can be used in a loop.
        infected_count = int(round(simulation.infection_percent*simulation.population_size, 0))

        infection = 0
        # Infect the population until you have infected the correct starting amount
        while infection < infected_count:
            # x is a random row in the population, y is a random person in the random row
            # self.population[x][y] represents a random person in the population list
            x = random.randint(0, simulation.grid_size - 1)
            y = random.randint(0, simulation.grid_size - 1)

            if not self.population[x][y].is_infected:
                self.population[x][y].is_infected = True
                self.population[x][y].days_infected = 1
                infection += 1

    def spread_infection(self, simulation):
        """Spread the infection in a 2D array to all adjacent people to a given person.
           A given person in the population attribute is referenced as self.population[i][j]
           A person to the right of the given person is referenced as self.population[i][j+1]
           A person to the left of the given person is referenced as self.population[i][j-1]
           A person below given person is referenced as self.population[i+1][j]
           A person above given person is referenced as self.population[i-1][j]"""

        # Loop through all rows of the population
        for i in range(simulation.grid_size):
            # Loop through all of the Person objects in a given row
            for j in range(simulation.grid_size):
                # Check to see if this given person self.population[i][j] is not dead
                if not self.population[i][j].is_dead:
                    # Check to see if we need to infect this person
                    # We will try infect the given person is already infected
                    # If i == 0, we are in the first row
                    if i == 0:
                        # If j == 0, we are in the first column, so we can't look left.
                        if j == 0:
                            if self.population[i][j+1].is_infected or self.population[i+1][j].is_infected:
                                self.population[i][j].infect(simulation)
                        # If we are in the last column we can't look right
                        elif j == simulation.grid_size-1:
                            if self.population[i][j-1].is_infected or self.population[i+1][j].is_infected:
                                self.population[i][j].infect(simulation)
                        # Check all direction
                        else:
                            if self.population[i][j - 1].is_infected or self.population[i][j+1].is_infected or self.population[i+1][j].is_infected:
                                self.population[i][j].infect(simulation)

                    # If we are in the last row
                    elif i == simulation.grid_size-1:
                        # If j == 0, we are in the first column, so we can't look left.
                        if j == 0:
                            if self.population[i][j+1].is_infected or self.population[i-1][j].is_infected:
                                self.population[i][j].infect(simulation)
                        # If we are in the last column we can't look right
                        elif j == simulation.grid_size-1:
                            if self.population[i][j-1].is_infected or self.population[i-1][j].is_infected:
                                self.population[i][j].infect(simulation)
                        # Check all direction
                        else:
                            if self.population[i][j - 1].is_infected or self.population[i][j+1].is_infected or self.population[i-1][j].is_infected:
                                self.population[i][j].infect(simulation)

                    # Otherwise we are in a row in between, we can look left, right, above or below
                    else:
                        # If j == 0, we are in the first column, so we can't look left.
                        if j == 0:
                            if self.population[i][j+1].is_infected or self.population[i-1][j].is_infected or self.population[i+1][j].is_infected:
                                self.population[i][j].infect(simulation)
                        # If we are in the last column we can't look right
                        elif j == simulation.grid_size-1:
                            if self.population[i][j-1].is_infected or self.population[i-1][j].is_infected or self.population[i+1][j].is_infected:
                                self.population[i][j].infect(simulation)
                        # Check all direction
                        else:
                            if self.population[i][j - 1].is_infected or self.population[i][j+1].is_infected or self.population[i-1][j].is_infected or self.population[i+1][j].is_infected:
                                self.population[i][j].infect(simulation)

    def update(self, simulation):
        """Update the whole population by updating each individual Person"""
        simulation.day_number += 1
        # Loop through the population to access each row
        for row in self.population:
            # Loop through the row to update each person
            for person in row:
                person.update(simulation)

    def display_statistics(self, simulation):
        """Display the statistics of the population"""
        global x
        # Initialize values
        total_infected_count = 0
        total_death_count = 0

        # Loop through the population to access each row
        for row in self.population:
            # Loop through the row to update each person
            for person in row:
                if person.is_infected:
                    # Person is infected
                    total_infected_count += 1
                    if person.is_dead:
                        # Person is dead
                        total_death_count += 1

        # Calculate percentage of population that is infected
        infected_percent = round(100 * (total_infected_count / simulation.population_size), 4)
        x.append(infected_percent)
        death_percent = round(100 * (total_death_count / simulation.population_size), 4)

        # Statistics summary
        print("\n-----Day # " + str(simulation.day_number) + "-----")
        print("Percentage of population Infected: " + str(infected_percent) + "%")
        print("Percentage of Population Dead: " + str(death_percent) + "%")
        print("Total People Infected: " + str(total_infected_count) + " / " + str(simulation.population_size))
        print("Total Deaths: " + str(total_death_count) + " / " + str(simulation.population_size))


# A helper function to create graphics
def graphics(simulation, population, canvas):
    """A helper function to update the tkinter display."""
    # Get the dimensions of an individual square in a grid
    # Each square represents a person in the population
    # Use 600 for a GUI window that is 600x600, change if desired.
    # To get the dimensions of a square, take the dimensions of the window and divide by total number of squares in a row
    square_dimension = 600//simulation.grid_size

    # Loop through all rows in the population
    for i in range(simulation.grid_size):
        # y is the starting index of where a given square should be drawn
        y = i*square_dimension
        for j in range(simulation.grid_size):
            # x is the starting index of where a given square should be drawn.
            x = j*square_dimension

            # Check to see if the given person is dead
            if population.population[i][j].is_dead:
                # Create a red square at the correct location
                canvas.create_rectangle(x, y, x+square_dimension, y+square_dimension, fill='red')
            # Check to see if the given person is infected
            elif population.population[i][j].is_infected:
                # Create a yellow square at the correct location
                canvas.create_rectangle(x, y, x+square_dimension, y+square_dimension, fill='yellow')
            else:
                # Create a green square at the correct location
                canvas.create_rectangle(x, y, x+square_dimension, y+square_dimension, fill='green')


# The main code
x = []
y = [0]
# Create a simulation Object
sim = Simulation()

# Set constant variables for window size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Create the tkinter window and canvas
sim_window = tkinter.Tk()
sim_window.title("Epidemic Outbreak Simulator")
sim_canvas = tkinter.Canvas(sim_window, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, bg = 'lightblue')
sim_canvas.pack(side=tkinter.LEFT)

# Create a population Object
pop = Population(sim)

# Set the initial condition of the population
pop.initial_infection(sim)
pop.display_statistics(sim)
input("Press Enter to begin simulation...")

# Run the simulation
for i in range(1,sim.sim_days):
    pop.spread_infection(sim)
    pop.update(sim)
    pop.display_statistics(sim)
    graphics(sim, pop, sim_canvas)

    # Update tkinter window
    sim_window.update()

    # If we are currently not on the last day of the simulation, wipe the canvas clean
    if i < sim.sim_days-1:
        sim_canvas.delete('all')

    y.append(sim.day_number)

plt.plot(y,x)
plt.show()
input("---Simulation finished---\nPress Enter to EXIT")