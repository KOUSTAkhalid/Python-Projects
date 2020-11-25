# Classes challenge 39: Epidemic Outbreak Terminal app
import random


class Simulation:
    """A class to control the simulation and help facilitate in the spread of the disease."""

    def __init__(self):
        """Initialise attributes"""
        self.day_number = 1

        # Get simulation initial conditions from the user
        print("To simulate an epidemic outbreak, we must know the population size.")
        self.population_size = int(input("---Enter the population size: "))

        # Get
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
    """A class to model an individual person in a population."""

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
        # A list to hold all the person instances once created
        self.population = []

        # Create the correct number of person instances based on the sim conditions
        for i in range(simulation.population_size):
            person = Person()
            self.population.append(person)

    def initial_infection(self, simulation):
        """Infect an initial portion of the population"""
        # The number of people to infect is found by taking the pop size * infection percentage
        # WE must round to 0 decimals and cast to an int so wee can use infected_count in a for loop
        infected_count = int(round(simulation.infection_percent * simulation.population_size, 0))

        # Infect the correct number of people
        for i in range(infected_count):
            # Infect the ith person in the population attribute
            self.population[i].is_infected = True
            self.population[i].days_infected = 1

        # Shuffle the population list so we spread the infection out randomly
        random.shuffle(self.population)

    def spread_infection(self, simulation):
        """Spread the infection to all adjacent people in the list population."""

        for i in range(len(self.population)):
            # ith person is ALIVE, see if they should be infected
            # Don't bother infect a dead person, they are infected and dead
            # Check to see if adjacent Persons are infected
            if not self.population[i].is_dead:
                # i is the first person in the list, can only check to the right.
                if i == 0:
                    if self.population[i + 1].is_infected:
                        self.population[i].infect(simulation)
                # i is in the middle of the list, can check to the left and right.
                elif len(self.population) - 1 > i > 0:
                    if self.population[i - 1].is_infected or self.population[i + 1].is_infected:
                        self.population[i].infect(simulation)
                # i is the last person in the list, can only check to the left
                elif i == len(self.population) - 1:
                    if self.population[i - 1].is_infected:
                        self.population[i].infect(simulation)

    def update(self, simulation):
        """Update the whole population by updating each individual person in the population."""
        simulation.day_number += 1

        # Call the update method for all person instances in the population
        for person in self.population:
            person.update(simulation)

    def display_statistics(self, simulation):
        """Display the current statistics of a population"""
        # Initialize values
        total_infected_count = 0
        total_death_count = 0

        # Loop through whole population
        for person in self.population:
            # Person is infected
            if person.is_infected:
                total_infected_count += 1
                # Person is dead
                if person.is_dead:
                    total_death_count += 1

        # Calculate percentage of population that is infected
        infected_percent = round(100 * (total_infected_count / simulation.population_size), 4)
        death_percent = round(100 * (total_death_count / simulation.population_size), 4)

        print("\n-----Day # " + str(simulation.day_number) + "-----")
        print("Percentage of population Infected: " + str(infected_percent) + "%")
        print("Percentage of Population Dead: " + str(death_percent) + "%")
        print("Total People Infected: " + str(total_infected_count) + " / " + str(simulation.population_size))
        print("Total Deaths: " + str(total_death_count) + " / " + str(simulation.population_size))

    def graphics(self):
        """A graphical representation for a population. O is healthy, I infected, X dead."""
        status = []
        for person in self.population:
            # Person is dead, X
            if person.is_dead:
                char = 'X'
            # Person is alive, are they infected ?
            elif person.is_infected:
                char = 'I'
            # Person is healthy, O
            else:
                char = 'O'
            status.append(char)

        # Print out all status characters separated by '-'
        for letter in status:
            print(letter, end='-')


# The main code

# Create a simulation object
sim = Simulation()

# Create a population object
pop = Population(sim)

# Set the initial infection conditions of the population
pop.initial_infection(sim)
pop.display_statistics(sim)
pop.graphics()
input("\nPress enter to begin the simulation...")

# Run simulation
for i in range(1, sim.sim_days):
    # For a single day, spread the infection,update the population, display statistics and graphics.
    pop.spread_infection(sim)
    pop.update(sim)
    pop.display_statistics(sim)
    pop.graphics()

    # If it is not the last day of the simulation, pause the program
    if i != sim.sim_days - 1:
        input("\nPress enter to advance to the next day.")
