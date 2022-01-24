from __future__ import annotations
from audioop import cross
import functools
import numpy as np
from random import sample, shuffle
from hard_constraints import hard_constraints_per_nurse, hard_constraints_per_schedule
from soft_constraints import soft_constraints
from timetable import timetable
import math
from copy import deepcopy
from typing import Tuple

class Survivor():
    hard_constraints_per_nurse = hard_constraints_per_nurse
    hard_constraints_per_schedule = hard_constraints_per_schedule
    soft_constraints = soft_constraints

    def __init__(self, timetable: timetable, iteration: int, schedule: list = None, mutation_rate: float = 0.03, crossover_rate: float = 0.9) -> None:
        self.timetable = timetable
        self.nurse_count = 0
        self.shift_generations = 0 
        self.iteration = iteration
        self.fitness = 'pain'
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.nurse_assignments = [[[-1] for day in range(0, self.timetable.days)] for assignment in range(0, self.timetable.nurses)]
        if schedule is not None:
            self.nurse_assignments = schedule
        else:
            self.generate_nurse_assignments()
        
        self.fitness = self.evaluate_fitness()
        
    def __str__(self) -> str:
        return "\nNurse_assignments:\n" + "\n".join(["Nurse {}: {}".format(i, self.nurse_assignments[i]) for i in range(0, self.timetable.nurses)]) + '\nNurses Generated: ' + str(self.nurse_count) + '\nIteration: ' + str(self.iteration) + '\n' + self.constraint_violations + '\nFitness: ' + str(self.fitness)

    def generate_nurse_assignments(self):
        while True:
            self.nurse_assignments = [[[0] * self.timetable.shifts for day in range(0, self.timetable.days)] for assignment in range(0, self.timetable.nurses)]
            for day in range(0, self.timetable.days):
                daily_selected_nurses = self.select_nurses_for_day(day)
                for shift in range(0, self.timetable.shifts):
                    shift_selected_nurses = self.select_nurses_for_shift(daily_selected_nurses, day, shift)
                    self.fill_in_nurse_assignments(shift_selected_nurses, day, shift)
             
            self.nurse_count += self.timetable.nurses
            if not self.check_hard_constraints():
                continue
            
            return
    
    def check_hard_constraints(self, nurse_assignments: list = None):
        nurse_assignments = nurse_assignments if nurse_assignments is not None else self.nurse_assignments
        for nurse in range(0, len(nurse_assignments)):
            if not all([constraint(self.timetable, nurse_assignments[nurse]) for constraint in self.hard_constraints_per_nurse]):
                return False
        if not all([constraint(self.timetable, nurse_assignments) for constraint in self.hard_constraints_per_schedule]):
            return False

        return True
     
    def fill_in_nurse_assignments(self, available_nurses: list, day: int, shift: int) -> None:
        for nurse in available_nurses:
            self.nurse_assignments[nurse][day][shift] = 1
    
    def select_nurses_for_day(self, day: int) -> list:
        daily_required_nurses = sum(self.timetable.required_nurses[day][0:self.timetable.shifts])
        daily_selected_nurses = []
        counter = 0
        while len(daily_selected_nurses) < daily_required_nurses:
            counter += 1
            nurses_to_select = self.timetable.nurses if (daily_required_nurses - len(daily_selected_nurses)) > self.timetable.nurses else daily_required_nurses - len(daily_selected_nurses)
            selected_nurse = sample(range(0, self.timetable.nurses), nurses_to_select)
            if counter > 1000: 
                raise "Too many iterations selecting nurses for day" 
            
            for nurse in selected_nurse: 
                if self.timetable.max_shifts > daily_selected_nurses.count(nurse): 
                    daily_selected_nurses.append(nurse) 
            
        return daily_selected_nurses 
    
    def select_nurses_for_shift(self, available_nurses: list, day: int, shift: int) -> list: 
        counter = 0 
        while True: 
            counter += 1 
            if counter > 500: 
                counter = 0 
                selected_nurses = [] 
            
            selected_nurses = sample(available_nurses, self.timetable.required_nurses[day][shift]) 
            # print(self.iteration, self.timetable, self, selected_nurses, available_nurses, day, shift, len(set(selected_nurses)) == len(selected_nurses), all([available_nurses.count(nurse) <= self.timetable.shifts - shift - 1 for nurse in available_nurses if nurse not in selected_nurses]), not any([day != 0 and shift == 0 and self.nurse_assignments[nurse][day - 1][self.timetable.shifts - 1] for nurse in selected_nurses])) 
            if not len(set(selected_nurses)) == len(selected_nurses): 
                continue 
            if not all([available_nurses.count(nurse) <= self.timetable.shifts - shift - 1 for nurse in available_nurses if nurse not in selected_nurses]): 
                continue
        # if any([day != 0 and shift == 0 and self.nurse_assignments[nurse][day - 1][self.timetable.shifts - 1] for nurse in selected_nurses]):
        #    continue

            for nurse in selected_nurses:
                available_nurses.remove(nurse)
            return selected_nurses
    
    def crossover(self, other: Survivor) -> Tuple[Survivor, Survivor]: 
        if np.random.randint(0, 100) > self.crossover_rate * 100:
            return (self, other)
            
        # Choosing a 50 50 crossover ratio
        # multiple techniques I could try here but I'm too dumb so I'm just gonna split fifty fifty based on rng
        bisecting_point = np.random.randint(0, self.timetable.days)
        cross_over_nurse_assignments1 = []
        cross_over_nurse_assignments2 = []
        while True:
            for (nurse1, nurse2) in zip(self.nurse_assignments, other.nurse_assignments):
                cross_over_nurse_assignments1.append(nurse1[:bisecting_point] + nurse2[bisecting_point:])
                cross_over_nurse_assignments2.append(nurse2[:bisecting_point] + nurse1[bisecting_point:])
            
            # print('old 1')
            # print("\n".join(["Nurse {}: {}".format(i, other.nurse_assignments[i]) for i in range(0, self.timetable.nurses)]))
            # print('old 2')
            # print("\n".join(["Nurse {}: {}".format(i, self.nurse_assignments[i]) for i in range(0, self.timetable.nurses)]))
            # print('new')
            # print("\n".join(["Nurse {}: {}".format(i, cross_over_nurse_assignments[i]) for i in range(0, self.timetable.nurses)]))
            if not self.check_hard_constraints(cross_over_nurse_assignments1) and self.check_hard_constraints(cross_over_nurse_assignments2):
                bisecting_point += sample([-1, 1], 1)[0]
                cross_over_nurse_assignments1 = cross_over_nurse_assignments2 = []
                continue
        
            survivor1 = Survivor(self.timetable, self.iteration + 1, cross_over_nurse_assignments1, mutation_rate=self.mutation_rate, crossover_rate=self.crossover_rate)
            survivor2 = Survivor(self.timetable, self.iteration + 1, cross_over_nurse_assignments2, mutation_rate=self.mutation_rate, crossover_rate=self.crossover_rate)
            return (survivor1, survivor2)
            
    def mutation(self) -> None:
        if np.random.randint(0, 99) < self.mutation_rate * 100:
            counter = 0
            while True:
                if counter > self.timetable.nurses * self.timetable.days * self.timetable.shifts * 2:
                    return
                random_nurse = np.random.randint(0, self.timetable.nurses)
                random_day = np.random.randint(0, self.timetable.days)
                random_shift = np.random.randint(0, self.timetable.shifts)
                self.nurse_assignments[random_nurse][random_day][random_shift] ^= 1 
                if not self.check_hard_constraints():
                    self.nurse_assignments[random_nurse][random_day][random_shift] ^= 1
                    counter += 1
                    continue
                
                return
                
    def __lt__(self, other: Survivor = None) -> bool:
        if other is None:
            return True
        
        return self.fitness > other.fitness
    
    def evaluate_fitness(self) -> int:
        results = [constraint(self.timetable, self.nurse_assignments) for constraint in soft_constraints]
        self.constraint_violations = '\n'.join([f'{constraint.__name__}: {str(result)}' for result, constraint in zip(results, soft_constraints)])
        return sum(results)
        
