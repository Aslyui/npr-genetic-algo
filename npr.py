import random
import math
import itertools
import numpy as np
     
class Shifts:
    def __init__(self, nurses: int, days: int, shifts: int, minimum_nurses: int, maximum_nurses: int) -> None:
        self.nurses = nurses
        self.days = days
        self.shifts = shifts
        self.minimum_nurses = minimum_nurses
        self.maximum_nurses = maximum_nurses
        self.required_nurses = self.generate_required_nurses()
        self.nurse_preferences = self.generate_nurse_preferences()

    def __str__(self) -> str:
        preferences = "\n".join(["Nurse {}: {}".format(i, self.nurse_preferences[i]) for i in range(0, self.nurses)])
        return f"""Nurses: {self.nurses}
Days: {self.days}
Shifts: {self.shifts}
Minimum_nurses: {self.minimum_nurses}
Maximum_nurses: {self.maximum_nurses}
Required_nurses: 
{self.required_nurses}
Nurse_preferences: 
{preferences}"""
                
    def generate_required_nurses(self) -> list:
        return np.random.randint(self.minimum_nurses, self.maximum_nurses, size=(self.days, self.shifts))

    def generate_nurse_preferences(self) -> list:
        for i in range(0, self.nurses):
            nurse_preferences = []
            while len(nurse_preferences) < self.nurses:
                nurse_preference = np.random.randint(1, 5, size=self.days * self.shifts)
                nurse_preferences.append(nurse_preference.tolist() if sum(nurse_preference.tolist()) < 5 * self.days * self.shifts else None)

            return nurse_preferences

class Survivor:
    constraints = {}
    def __init__(self, schedule: Shifts) -> None:
        self.schedule = schedule
        self.nurse_availabilities = self.generate_nurse_availabilities(schedule)
    
    def generate_nurse_availabilities(self, schedule: Shifts) -> list:
        self.schedule.
    
    def crossover():
        pass
        
    def mutation():
        pass
    
    def evaluate_fitness():
        pass
    
class Generation:
    def __init__(self, generation_size: int, survivors: list, schedule: Shifts, generation_number: int) -> None:
        self.generation_size = generation_size
        self.survivors = survivors
        self.generation_number = generation_number
        self.best_survivor = max(survivors, key=lambda survivor: survivor.fitness)
        self.max_fitness = self.best_survivor.fitness
    
    def mutate_until(self, generation_number: int, desired_fitness: int ):
        current_generation = self    
        while current_generation.generation_number < generation_number or current_generation.fitness < desired_fitness:
            current_generation = current_generation.select_next_generation()

    def select_next_generation(self):          
        best_survivors = self.determine_best_survivors()
        children = []
        for pair in generate_random_pairs(best_survivors):
            children.append(pair[0].crossover(pair[1]).mutation())
            
        while len(children) < self.generation_size:
            children.append(Survivor(self.shifts))            
            
        return Generation(children, self.generation_number + 1)    
        
    def determine_best_survivors(self) -> list:
        random_survivors = random.sample(self.survivors.remove(list(self.best_survivor)), random.randint(1, len(self.survivors) / 2))
        best_survivors = [self.best_survivor]
        for pair in generate_random_pairs(random_survivors):
            best_survivors.append(better_survivor = pair[1] if pair[1].fitness > pair[2].fitness else pair[2])
            
        return best_survivors

def generate_random_pairs(list: list) -> list:
    while 1 < len(list):
        pair1 = list.pop(random.randint(0, len(list) - 1))
        pair2 = list.pop(random.randint(0, len(list) - 1))
        yield (pair1, pair2)
        
print(Shifts(6, 3, 3, 2, 5))

