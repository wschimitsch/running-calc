'''
Calculator to gage aerobic fitness level and guide training efforts for endurance
sports, particularly mid-/long-distance running.
'''
# Packages
import sys
import math
from pint import UnitRegistry

# Object for unit conversions from Pint library
ureg = UnitRegistry()

# Functions
'''
Calculate max aerobic heartrate based on Dr. Phil Maffetone's
"MAF 180" Formula.
'''
def get_MAF_180(age):
    hr = 180 - int(age)
    print('Please answer the following questions with yes (y) or no (n):')
    ans1, ans2 = False, False
    ans = input('Recovering from any major illness or overtraining OR on any regular medication? (y/n) ')
    if ans.casefold() == 'yes' or ans.casefold() == 'y':
        ans1 = True
        hr = hr - 10

    print('Injured, regressed, not improving or inconsistent in training OR are overfat, get more')
    ans = input('than two colds, flu or other infections per year, have seasonal allergies or asthma? (y/n) ')
    if ans.casefold() == 'yes' or ans.casefold() == 'y':
        ans2 = True
        hr = hr - 5
    
    if not ans1 and not ans2:
        ans = input ('Training consistently for MORE THAN 2 years WITH progress and WITHOUT any problems? (y/n) ')
        if ans.casefold() == 'yes' or ans.casefold() == 'y':
            hr = hr + 5
    print()
    return hr

'''
Calculates VO2 Max from 
'''
def get_vo2(race_dist, race_unit, race_time):
    velocity = 0 # calculate velo

    vo2_max = (-4.60 + 0.182258 * velocity + 0.000104 * velocity**2) / (0.8 + 0.1894393 * math.e**(-0.012778 * race_time) + 0.2989558 * math.e^(-0.1932605 * race_time))
    return vo2_max

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
    p_sec = string_to_time(pace) / convert_units(1.0, p_unit, d_unit)
    total_time = p_sec * dist
    return time_to_string(total_time)

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

    return f'{hours:02}:{minutes:02}:{seconds:02}.{decimal:02}' if hours > 0 else f'{minutes:02}:{seconds:02}.{decimal:02}'

'''
Converts values from a given unit to the desired unit. 
'''
def convert_units(metric, from_unit, to_unit):
    # convert the value to the desired units
    original = metric * ureg(from_unit)
    converted = original.to(to_unit)
    return converted.magnitude

'''
Parse the length and units from a string containing both (i.e. "5000m").
'''
def parse_distance(distance):
    # parse inputted distance to get the length and units separately
    return

# Main
# TODO let user choose which function to use

print('\n--~==Welcome to Python Running Calculator==~--\n')
print ('\033[1m' + 'Hello')
while True:
    print('1. Average pace \n2. Total activity time \n3. Time splits \n4. Max Aerobic Heartrate \n5. Vo2 Max \n6. Equivalent Race Efforts')
    choice = input("Choose one of the above to calculate or type 'quit' to exit: ")
    print()

    if choice.casefold() == 'quit' or choice.casefold() == 'q':
        sys.exit(0)    
    if not choice.isdigit() or (int(choice) >= 1 and int(choice) >= 6):
        print("'" + choice + "' is not a valid input. Pick a number between 1 and 6 or type 'quit' to exit.\n")
        continue
    
    calc = int(choice)
    if calc == 1:
        distance = float(input('Distance covered: '))
        d_unit = input('Distance units: ')
        time = input('Time elapsed (HH:MM:SS): ')
        p_unit = input("Desired pace units (i.e. 'miles' for mi/min)")
        pace = get_pace(distance, d_unit, time, p_unit)
        print(pace)
    if calc == 2:
        distance = float(input('Distance covered: '))
        d_unit = input('Distance units: ')
        pace = input('Average pace (HH:MM:SS): ')
        p_unit = input("Pace units (i.e. 'miles' for mi/min): ")
        time = get_time(distance, d_unit, pace, p_unit)
        print(time)
    if calc == 3:
        distance = float(input('Distance covered: '))
        d_unit = input('Distance units: ')
        time = input('Time elapsed (HH:MM:SS): ')
        split_dist = input('Split distance: ')
        split_unit = input('Split units: ')
        splits = get_splits(distance, d_unit, time, split_dist, split_unit)
    if calc == 4:
        age = input('What is your age? ')
        maf_hr = get_MAF_180(age)
        print('Your ideal maximum aerobic heart rate is ' + '\033[1m' + str(maf_hr) + '\033[0m' + ", based on Phil Maffetone's MAF 180 formula.\n")
    if calc == 5:
        race_distance = float(input('Provide the length of a recent race (max effort) run : '))
        race_unit = input('Units for the race length: ')
        race_time = input('Provide the elapsed time of the race (HH:MM:SS): ')
        vo2 = get_vo2(race_distance, race_unit, race_time)
    if calc == 6:
        print('TODO\n')
       
