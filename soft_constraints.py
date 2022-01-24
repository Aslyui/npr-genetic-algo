from timetable import timetable
import functools
import itertools

def matching_preferences(timetable: timetable, nurse_schedules: list[list[int]]) -> float:
    violations = 0
    for nurse in range(0, timetable.nurses):
        for day in range(0, timetable.days):
            for shift in range(0, timetable.shifts):
                if timetable.nurse_preferences[nurse][day][shift] and not nurse_schedules[nurse][day][shift]:
                    violations += 1
    
    return violations
    
def minimize_inconsistent_shifts(timetable: timetable, nurse_schedules: list[list[int]]) -> float:
    violations = 0
    for nurse in range(1, timetable.nurses):
        consistent_schedule = -1
        for day in range(1, timetable.days):
            previous_shift = []
            for shift in range(0, timetable.shifts):
                if nurse_schedules[nurse - 1][day - 1][shift] == 1:
                    previous_shift.append(shift)
                if nurse_schedules[nurse][day][shift] == 1 and (shift not in previous_shift and timetable.nurse_preferences[nurse][day][shift] and shift != consistent_schedule):        
                    violations += 1
            
    return violations
    
def weekly_breaks(timetable: timetable, nurse_schedules: list[list[int]]) -> float:
    violations = 0
    for nurse in nurse_schedules:
        days_worked_per_week = [sum(list(itertools.chain.from_iterable(week))) for week in [nurse[x:x + 7] for x in range(0, len(nurse), 7)]]
        for week in days_worked_per_week:
            if week > 7 - timetable.breaks_per_week:
                violations += 1

    return violations

def equal_shifts(timetable: timetable, nurse_schedules: list[list[int]]) -> float:
    violations = 0
    number_of_shifts_per_nurse = [sum(list(itertools.chain.from_iterable(nurse))) for nurse in nurse_schedules]
    average = sum(number_of_shifts_per_nurse) / len(number_of_shifts_per_nurse)
    for nurse in number_of_shifts_per_nurse:
        if abs(nurse - average) / average > 0.15:
            violations += 1
            
    return violations


soft_constraints = [matching_preferences, minimize_inconsistent_shifts, weekly_breaks, equal_shifts]