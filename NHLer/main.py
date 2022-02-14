import requests
from flask import Flask
from requests import request

def get_teams():
    url = "https://statsapi.web.nhl.com/api/v1/teams"
    data = requests.get(url).json()
    return data

result=get_teams()
print(result)

app = Flask(__name__)

@app.route('/')
def index():
    return data.text

@app.route('/test')
def test():
    return data.text

if __name__ == "__main__":
    app.run(debug=True)