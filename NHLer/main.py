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

    url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate=2022-01-01&endDate=2022-02-02"
    data = requests.get(url).json()
    days=data['dates']

    print(type(days))
    for value in days:
#       print(value['date'])
#       print(value['games'][0]['venue']['name'])
#        gamesaday=value['totalItems']
        for gamesaday in value['games']:
#            print(value['date'],gamesaday['gamePk'])
            if gamesaday['venue']['name'] == "Enterprise Center":
                print(value['date'],"||",gamesaday['gamePk'],"||",gamesaday['venue']['name'],"||",gamesaday['teams']['home']['team']['name'],"||",gamesaday['teams']['away']['team']['name'])
#print(value['games'])

#a_dict = {1: "one", 2: "two", 3: "three"}
#keys = a_dict.keys()
#keys = sorted(keys)
#for key in keys:
#    print(key)

result=get_teams()
print(result)
