# Tanner Tamondong
# March 31, 2023
# Baseball Roster Program
# This program imports a baseball team lineup and provides an interface to view the lineup and make changes to stats and lineup positions.

import FileIO
from datetime import date,datetime,timedelta

POSITIONS_TUPLE = ("C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P")

def display_lineup(roster):
    # This function calculates batting average and prints out the team roster with stats
    print('\nCURRENT ROSTER')
    print(f"{'#':<3}{'Player':<31} {'POS':<6} {'AB':<6} {'H':<6} {'AVG':<8}")
    print('----------------------------------------------------------------')
    num = 1
 
    for player in roster:
        if player['AB'] == '0':
            average = 0
        else:
            average = int(player['hits'])/int(player['AB'])   
        print(f"{str(num):<3} {player['name']:<31} {player['position']:<6} {player['AB']:<6} {player['hits']:<6} {average:.3f}")
        num += 1

      
def add_player(roster):
    # This function gets input from the user for the new player's name, position, at bats, and hits.
    print('Enter new player information: ')
    name = input('Name: ')
    position = input('Position: ')
    while position not in POSITIONS_TUPLE:   
        print('Invalid position.')
        display_positions()
        position = input('Position: ') 
    at_bats = input('At Bats: ')
    while True:
        try: 
            if int(at_bats) >= 0:
                pass
            else:
                raise ValueError     
        except ValueError:
            print('Invalid number of at bats. Value must be integer greater than or equal to 0')
            at_bats = input('At Bats: ')    
        else:
            break
       
    hits = input('Hits: ')  
    while True:
        try:
            if int(hits) <= int(at_bats) and int(hits) >= 0:
                pass
            else:
                raise ValueError
        except ValueError: 
            print('Invalid number of hits. Value must be less than or equal to # of AB')
            hits = input('Hits: ')  
        else:
            break
    new_player = {'name':name,'position':position,'AB':at_bats,'hits':hits}

    roster.append(new_player)
    print(f'\n{new_player["name"]} was added to the roster.' )
    FileIO.save_team_data(roster)
    return roster

def remove_player(roster):
    # This function removes a player from the lineup based on the user's input of lineup number
    remove_input = input('Enter a lineup number to remove: ')
    while True:
        try: 
            remove_index = int(remove_input) - 1
        except ValueError:
            print('Expected an integer for player number')
            remove_input = input('Enter a lineup number to remove: ')
        else:
            print(f'\n{roster[remove_index]["name"]} was removed from the roster. ')
            del roster[remove_index]
            FileIO.save_team_data(roster)
            return roster

def move_player(roster):
    # This function takes user input for a player to move in the lineup. It then swaps lineup spots with the player in the new spot
    old_lineup = input('Enter a current lineup number to move: ')
    
    while True:
        try: 
            if int(old_lineup) not in range(len(roster)+1):
                raise ValueError
        except ValueError:
            print('Invalid lineup number')
            old_lineup = input('Enter a current lineup number to move: ')
        else:
            old_index = int(old_lineup)-1
            player = roster[old_index]
            print(f'{player["name"]} was selected')
            break
    
    new_lineup = input('Enter new lineup number: ')

    while True:
        try: 
            if int(new_lineup) not in range(len(roster)+1):
                raise ValueError
        except ValueError:
            print('Invalid lineup number')
            new_lineup = input('Enter new lineup number: ')
        else:
            new_index = int(new_lineup)-1
            temp_player = roster[new_index]
            roster[new_index] = player
            roster[old_index] = temp_player
            print(f'\n{player["name"]} was moved to {new_lineup}')
            print(f'{temp_player["name"]} was moved to {old_lineup}')
            break
    
    FileIO.save_team_data(roster)
    return roster
    
