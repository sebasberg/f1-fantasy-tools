import itertools

BUDGET = 102.5
CURRENT_TEAM = "current team features to be implemented so that one can calculate number of "

# Get data from files
with open("drivers.txt") as drivers_file, open("constructors.txt") as constructors_file:
    drivers_dict = {}
    for line in drivers_file.readlines():
        drivers_dict[line.split()[0]] = float(line.split()[1])

    constructors_dict = {}
    for line in constructors_file.readlines():
        constructors_dict[line.split()[0]] = float(line.split()[1])

def calculate_price(team):
    """
    Calculates and returns the total price of the drivers and the constructor on a team.
    """
    price = 0
    for member in team:
        try:
            price += drivers_dict[member]
        except:
            price += constructors_dict[member]
    return round(price, 1)

def find_available_teams(drivers, constructors):
    """
    Returns a list of all combinations of drivers and constructor that is within the budget
    and contains the given drivers and constructor as parameters.
    Parameters:
        drivers:        All drivers given in this list or tuple must be included on the teams in the list of available teams,
                        if none is given then all drivers are considered eligible.
        constructors:    If the list or tuple of constructors is empty, then all constructors are considered. If non empty,
                        all teams are combined with all the constructors given in this list.
    Returns:
        A list of all available teams given the information from arguments.
    """

    # List to store all combinations of available teams with current budget
    available_teams = []
    # Finds all possible driver combinations
    all_driver_combinations = list(itertools.combinations(drivers_dict.keys(), 5))
    # Finds all possible team combinations
    all_team_combinations = list(itertools.product(all_driver_combinations, constructors_dict.keys()))
    # Flattens driver tuple to be one tuple with constructor included in the tuple
    all_team_combinations = [team[0] + (team[1],) for team in all_team_combinations]
    
    # Find all teams that is subsets of the available teams
    all_subsets = []
    if constructors:
        for constructor in constructors:
            all_subsets.append(drivers + (constructor,))
    else:
        for constructor in constructors_dict.keys():
            all_subsets.append(drivers + (constructor,))

    for team_combination in all_team_combinations:
        # If a possible subset is a subset of a team combination, and the team combination is within the budget, append to available teams
        for subset in all_subsets:
            if set(subset).issubset(team_combination) and calculate_price(team_combination) <= BUDGET:
                available_teams.append(team_combination + (calculate_price(team_combination),))



        #if set(drivers).issubset(combination) and calculate_price(combination, constructor) <= BUDGET:
            # Add constructor and price to the combination tuple before adding available team to the returned list
        #    available_teams.append(combination + (constructor, calculate_price(combination, constructor)))

    return available_teams

def print_teams(teams):
    """
    Printing teams to the terminal with the current price.
    Parameters:
        teams:  A list of tuples, where each tuple is a team with drivers, constructor, and total price.
    """
    for team in teams:
        print(f"{team[0]}-{team[1]}-{team[2]}-{team[3]}-{team[4]}-{team[5]}    ${team[6]}M")


print_teams(find_available_teams(("PER", "SAI", "BOT",), ("RB",)))