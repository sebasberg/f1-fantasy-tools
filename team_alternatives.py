import itertools
from constants import CURRENT_BUDGET, CURRENT_TEAM
from database_helper import DatabaseHelper

with DatabaseHelper() as db:
    drivers_dict = db.get_drivers()
    constructors_dict = db.get_constructors()

def calculate_price(team):
    """
    Calculates and returns the total price of the drivers and the constructor on a team.
    """
    price = 0
    for member in team:
        try:
            price += drivers_dict[member][0]
        except:
            price += constructors_dict[member][0]
    return round(price, 1)

def calculate_points(team):
    """
    Calculates and returns the total points of the drivers and the constructor on a team.
    """
    points = 0
    for member in team:
        try:
            points += drivers_dict[member][1]
        except:
            points += constructors_dict[member][1]
    return points

def calculate_subs(team):
    """
    Calculates and returns the total number of subs from current team to achieve the given team.
    """
    subs = 0
    for member in team:
        if member not in CURRENT_TEAM:
            subs += 1
    return subs

def find_available_teams(drivers, constructors):
    """
    Returns a list of all combinations of drivers and constructor that is within the budget
    and contains the given drivers and constructor as parameters.
    Parameters:
        drivers:        All drivers given in this list or tuple must be included on the teams in the list of available teams,
                        if none is given then all drivers are considered eligible.
        constructors:   If the list or tuple of constructors is empty, then all constructors are considered. If non empty,
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
            if set(subset).issubset(team_combination) and calculate_price(team_combination) <= CURRENT_BUDGET:
                available_teams.append(team_combination + (calculate_price(team_combination), calculate_points(team_combination), calculate_subs(team_combination)))

    return available_teams

def sort_by_points(teams, reverse=True):
    """
    Sort a list of teams in descending order by total points.
    Parameters:
        teams: A list of tuples, where each tuple is a team.
        reverse: Set this to false to sort in ascending order.
    Returns:
        The sorted list of teams.
    """
    # Sort by the 7th item in team tuple
    return sorted(teams, key=lambda x: x[7], reverse=reverse)

def print_teams(teams):
    """
    Printing teams to the terminal with the current price.
    Parameters:
        teams:  A list of tuples, where each tuple is a team with drivers, constructor, total price, and total points.
    """
    for team in teams:
        print(f"{team[0]}-{team[1]}-{team[2]}-{team[3]}-{team[4]}-{team[5]}    ${team[6]}M    {team[7]} points    {team[8]} subs")

def print_top_driver_value(reverse=True):
    """
    Printing drivers sorted by points/price.
    Parameters:
        reverse: If reverse is set to False, the drivers are sorted in ascending order
    """
    with DatabaseHelper() as db:
        drivers_sorted = db.drivers_sorted_points_price(reverse=reverse)
    for position, driver in enumerate(drivers_sorted):
        print(f"{position+1}. | {driver[0]} | ${driver[1]}M | {driver[2]} points | {driver[3]} points per $M")

def print_top_constructor_value(reverse=True):
    """
    Printing constructors sorted by points/price.
    Parameters:
        reverse: If reverse is set to False, the constructors are sorted in ascending order.
    """
    with DatabaseHelper() as db:
        construcors_sorted = db.constructors_sorted_points_price(reverse)
    for position, constructor in enumerate(construcors_sorted):
        print(f"{position+1}. | {constructor[0]} | ${constructor[1]}M | {constructor[2]} points | {constructor[3]} points per $M")


print_teams(sort_by_points(find_available_teams(("PER", "SAI", "BOT",), ("RB",))))
