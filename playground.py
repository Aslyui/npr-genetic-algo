from timetable import timetable
from genetic_algo import Survivor, Generation
import math

# my generator algo is dodgy and breaks randomly for very specific timetabls
nurse_preferences = [[[1, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]], [[0, 1, 0], [0, 1, 0], [1, 0, 0], [0, 0, 1], [0, 0, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]], [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]], [[0, 0, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 0, 1], [0, 0, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0]], [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]]]
required_nurses = [[2, 1, 2], [2, 2, 2], [2, 1, 1], [1, 2, 2], [2, 1, 1], [2, 1, 2], [1, 2, 1], [2, 1, 1], [2, 1, 2], [2, 2, 2]]
# ipray = timetable(nurses=5, days=10, shifts=3, minimum_nurses=1, maximum_nurses=2, nurse_preferences=nurse_preferences, required_nurses=required_nurses)

new_nurse_preferences = [[[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [1, 0, 0], [1, 0, 0]], [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0]], [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 0, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]], [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]], [[0, 1, 0], [1, 0, 0], [1, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 1, 0], [0, 0, 1], [0, 0, 1], [0, 1, 0], [0, 1, 0], [0, 0, 1], [0, 0, 1], [0, 1, 0], [0, 0, 1], [0, 0, 1], [1, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 1, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]], [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]], [[1, 0, 0], [1, 0, 0], [0, 1, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 0, 1], [1, 0, 0], [1, 0, 0], [0, 1, 0]], [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [1, 0, 0], [1, 0, 0], [0, 0, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 0, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]], [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 0, 0], [0, 0, 1], [0, 0, 1], [0, 1, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1]], [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 0, 0]], [[1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 0, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 0, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]]]
new_nures_requirements = [[3, 3, 4], [3, 3, 3], [3, 4, 4], [3, 3, 4], [3, 4, 3], [4, 3, 3], [4, 4, 4], [4, 4, 3], [3, 3, 4], [4, 4, 4], [3, 4, 3], [3, 3, 3], [3, 3, 3], [3, 4, 3], [4, 3, 4], [3, 4, 3], [4, 4, 3], [3, 4, 3], [3, 3, 4], [3, 4, 4], [3, 3, 4], [3, 4, 4], [4, 3, 4], [4, 4, 4], [3, 4, 3], [4, 4, 3], [3, 4, 4], [4, 3, 3], [3, 3, 3], [4, 4, 3]]
killme = timetable(nurses=11, days=30, shifts=3,minimum_nurses=3, maximum_nurses=4)

# thonk = Generation(generation_size=80, timetable=new, generation_number=0, mutation_rate=0.05, crossover_rate=0.95).generate_until(generation_number=100)[1].fitness

# min = math.inf
# for i in range(0, 8000):
#     hmm = Survivor(new, i)
#     if hmm.fitness < min:
#         best_survivor = hmm
#     min = best_survivor.fitness
# print(best_survivor)

print(killme)

with open('out.txt', 'w') as f:
    f.write(str(killme))

sum = 0
for i in range(0, 50):
    thonk = Generation(generation_size=80, timetable=killme, generation_number=0, mutation_rate=0.25, crossover_rate=0.95).generate_until(generation_number=200)[1].fitness
    print(thonk, 'generation', i)
    sum += thonk
    
print('generation average', sum / 50)
    


# for i in range(0, 100):
#     sum += Generation(80, new, 0, mutation_rate=0.05).generate_until(120, 29)[1].fitness
    
# print(sum / 100)
 

sum = 0
for i in range(0, 50):
    min = math.inf
    best_survivor = None
    for i in range(0, 8000):
        hmm = Survivor(killme, i)
        if hmm.fitness < min:
            best_survivor = hmm
        min = best_survivor.fitness
    sum += min
    print(min, 'random 1')
print(sum / 50, 'random average')

min = math.inf
best_survivor = None
for i in range(0, 1000000):
    hmm = Survivor(killme, i)
    if hmm.fitness < min:
        best_survivor = hmm
    min = best_survivor.fitness

print(min)
print(best_survivor)
# sum = 0


# Loosen the restrictions on the hard constraints and move them to the soft constraints
# Include weekends in soft constraints
# Include a grouping restriction where I write an algorithm to see how best I can group people in isolated groups and connections between groups are violations
# - Once these grouping have been found each interaction outside your group is a violation
# Minimize overtime shifts 
# - Regular shifts = 1 a day, each nurse gets 1 non-violated extra shift a week. every shift past that is a violation
# Minimize irregular schedules 
# Algo uses tournament selection techniques

# -  consider, partially matched crossover, rng, order crossover

# So random generation of 1,000,000 survivors gets a survivor of fitness 29
# Lets try get my algo to a level where I can produce that within 10,000 survivors