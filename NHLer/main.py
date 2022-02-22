import requests
from datetime import datetime

def get_teams():

    request = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?startDate=2022-01-01&endDate=2022-02-01").json()
    days = request['dates']
    for value in days:
        for gamesaday in value['games']:
            if gamesaday['venue']['name'] == "Enterprise Center":
                print(value['date'],"||",gamesaday['gamePk'],"||",gamesaday['venue']['name'],"||",gamesaday['teams']['home']['team']['name'],"||",gamesaday['teams']['away']['team']['name'])
                game_id = str(gamesaday['gamePk'])
                home_players(game_id=game_id)
                away_players(game_id=game_id)

def home_players(game_id):
    teamdata = requests.get("https://statsapi.web.nhl.com/api/v1/game/" + game_id + "/boxscore").json()
    print ('-' *25)
    print("Хозяйва")
    print ('-' *25)
    location = "home"
    print(top_three_players(teamdata=teamdata, location=location))

def away_players(game_id):
    teamdata = requests.get("https://statsapi.web.nhl.com/api/v1/game/" + game_id + "/boxscore").json()
    print ('-' *25)
    print("Гости")
    print ('-' *25)
    location = "away"
    print(top_three_players(teamdata=teamdata, location=location))

def top_three_players(teamdata,location):
    players_list = {}
    players = teamdata['teams'][location]['players']
    for player in players:
        try:
            time_on_ice = players[player]['stats']['skaterStats']['timeOnIce']
        except:
            time_on_ice = "0:0"
        full_name = players[player]['person']['fullName']
        time = datetime.strptime(time_on_ice, '%M:%S')
        minutes = time.time()
        players_list[full_name] = minutes
    sorted_list = (sorted(players_list.items(), key=lambda x: x[1], reverse=True)[:3])
    return(sorted_list)




result=get_teams()

