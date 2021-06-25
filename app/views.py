from flask import current_app as app
from flask import request as flask_request
from flask import render_template
from flask import Response
# from . import 

from sqlalchemy import and_
import csv
import pandas as pd
import seaborn as sns
import io
import matplotlib.image

import uuid

from app.models.salary import Salary
from app.models.stats import Stats
from app import db



"""
select * from player_salary as sal
inner join player_stats stats on stats.player_name = sal.player_name and stats.season = sal.season_start
where season_start < 2010
and sal.player_name = 'Tracy McGrady'
order by salary desc

select * from player_salary
where player_name LIKE '%Tracy%'

"""


# TODO: Add exception handling
@app.route('/')
def index():
    print("index")
    stat_options = stats_column_mapping.items()
    return render_template('dashboard.html', stat_options=stat_options)


@app.route('/seed/6516854352asdffsdg')
def get():
    print("Seeding")
    # seed_salary_table()
    # seed_stats_table()
    return {"hello": "world"}

@app.route('/plot.png')
def plot_png():
    read_img = matplotlib.image.imread('plot.png')
    return Response(read_img, mimetype="image/png")


@app.route('/getVisual/scatterplot', methods=['POST'])
def post():
    print("scatter")
    params = flask_request.get_json(force=True)
    print(params)
    stat_selected = str(params['stat_selected'])

    img = io.BytesIO()

    # results = db.session\
        # .query(Stats.player_name, Salary.salary,Stats.season, Stats.team)\
        # .join(Salary, and_(Stats.season==Salary.season_start, Stats.player_name==Salary.player_name))\
        # .limit(2000)\
        # .all()


    results1 = db.session\
            .query(Stats.player_name, Salary.salary, Stats.season, Stats.team, getattr(Stats,stat_selected) )\
            .join(Salary, and_(Stats.season==Salary.season_start, Stats.player_name==Salary.player_name))\
            .filter(Stats.season > 1995)\
            .limit(4000)
    df = pd.read_sql(results1.statement, db.session.bind)
    # print(df)

    # players = sns.load_dataset(df)

    plot = sns.lmplot(
        data = df,
        x=stat_selected,
        y="salary",
        legend_out=True
    )

    file_path, filename = generate_filename()


    # fig = plot.get_figure()
    plot.savefig("{}".format(file_path))

    # sns.savefig(img, format="png")


    return {
        "filename": filename
    }




def generate_filename():
    filename = uuid.uuid4().hex
    return "app/static/{}.png".format(filename), "static/{}.png".format(filename)


salary_column_mapping = {
    'Register Value': "data_id",
    'Player Name':"player_name",
    'Salary in $':"salary",
    'Season Start':"season_start",
    'Season End': "season_end",
    'Team': "team_short",
    'Full Team Name':"team_full"
}


stats_column_mapping = {
    "Index": "data_id",
    "Year": "season",
    "Player": "player_name",
    "Pos": "position",
    "Age": "age",
    "Tm": "team",
    "G": "games_played",
    "GS": "games_started",
    "MP": "min_played",
    "PER": "per",
    "TS%": "true_shooting",
    "3PAr": "three_pt_att_rate",
    "FTr": "ft_rate",
    "ORB%": "off_reb_perc",
    "DRB%": "def_reb_perc",
    "TRB%": "total_reb_perc",
    "AST%": "assist_perc",
    "STL%": "steal_perc",
    "BLK%": "block_perc",
    "TOV%": "to_perc",
    "USG%": "usage_perc",
    "OWS": "offensive_win_shares",
    "DWS": "defensive_win_shares",
    "WS": "win_shares",
    "WS/48": "win_shares_per_48",
    "OBPM": "offensive_box_p_m",
    "DBPM": "defensive_box_p_m",
    "BPM": "box_p_m",
    "VORP": "var",
    "FG": "fg",
    "FGA": "fga",
    "FG%": "fg_perc",
    "3P": "three_pt_fg",
    "3PA": "three_pt_fga",
    "3P%": "three_pt_fg_perc",
    "2P": "two_pt_fg",
    "2PA": "two_pt_fga",
    "2P%": "two_pt_fg_perc",
    "eFG%": "effective_fg_perc",
    "FT": "ft",
    "FTA": "fta",
    "FT%": "ft_perc",
    "ORB": "off_reb",
    "DRB": "def_reb",
    "TRB": "reb",
    "AST": "assists",
    "STL": "steals",
    "BLK": "blocks",
    "TOV": "turnovers",
    "PF": "fouls",
    "PTS": "points"
}



    
def seed_salary_table():
    # TODO: Normalize salaries based on inflation
    with open('app/static/data/player_salaries.csv') as salary_file:
        csv_reader = csv.DictReader(salary_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            player_dict = {}
            for k, v in row.items():
                key, val = map_salaries(k, v)
                player_dict[key] = val
            player_salary = Salary(**player_dict)
            db.session.add(player_salary)
        db.session.commit()



def seed_stats_table():
    with open('app/static/data/player_stats.csv') as stats_file:
        csv_reader = csv.DictReader(stats_file, delimiter=',')
        for row in csv_reader:
            player_dict = {}
            for k, v in row.items():
                if k not in stats_column_mapping or not k or not v:
                    continue
                key, val = map_stats(k, v)
                player_dict[key] = val
            player_stats = Stats(**player_dict)
            db.session.add(player_stats)
        db.session.commit()


def map_salaries(key, value):
    if not value or len(value) == 0:
        return None
    return salary_column_mapping[key], value

def map_stats(key, value):
    if not value or len(value) == 0:
        return None
    return stats_column_mapping[key], value