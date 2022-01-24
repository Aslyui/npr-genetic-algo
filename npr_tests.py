# ok i know i should be writing tests... but this is a FOR FUN project and I'll suffer the consequences of my own actions eventually
import pytest

from timetable import timetable

def test_timetable():
    t = timetable(nurses=10, days=5, shifts=3, minimum_nurses=1, maximum_nurses=3)
    print(t)