# Tanner Tamondong
# March 31, 2023
# Baseball Roster Program
# This program imports a baseball team lineup and creates a list of dictionaries to be manipulated by the main program, then exports any changes. 

import csv

FILE_NAME = '/Users/tannertamondong/python_files/project2/BaseballPlayers.csv'
#FILE_NAME = 'BaseballPlayers.csv'

def read_team_data():
    # This function searches for the team data .csv file from FILE_NAME constant and returns a list of each player and their attributes. 
    # An empty list is returned if no file is found
    
    roster_list = []
    try:
        with open (FILE_NAME) as data:
            reader = csv.reader(data)   
            player_list = list(reader)     
            
            for player in player_list:
                player_dict = {'name':player[0],'position':player[1],'AB':player[2],'hits':player[3]}
                roster_list.append(player_dict)
 
        return roster_list
    
    except FileNotFoundError:
        print("Player database was not found. Returning empty list")
        return roster_list
            

# FIX THE SAVE FUNCTION
def save_team_data(roster):
    # Function to save the updated team roster to the original file 
    with open (FILE_NAME,'w') as data:
        for player in roster:
            data.write(f'{player["name"]},{player["position"]},{player["AB"]},{player["hits"]}\n')             
   

