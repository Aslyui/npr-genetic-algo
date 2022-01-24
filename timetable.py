import random
import numpy as np
     
class timetable:
    def __init__(self, nurses: int, days: int, shifts: int, minimum_nurses: int, maximum_nurses: int, required_nurses: list[list[int]] = None, nurse_preferences: list[list[int]] = None, max_shifts: int = 2, max_consecutive_shifts: int = 2, min_shifts: int = 0, breaks_per_week: int = 1) -> None:
        self.nurses = nurses
        self.days = days
        self.shifts = shifts
        self.minimum_nurses = minimum_nurses
        self.maximum_nurses = maximum_nurses
        self.max_shifts = max_shifts
        self.min_shifts = min_shifts
        self.max_consecutive_shifts = max_consecutive_shifts 
        self.breaks_per_week = breaks_per_week
        self.required_nurses = required_nurses if required_nurses is not None else self.generate_required_nurses()
        self.nurse_preferences = nurse_preferences if nurse_preferences is not None else self.generate_nurse_preferences()
        # print(self.nurse_preferences)
        # print("\n\n\n\n")
        # print(self.required_nurses)
            
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
{preferences}
"""
                
    def generate_required_nurses(self) -> list:
        counter = 0
        while True:
            if counter > 100000:
                raise "Too many iterations"
            
            required_nurses = np.random.randint(self.minimum_nurses, self.maximum_nurses + 1, size=(self.days, self.shifts))
            if not all([sum(daily_nurse_requirement) <= self.nurses * self.max_shifts * 2 / 3 for daily_nurse_requirement in required_nurses]) and not all([sum(daily_nurse_requirement) >= self.nurses * self.min_shifts for daily_nurse_requirement in required_nurses]):
                continue
            # Condition to ensure that no night + morning shift is held
            if not all([required_nurses[i][self.shifts - 1] + required_nurses[i + 1][0] < self.nurses for i in range(0, self.days - 1)]):
                continue
            
            counter += 1
            return required_nurses

    def generate_nurse_preferences(self) -> list:
        nurse_preferences = [[[0] * 3 for _ in range(self.days)] for _ in range(self.nurses)]
        current_nurse = 0
        while current_nurse != self.nurses:
            shift_preference = np.random.randint(0, self.shifts)
            prefers_similar_shifts = np.random.randint(70, 100)
            for day in range(0, self.days):
                if np.random.randint(0, 100) < prefers_similar_shifts:                   
                    nurse_preferences[current_nurse][day][shift_preference] = 1
                else:
                    nurse_preferences[current_nurse][day][np.random.randint(0, self.shifts)] = 1
        
            current_nurse += 1
        return nurse_preferences