class Generation:
    def __init__(self, generation_size: int, timetable: timetable, generation_number: int, survivors: list = None, amount_survivors: int = None, mutation_rate: float = 0.03, crossover_rate: float = 0.9) -> None:
        self.generation_size = generation_size
        self.timetable = timetable
        self.generation_number = generation_number
        self.mutation_rate = mutation_rate 
        self.crossover_rate = crossover_rate
        self.amount_survivors = amount_survivors if amount_survivors is not None else round(self.generation_size / 2)
        self.survivors = survivors if survivors is not None else []
        self.fill_empty_population()
        # Implement a method that guarantees a proportion
        self.best_survivor = functools.reduce(lambda x, y: x if x > y else y, self.survivors) 
     
    def __str__(self):
        return f"Generation Number: {self.generation_number}\n" + "\n".join([str(survivor) for survivor in self.survivors]) + '\n'
    
    def generate_until(self, generation_number: int = None, desired_fitness: int = None) -> Tuple[Generation, Survivor]:
        if generation_number is None and desired_fitness is None:
            raise 'Must specify either generation number or desired fitness'
        
        current_generation = self
        min = math.inf
        desired_fitness = desired_fitness if desired_fitness is not None else -1
        generation_number = generation_number if generation_number is not None else math.inf
        counter = 0
        best_survivor_so_far = self.best_survivor
        
        while current_generation.generation_number < generation_number or current_generation.best_survivor.fitness < desired_fitness:
            if current_generation.best_survivor.fitness < min:
                min = current_generation.best_survivor.fitness
                best_survivor_so_far = current_generation.best_survivor
                
            average = sum([survivor.fitness for survivor in current_generation.survivors]) / len(current_generation.survivors)        
            counter += 1
            
            # print(f"\ngen: {current_generation.generation_number}\nmin {min}\ncounter: {counter}\nbest_current:  {current_generation.best_survivor.fitness}\naverage: {average}")
            current_generation = current_generation.select_next_generation()

        # print(best_survivor_so_far)
        
        return (Generation, best_survivor_so_far)

    def fill_empty_population(self):
        # print('empty', self.generation_size - len(self.survivors))
        while len(self.survivors) < self.generation_size:
            survivor = Survivor(self.timetable, self.generation_number, mutation_rate=self.mutation_rate, crossover_rate=self.crossover_rate)
            self.survivors.append(survivor)  

    def select_next_generation(self) -> Generation:          
        best_survivors = self.determine_parents()
        children = []
        
        for pair in generate_random_pairs(best_survivors):
            child1, child2 = pair[0].crossover(pair[1])
            child1.mutation()
            child2.mutation()
            children.extend([child1, child2])
        
        return Generation(self.generation_size, self.timetable, self.generation_number + 1, children, self.amount_survivors)    
        
    def determine_parents(self) -> list:
        self.survivors.remove(self.best_survivor)
        while True:
            random_survivors = sample(self.survivors, self.amount_survivors * 2) if self.amount_survivors * 2 < len(self.survivors) else self.survivors
            if len(set(random_survivors)) == len(random_survivors):
                break
            
        self.survivors.append(self.best_survivor)
        best_survivors = []
        for pair in generate_random_pairs(random_survivors):
            better_survivor = pair[0] if pair[0] > pair[1] else pair[1]
            best_survivors.append(better_survivor)

        return best_survivors

def generate_random_pairs(list: list) -> list:
    shuffle(list)
    while len(list) > 2:
        pair1 = list.pop()
        pair2 = list.pop() 
        yield (pair1, pair2)



