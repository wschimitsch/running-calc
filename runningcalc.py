'''
Calculator to gage aerobic fitness level and guide training efforts for endurance
sports, particularly mid-/long-distance running.
'''
# Packages
import sys
import math
import pint 

# Object for unit conversions from Pint library
ureg = pint.UnitRegistry()

options = [
    'Average pace',
    'Total activity time',
    'Splits',
    'Max Aerobic Heartrate',
    'Vo2 Max',
    # 'Equivalent Race Efforts'
]

# Modulated functions of the calculator
def get_MAF_180(age: int) -> int:
    '''
    Calculate max aerobic heartrate based on Dr. Phil Maffetone's
    "MAF 180" Formula.
    '''
    hr = 180 - age
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



def get_vo2(race_dist: pint.Quantity, race_time: pint.Quantity): # TODO update
    '''
    Calculates VO2 Max from Jack Daniels' Running Formula.
    '''   
    race_dist_m = race_dist.to('meters')
    mins = race_time.to('minutes')
    velocity = (race_dist_m / mins)
   
    vo2_max = (-4.60 + (0.182258 * velocity.magnitude) + (0.000104 * velocity.magnitude**2)) / ((0.8 + (0.1894393 * math.e**(-0.012778 * mins.magnitude)) + (0.2989558 * math.e**(-0.1932605 * mins.magnitude))))
    return vo2_max



def simulate_race(dist, time, sex):
    '''
    TODO: Estimates similar race efforts across various other distances. 
    '''
    return 0



def get_pace(dist: pint.Quantity, time: pint.Quantity , p_unit : pint.Quantity) -> str:
    '''
    Calculates the average pace (in user given units) of the given
    time and distance.
    '''
    pace = (time / dist).to(p_unit)
    return pace_to_string(pace)



def get_time(dist: pint.Quantity, pace: pint.Quantity) -> str:
    '''
    Calculates total time given a distance and pace.
    '''
    time = (dist * pace).to('seconds')
    return time_to_string(round(time.magnitude, 2))



def get_splits(total_dist: pint.Quantity, split_dist: pint.Quantity, total_time: pint.Quantity) -> str:
    '''
    Calculates the time needed for each given split distance in order to cover
    the given distance in the given time.
    '''
    # get the ratio of the split distance to the total distance and multiply by the time
    split_time = ((split_dist / total_dist) * total_time).to('seconds')
    return time_to_string(round(split_time.magnitude, 2))


def string_to_time(time_str: str) -> float:
    '''
    Converts time from a string format (HH:MM:SS.ss) to a number in seconds.
    '''
    # separate string
    time_parts = time_str.split(':')
    # put each part into variables
    hours = int(time_parts[0]) if len(time_parts) == 3 else 0
    minutes = int(time_parts[1]) if len(time_parts) == 3 else int(time_parts[0])
    seconds = float(time_parts[2]) if len(time_parts) == 3 else float(time_parts[1]) 

    return 3600*hours + 60*minutes + seconds


