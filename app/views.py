from flask import current_app as app
# from . import 

from app.models.salary import Salary
import csv
from app import db


@app.route('/')
def hello():
    seed_salary_table()
    return {"hello": "world"}


    
def seed_salary_table():
    with open('app/static/data/player_salaries.csv') as stats_file:
        csv_reader = csv.DictReader(stats_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count < 20:
                line_count += 1
                player_salary = Salary(
                    id=row['Register Value'],
                    player_name=row['Player Name'],
                    salary=row['Salary in $'],
                    season_start=row['Season Start'],
                    season_end=row['Season End'],
                    team_short=row['Team'],
                    team_full=row['Full Team Name']
                )
                db.session.add(player_salary)
                db.session.commit()
                # db.session.flush()
                # print(row['Player Name'])
                # print(row['Salary in $'])

