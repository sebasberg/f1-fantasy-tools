import itertools

BUDGET = 102.5
CURRENT_TEAM = "current team features to be implemented so that one can calculate number of "

with open("drivers.txt") as drivers_file, open("constructors.txt") as constructors_file:
    drivers_dict = {}
    for line in drivers_file.readlines():
        drivers_dict[line.split()[0]] = float(line.split()[1])

    constructors_dict = {}
    for line in constructors_file.readlines():
        constructors_dict[line.split()[0]] = float(line.split()[1])

def calculate_price(drivers, constructor):
    """
    Calculates and returns the total price of the drivers and the constructor
    """
    price = 0
    price += constructors_dict[constructor]
    for driver in drivers:
        price += drivers_dict[driver]
    return round(price, 1)

def find_available_teams(*drivers, constructor=None):
    """
    Returns a list of all combinations of drivers and constructor that is within the budget
    and contains the given drivers and constructor as parameters. 
    """
    # Currently not implemented calculation of all constructors, need to choose constructor manually at this point
    if constructor == None:
        print("No constructor given, exiting...")
        return
    # List to store all combinations of available teams with current budget
    available_teams = []
    # Finds all possible driver combinations
    all_driver_combinations = list(itertools.combinations(drivers_dict.keys(), 5))

    for combination in all_driver_combinations:
        # If all given drivers is contained in the combination of drivers and the price is within the budget, append to available list
        if set(drivers).issubset(combination) and calculate_price(combination, constructor) <= BUDGET:
            # Add constructor and price to the combination tuple before adding available team to the returned list
            available_teams.append(combination + (constructor, calculate_price(combination, constructor)))

    return available_teams

def print_teams(teams):
    for team in teams:
        print(f"{team[0]}-{team[1]}-{team[2]}-{team[3]}-{team[4]}-{team[5]}    ${team[6]}M")


print_teams(find_available_teams("PER", "ALB", "VER", constructor="RB"))