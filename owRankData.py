from flask import Flask, request, Response, flash
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from sqlalchemy.sql import func

def main():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'enter_database_uri_here'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    # Creating the table of ranked data
    class Ranks(db.Model):
        __tablename__='ranks'
        id = db.Column(db.Integer, primary_key=True)
        tank = db.Column(db.Integer, nullable=False)
        damage =  db.Column(db.Integer, nullable=False)
        support =  db.Column(db.Integer, nullable=False)
        time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # Initializing the API so I can start using it
    url = "https://owapi.io/profile/pc/us/Perseus1277-1719"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"}
    r = requests.get(url, headers=headers)

    # Gets back the most recent tank, support, and damage rank from the API
    tankRank = r.json()['competitive']['tank']['rank']
    damageRank =  r.json()['competitive']['damage']['rank']
    supportRank =  r.json()['competitive']['support']['rank']

    # Goes back to the database and returns the most recent entry from there to ensure you upload the right one
    query = db.session.query(Ranks).order_by(Ranks.time_created.desc()).first()
    queryObject = {'tank': query.tank,
                    'damage': query.damage,
                    'support': query.support,
                    'timestamp': query.time_created}

    # Makes sure the data from the API is diff from the most recent row in the sql table, wont do anything if it the same
    if(tankRank != queryObject['tank'] or damageRank != queryObject['damage'] or supportRank != queryObject['support']):
        addRanks = Ranks(tank=tankRank, damage=damageRank, support=supportRank)
        db.session.add(addRanks)
        db.session.commit()
        print("Uploaded :D")


if __name__ == "__main__":
    main()
