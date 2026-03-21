import pygame

class population():
    def __init__(self):
        self.unemployed_population = 0
        self.employed_population = 0
        self.population = self.unemployed_population + self.employed_population
        self.company_sol = 5
        self.rich_population = round(self.population * 0.01)
        self.retired_population = 0
        self.potential_positions = 0
        self.workable = 0
        

    def update(self, housing, maximum_positions):

        self.population = housing

        self.rich_population = round(self.population * 0.01)
        self.retired_population = self.rich_population + (self.population * 0.10)

        self.workable = self.population - self.retired_population

        if maximum_positions > self.population:
            self.potential_positions = maximum_positions - self.population
            self.unemployed_population = 0
            self.employed_population = self.population
        else:
            self.potential_positions = 0
            self.unemployed_population = self.population - maximum_positions