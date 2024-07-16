'''
Calculator to gage aerobic fitness level and guide training
efforts for endurance sports, particularly mid-/long-distance
running.
'''
# Packages
import math
from pint import UnitRegistry

# Functions
'''
Calculate max aerobic heartrate based on Dr. Phil Maffetone's
"MAF 180" Formula.
'''
def get_MAF_180(age):
    hr = 180 - age
    print("Please answer the following questions with yes (y) or no (n):\n")

    ans = input("Recovering from any major illness or overtraining OR on any regular medication? (y/n) ")
    if ans.casefold() == "yes" or ans.casefold() == "y":
        hr = hr - 10

    print("Injured, regressed, not improving or inconsistent in training OR are overfat, get more")
    ans = input("than two colds, flu or other infections per year, have seasonal allergies or asthma? (y/n) ")
    if ans.casefold() == "yes" or ans.casefold() == "y":
        hr = hr - 5

    ans = input ("Training consistently for MORE THAN 2 years WITH progress and WITHOUT any problems? (y/n) ")
    if ans.casefold() == "yes" or ans.casefold() == "y":
        hr = hr + 5

    return hr

'''
Calculates VO2 Max
'''
def get_vo2(resting_hr):
    return 0

'''
Estimates similar race efforts across various other distances. 
'''
def simulate_race(dist, time, sex):
    return 0

'''
Calculates the average pace (in user given units) of the given time and distance.
'''
def get_pace(dist, d_unit, time, p_unit):
    converted_dist = convert_units(dist, d_unit, p_unit)
    seconds = string_to_time(time)
    return time_to_string(seconds / converted_dist)

'''
Calculates total time given a distance and pace.
'''
def get_time(dist, d_unit, pace, p_unit):
    # convert the pace units to be the same as the distance units, then multiply by the distance
    return time_to_string(string_to_time(pace)/convert_units(1.0, p_unit, d_unit)*dist)

'''
Calculates the time needed for each given split distance to run the given time
across the total distance. Can use feet, meters, yards, miles, or kilometers.
'''
def get_splits(total_dist, d_unit, time, split_dist, s_unit):
    # convert total distance to the split distance units and get the ratio
    converted_dist = convert_units(total_dist, d_unit, s_unit)
    ratio = split_dist / converted_dist
    # multiply the time in seconds by the ratio and return a rounded, formatted time
    return time_to_string(round(string_to_time(time) * ratio, 2))

'''
Converts time from a string format (HH:MM:SS.ss) to a number in seconds.
'''
def string_to_time(time_str):
    # separate string
    time_parts = time_str.split(':')
    # put each part into variables
    hours = int(time_parts[0]) if len(time_parts) == 3 else 0
    minutes = int(time_parts[1]) if len(time_parts) == 3 else int(time_parts[0])
    seconds = float(time_parts[2]) if len(time_parts) == 3 else float(time_parts[1]) 

    return 3600*hours + 60*minutes + seconds

'''
Converts time from seconds to string format (HH:MM:SS.ss).
'''
def time_to_string(time):
    # separate time in seconds into hours, minutes, seconds
    hours = int(time // 3600)
    minutes = int((time % 3600) // 60)
    seconds = (time % 3600) % 60
    # add the decimal
    decimal, seconds = math.modf(seconds)
    seconds = int(seconds)
    decimal = round(decimal * 100)

    return f"{hours:02}:{minutes:02}:{seconds:02}.{decimal:02}" if hours > 0 else f"{minutes:02}:{seconds:02}.{decimal:02}"

'''
Converts values from a given unit to the desired unit. 
'''
def convert_units(metric, from_unit, to_unit):
    # from Pint library
    ureg = UnitRegistry()
    # convert the value to the desired units
    original = metric * ureg(from_unit)
    converted = original.to(to_unit)
    return converted.magnitude

# Main
# TODO let user choose which function to use

print(get_pace(42195, "meters", "2:19:59", "miles"))
print(get_time(42195, "meters", "5:20.34", "miles"))