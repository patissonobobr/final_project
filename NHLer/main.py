import requests
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

main = Flask(__name__)
main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NHLer.db'
db = SQLAlchemy(main)

class gamesdb(db.Model):
    date = db.Column(db.String(10), primary_key = True)
    hometeam = db.Column(db.String(30))
    awayteam = db.Column(db.String(30))
    homescore  = db.Column(db.Integer)
    awayscore = db.Column(db.Integer)
    homeplayer1 = db.Column(db.String(30))
    homeplayer1_time = db.Column(db.String(5))
    homeplayer2 = db.Column(db.String(30))
    homeplayer2_time = db.Column(db.String(5))
    homeplayer3 = db.Column(db.String(30))
    homeplayer3_time = db.Column(db.String(5))
    awayplayer1 = db.Column(db.String(30))
    awayplayer1_time = db.Column(db.String(5))
    awayplayer2 = db.Column(db.String(30))
    awayplayer2_time = db.Column(db.String(5))
    awayplayer3 = db.Column(db.String(30))
    awayplayer3_time = db.Column(db.String(5))

def get_teams():

    request = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?startDate=2022-01-01&endDate=2022-02-01").json()
    days = request['dates']
    for value in days:
        for gamesaday in value['games']:
            if gamesaday['venue']['name'] == "Enterprise Center":
                date = value['date']
                game_id = str(gamesaday['gamePk'])
                venue = gamesaday['venue']['name']
                hometeam = gamesaday['teams']['home']['team']['name']
                awayteam = gamesaday['teams']['away']['team']['name']
                homescore = gamesaday['teams']['home']['score']
                awayscore = gamesaday['teams']['away']['score']
#                print(date, "||", game_id, "||", venue, "||", hometeam, "||", homescore, "||", awayscore, "||", awayteam)
                homeplayerslist = home_players(game_id=game_id)
                awayplayerslist = away_players(game_id=game_id)
                try:
                    game = gamesdb(
                        ### game data
                        date=date, hometeam=hometeam, homescore=homescore, awayteam=awayteam, awayscore=awayscore,
                        ### Top3 home players
                        homeplayer1=homeplayerslist[0][0],
                        homeplayer1_time=homeplayerslist[0][1].strftime('%M:%S'),
                        homeplayer2=homeplayerslist[1][0],
                        homeplayer2_time=homeplayerslist[1][1].strftime('%M:%S'),
                        homeplayer3=homeplayerslist[2][0],
                        homeplayer3_time=homeplayerslist[2][1].strftime('%M:%S'),
                        ### Top3 away players
                        awayplayer1=awayplayerslist[0][0],
                        awayplayer1_time=awayplayerslist[0][1].strftime('%M:%S'),
                        awayplayer2=awayplayerslist[1][0],
                        awayplayer2_time=awayplayerslist[1][1].strftime('%M:%S'),
                        awayplayer3=awayplayerslist[2][0],
                        awayplayer3_time=awayplayerslist[2][1].strftime('%M:%S')
                    )
                    db.session.add(game)
#                   db.session.flush()
                    db.session.commit()
                except:
                    exit("Cannot upload to DB")


def home_players(game_id):
    teamdata = requests.get("https://statsapi.web.nhl.com/api/v1/game/" + game_id + "/boxscore").json()
    location = "home"
#    print("хозяева")
    return(top_three_players(teamdata=teamdata, location=location))


def away_players(game_id):
    teamdata = requests.get("https://statsapi.web.nhl.com/api/v1/game/" + game_id + "/boxscore").json()
    location = "away"
#    print("гости")
    return(top_three_players(teamdata=teamdata, location=location))


def top_three_players(teamdata, location):
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


result = get_teams()