def edit_position(roster):
    # This function edits the position of a player based on lineup number input
    change_position = input('Enter a current lineup number to move: ')
    
    while True:
        try: 
            if int(change_position) not in range(len(roster)+1):
                raise ValueError
        except ValueError:
            print('Invalid lineup number')
            change_position = input('Enter a current lineup number to move: ')
        else:
            lineup_index = int(change_position)-1
            player = roster[int(lineup_index)]
            print(f'You selected {player["name"]} who is currently at {player["position"]}')
            break

    new_position = input('Enter a new position: ')

    while True:
        try: 
            if new_position not in POSITIONS_TUPLE:
                    raise ValueError
        except ValueError:
            print('Invalid position.')
            display_positions()
            new_position = input('Enter a new position: ')
        else:
            roster[int(lineup_index)]['position'] = new_position
            print(roster[lineup_index]["name"] + "'s position was updated was updated to " + new_position)
            break
    FileIO.save_team_data(roster)
    return roster

def edit_stats(roster):
    # This function edits the AB and Hits statistics for a player based on lineup number input
    edit_input = input('Enter lineup number to edit their stats: ')
    while True:
        try:
            if int(edit_input) not in range(len(roster)+1):
                raise ValueError
        except ValueError:
            print('Invalid lineup number')
            edit_input = input('Enter lineup number to edit their stats: ')
        else:
            edit_index = int(edit_input) - 1
            print(f'\n{roster[edit_index]["name"]} was selected. \nCurrent stats:\n---------------\nAt Bats: {roster[edit_index]["AB"]}\nHits: {roster[edit_index]["hits"]}')
            print('\nEnter updated stats')
            break

    while True:
        try:
            new_ABs = input('Number of at bats: ')
            new_hits = input('Number of hits: ')
            if int(new_ABs) < int(new_hits):
                raise ValueError
            if int(new_ABs) < 0 or int(new_hits) < 0:
                raise ValueError
        except ValueError:
            print('Invalid input. Must be atleast 0 and cannot have more hits than at bats')
        else:
            roster[edit_index]["AB"] = new_ABs
            roster[edit_index]["hits"] = new_hits
            print(f"{roster[edit_index]['name']}'s stats have been updated.")
            break
    FileIO.save_team_data(roster)
    
def display_title():
    # Display the program title
    print('\n\n==+==+===+==+==+==+===+==+==+==+===+==+==+==+===+==+==+==+==')
    print('             Baseball Team Management Program               ')
    date_calculation()

def date_calculation():
    # Display current data, prompt for next game day, and calculate days until then
    today = datetime.now().date()
    print(f'\nCURRENT DATE:  {today}')
    game_date = input('GAME DATE: ')
    if game_date:
        game_day = datetime.strptime(game_date,"%Y-%m-%d")
        days_until_game = game_day - datetime.now()
        if days_until_game.days > 0:
            print(f'DAYS UNTIL GAME: {days_until_game.days}')
        else:
            pass

def display_menu():
    # Display the menu with command options
    print('\nMENU OPTIONS')
    print('1 - Display lineup')
    print('2 - Add player')
    print('3 - Remove player')
    print('4 - Move player')
    print('5 - Edit player position')
    print('6 - Edit player stats')
    print('7 - Exit program')

    
def display_positions():
    # Display the tuple of valid positions
    print('\nPOSITIONS')
    print(POSITIONS_TUPLE)
    print('==+==+===+==+==+==+===+==+==+==+===+==+==+==+===+==+==+==+==\n')

    
def main():
    # Main function that initializes the menu, calls all other functions based on inputs, and kills the program when the exit command is entered
    display_title()
    display_menu()
    display_positions()
    roster = FileIO.read_team_data()
    
    command = input("Menu option: ")
    while command != '7':
        if command == '1':
            display_lineup(roster)
        elif command == '2':
            add_player(roster)
        elif command == '3':
            remove_player(roster)
        elif command == '4':
            move_player(roster)
        elif command == '5':
            edit_position(roster)
        elif command == '6':
            edit_stats(roster)
        else: 
            print('\nNot a valid option. Please choose an option from the menu\n')
            display_menu()
        command = input("\nMenu option: ")

    print('\nBye!')   

if __name__ == "__main__":
    main()