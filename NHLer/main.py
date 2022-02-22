import requests
from flask import Flask
from requests import request

def get_teams():
    url = "https://statsapi.web.nhl.com/api/v1/venues/5076"
    data = requests.get(url).json()
    print(data['venues'][0]['id'])
#    for key, value in data.items():
#        print(key, "222", value)
#        subvalue=value.json()
#        print(subvalue["id"])

    data = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?startDate=2022-01-01&endDate=2022-03-01").json()
    days=data['dates']

    print(type(days))
    for value in days:
        for gamesaday in value['games']:
            if gamesaday['venue']['name'] == "Enterprise Center":
                print(value['date'],"||",gamesaday['gamePk'],"||",gamesaday['venue']['name'],"||",gamesaday['teams']['home']['team']['name'],"||",gamesaday['teams']['away']['team']['name'])

# Список игроков
    teamdata = requests.get("https://statsapi.web.nhl.com/api/v1/game/2021020566/boxscore").json()

# Гости
    print ('-' *25)
    print("Гости")
    print ('-' *25)
    away_players = teamdata['teams']['away']['players']
    for away_player in away_players:
        try:
            timeOnIce = away_players[away_player]['stats']['skaterStats']['timeOnIce']
        except:
            timeOnIce = 0
        fullName = away_players[away_player]['person']['fullName']
        print(fullName, timeOnIce)

# Хозяйва
    print ('-' *25)
    print("Хозяйва")
    print ('-' *25)
    home_players = teamdata['teams']['home']['players']
    for home_player in home_players:
        try:
            timeOnIce = home_players[home_player]['stats']['skaterStats']['timeOnIce']
        except:
            timeOnIce = 0
        fullName = home_players[home_player]['person']['fullName']
        print(fullName, timeOnIce)

#    fullName = teamdata['teams']['away']['players']['ID8477949']['person']['fullName']
#    timeOnIce = teamdata['teams']['away']['players']['ID8477949']['stats']['skaterStats']['timeOnIce']
#    print(fullName,"||", timeOnIce)


#https://statsapi.web.nhl.com/api/v1/game/2021020613/boxscore/teams/away(#home)/players(#list)/ID8481580 "stats": {"skate#rStats": { "timeOnIce": "15:59"
#print(value['games'])

#a_dict = {1: "one", 2: "two", 3: "three"}
#keys = a_dict.keys()
#keys = sorted(keys)
#for key in keys:
#    print(key)

result=get_teams()
print(result)
