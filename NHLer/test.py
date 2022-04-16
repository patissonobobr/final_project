from flask_sqlalchemy import SQLAlchemy
from flask import Flask

test = Flask (__name__)
test.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NHLer.db'

db = SQLAlchemy(test)
class myclass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
print(123)
if __name__ == "__main__":
    test.run(debug=True)