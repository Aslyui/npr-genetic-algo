from typing_extensions import Required
from timetable import timetable
import itertools
import types

def no_consecutive_shifts(timetable: timetable, nurse_schedule: list[int]) -> bool:
    counter = 0
    for i in range(0, timetable.days):
        for j in range(0, timetable.shifts):
            counter = counter + 1 if nurse_schedule[i][j] else 0
            if counter > timetable.max_consecutive_shifts:
                # print('fails consecutive')
                return False
        
    return True

def max_shifts_a_day(timetable: timetable, nurse_schedule: list[int]) -> bool:
    if any in [sum(day) > timetable.max_shifts for day in nurse_schedule]:
        # print('fails max shifts') 
        return False
   
    return True

def minimum_shifts_a_day(timetable: timetable, nurse_schedule: list[int]) -> bool:
    if any in [sum(day) < timetable.min_shifts for day in nurse_schedule]:
        # rint('fails min shifts')
        return False
    
    return True

def no_end_to_beginning_shift(timetable: timetable, nurse_schedule: list[int]) -> bool:
    for i in range(0, timetable.days - 2):
        if nurse_schedule[i][timetable.shifts - 1] and nurse_schedule[i + 1][0]:
            # print('fails no end to beginning')
            return False
        
    return True

def meets_shift_requirements(timetable: timetable, nurse_schedules: list[list[int]]) -> bool:
    nurse_schedules = [list(itertools.chain.from_iterable(nurse_schedule)) for nurse_schedule in nurse_schedules]
    required_nurses = list(itertools.chain.from_iterable(timetable.required_nurses))
    for i in range(0, timetable.days * timetable.shifts):    
        number_of_nurses = sum([nurse_schedule[i] for nurse_schedule in nurse_schedules])
        if number_of_nurses < required_nurses[i]:
            # print('fails meets shift requirements')
            return False

    return True

def not_too_many_nurses(timetable: timetable, nurse_schedules: list[list[int]]) -> bool:
    nurse_schedules = [list(itertools.chain.from_iterable(nurse_schedule)) for nurse_schedule in nurse_schedules]
    for i in range(0, timetable.days * timetable.shifts):
        number_of_nurses = sum([nurse_schedule[i] for nurse_schedule in nurse_schedules])
        if number_of_nurses > timetable.maximum_nurses:
            # print("\n".join(["Nurse {}: {}".format(i, nurse_schedules[i]) for i in range(0, timetable.nurses)]), [nurse_schedule[i] for nurse_schedule in nurse_schedules])
            # print(f'{number_of_nurses} > {timetable.maximum_nurses} fails too many nurses at {i} ')
            if number_of_nurses > 10:
                return
            return False

    return True

hard_constraints_per_nurse = [no_consecutive_shifts, max_shifts_a_day]

hard_constraints_per_schedule = [meets_shift_requirements, not_too_many_nurses]