def time_to_string(time: float) -> str:
    '''
    Converts time from seconds to string format (HH:MM:SS.ss).
    '''
    # separate time in seconds into hours, minutes, secondso
    hours = int(time // 3600)
    minutes = int((time % 3600) // 60)
    seconds = (time % 3600) % 60
    # add the decimal
    decimal, seconds = math.modf(seconds)
    seconds = int(seconds)
    decimal = round(decimal * 100)

    return f'{hours:02}:{minutes:02}:{seconds:02}.{decimal:02}' if hours > 0 else f'{minutes:02}:{seconds:02}.{decimal:02}'


def pace_to_string(pace: pint.Quantity) -> str:
    '''
    Returns pace metrics in a nicely formatted string from a given pint Quantity. 
    '''
    # Get the time data from the pace
    time_unit = str(pace.units).split('/')[0]
    time = ureg.Quantity(str(pace.magnitude))

    # Convert to respective units
    if (time_unit.startswith('min')):
        time = time * ureg.minute
    elif (time_unit.startswith('hours')):
        time = time * ureg.hour
    
    # Then convert to seconds to call time_to_string() function
    if (time.dimensionless):
        seconds = time * ureg.second
    else:
        seconds = time.to('second')
    # Return a more formatted string denoting the pace 
    return time_to_string(seconds.magnitude) + ' ' + str(pace.units)


def parse_pace(pace_str: str) -> pint.Quantity:
    '''
    Returns a pint Quantity object from a given string.
    '''
    time, units = pace_str.split(' ', 1)
    seconds = ureg(str(string_to_time(time)) + 's')
    pace = (seconds / ureg('1 mile')).to(units)
    return pace

# def parse_distance(distance: str) -> tuple[int, str]:
#     '''
#     Parse the length and units from a string containing both (i.e. "5000m").
#     '''
#     # parse inputted distance to get the length and units separately
#     length = 0
#     units = ''
#     dec = 0.1
#     is_dec = False
#     for char in distance:
#         if char.isnumeric():
#             if not is_dec:
#                 length = length*10 + int(char)
#             else:
#                 length = length + dec*int(char)
#                 dec = dec / 10
#         elif char.isalpha():
#             units += char
#         elif char == '.':
#             is_dec = True
#     return (length, units)


# Main
print('\n--~==Welcome to Python Running Calculator==~--')
while True:
    for x, o in enumerate(options):
        print('{}. {}'.format(x+1, o))
    
    choice = input('Choose one of the above to calculate or type \'quit\' to exit: ')
    print()

    try:
        if choice.casefold() == 'quit' or choice.casefold() == 'q':
            break 
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
            print('\'{}\' is not a valid input. Pick a number between 1 and 6 or type \'quit\' to exit.\n'.format(choice))
            continue
        
        calc = int(choice)
        if calc == 1: # Average Pace
            # Get distance, time, and desired pace units as input
            dist_str = input('Distance covered: ')
            time_str = input('Total time (HH:MM:SS): ')
            p_unit = ureg(input('Desired pace units (i.e. "min/mi"): '))

            # Conver to pint Quantities
            distance = ureg(dist_str)
            time = ureg('{} seconds'.format(string_to_time(time_str)))
        
            # Calculate pace
            pace = get_pace(distance, time, p_unit)
            print('The pace is \033[1m{pace}\033[0m to cover {dist} in {time}.'.format(pace=pace, dist=dist_str, time=time_str))
        elif calc == 2: # Total Activity Time
            # Get distance and pace as input
            dist_str = input('Distance covered: ')
            pace_str = input('Average pace (i.e., 5:00 min/mi): ')

            # Convert to pint Quantities
            distance = ureg(dist_str)
            pace = parse_pace(pace_str)

            # Calculate overall time
            time = get_time(distance, pace, p_unit)
            print('It takes \033[1m{time}\033[0m to cover {dist} at a pace of {pace}.'.format(time=time, dist=dist_str, pace=pace_str))
        elif calc == 3: # Splits
            # Get distance, split distance, and time as input 
            total_dist_str = input('Distance covered: ')
            time_str = input('Total time (HH:MM:SS): ')
            split_dist_str = input('Distance for each split: ')

            # Convert to pint Quantities
            total_dist = ureg(total_dist_str)
            time = ureg('{} seconds'.format(string_to_time(time_str)))
            split_dist = ureg(split_dist_str)

            # Calculate time for each distance split
            splits = get_splits(total_dist, split_dist, time)
            print('You must split \033[1m{splits}\033[0m for every \033[1m{split_dist}\033[0m in order to cover {dist} in {time}'.format(splits=splits, split_dist=split_dist_str, dist=total_dist_str, time=time_str))
        elif calc == 4:
            # Get age as input
            age = int(input('What is your age? '))

            # Calculate MAF HR
            maf_hr = get_MAF_180(age)
            print('Your ideal maximum aerobic heart rate is \033[1m{}\033[0m , based on Phil Maffetone\'s MAF 180 formula.'.format(maf_hr))
        elif calc == 5:
            # Get race distance and time as input
            race_distance = ureg(input('Provide the length of a recent race (max effort) run : '))
            race_time = ureg('{} seconds'.format(string_to_time(input('Provide the elapsed time of the race (HH:MM:SS): '))))

            # Calculate VO2 Max
            vo2 = get_vo2(race_distance, race_time)
            print('VO2 Max: \033[1m{}\033[0m'.format(vo2))
        elif calc == 6:
            print('TODO')
        
        choice = input('\nPress [enter] to continue, or \'quit\' to exit ')
        if choice.casefold() == 'quit' or choice.casefold() == 'q':
            break 

    except Exception as e:
        print('\nAn unexpected error occurred: ', e)
        print('Please try again.\n')

print('Thank you for using Running Calculator! Goodbye.')

