from os import stat
from flask import current_app as app
from flask import request as flask_request
from flask import render_template
from flask import Response
from numpy import histogram
import numpy as np
from joblib import dump, load

# from . import 

from sqlalchemy import and_
import csv
import pandas as pd
import seaborn as sns
import io
import matplotlib.image
import matplotlib
matplotlib.use('Agg')

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


# TODO: Add exception handling!!!
@app.route('/')
def index():
    stat_options = stats_column_mapping.items()
    years = db.session.query(Salary)\
        .distinct(Salary.season_start)\
        .filter(Salary.season_start > 1995)\
        .order_by(Salary.season_start.desc()).all()
    year_options = [ year.season_start for year in years ]
    position_options = ['PG', 'SG', 'G', 'SF', 'PF', 'F', 'C']

    return render_template(
        'dashboard.html',
        stat_options=stat_options,
        year_options = year_options,
        position_options = position_options
        )


@app.route('/prediction/salary', methods=['POST'])
def get_prediction():
    params = flask_request.get_json(force=True)
    print(params)

    input = np.array([[
        float(params['min_played']),
        float(params['true_shooting']),
        float(params['off_reb_perc']),
        float(params['to_perc']),
        float(params['offensive_box_p_m']),
        float(params['off_reb']),
        float(params['points'])
    ]])

    # [1398, 0.516, 5.241, 13.8, 1, 50, 1000] -> 10313240.13318653

    model = load('random_forest_model.joblib')
    salary_prediction = model.predict(input)
    print(salary_prediction)

    return salary_prediction



@app.route('/seed/6516854352asdffsdg')
def get():
    print("Seeding")
    seed_salary_table()
    seed_stats_table()
    return {"hello": "world"}

@app.route('/plot.png')
def plot_png():
    read_img = matplotlib.image.imread('plot.png')
    return Response(read_img, mimetype="image/png")




@app.route('/getVisual/scatterplot', methods=['POST'])
def post():
    params = flask_request.get_json(force=True)
    print(params)
    stat_selected = str(params['stat_selected'])
    year_selected = int(params['year_selected'])
    position_selected = "%{}%".format(str(params['position_selected']))

    img = io.BytesIO()

    # results = db.session\
        # .query(Stats.player_name, Salary.salary,Stats.season, Stats.team)\
        # .join(Salary, and_(Stats.season==Salary.season_start, Stats.player_name==Salary.player_name))\
        # .limit(2000)\
        # .all()


    results1 = db.session\
            .query(Stats.player_name, Salary.salary, Stats.season, Stats.team, getattr(Stats,stat_selected) )\
            .join(Salary, and_(Stats.season==Salary.season_start, Stats.player_name==Salary.player_name))\
            .filter(Salary.season_start > year_selected)\
            .filter(Stats.position.like(position_selected))\
            .limit(4000)
    
    df = pd.read_sql(results1.statement, db.session.bind)
    # print(df)

    # players = sns.load_dataset(df)

    # TODO: Set boundaries of Y axis for max salary
    scatterplot = sns.lmplot(
        data = df,
        x=stat_selected,
        y="salary"
    )

    file_path, scatterplot_filename = generate_filename()
    scatterplot.savefig("{}".format(file_path))


    # histogram = sns.displot(
    #     data = df,
    #     x=stat_selected,
    #     y="salary",
    #     kind="kde"
    # )
    histogram = sns.displot(df["salary"], bins=100)
    file_path, histogram_filename = generate_filename()
    histogram.savefig("{}".format(file_path))



    heatmap = sns.boxplot(
        data = df,
        x=stat_selected,
        y="salary"
    )
    file_path, heatmap_filename = generate_filename()
    heatmap.figure.savefig("{}".format(file_path))

    # fig = plot.get_figure()

    # plot.close()

    # sns.savefig(img, format="png")


    return {
        "scatterplot_filename": scatterplot_filename,
        "histogram_filename": histogram_filename,
        "heatmap_filename": heatmap_filename
    }




def generate_filename():
    filename = uuid.uuid4().hex
    return "app/static/{}.png".format(filename), "static/{}.png".format(filename)





"""
select 
    distinct
    sal.salary,
    stats.age,
    stats.games_played,
    stats.games_started,
    stats.min_played,
    stats.per,
    stats.true_shooting,
    stats.three_pt_att_rate,
    stats.ft_rate,
    stats.off_reb_perc,
    stats.def_reb_perc,
    stats.total_reb_perc,
    stats.assist_perc,
    stats.steal_perc,
    stats.block_perc,
    stats.to_perc,
    stats.usage_perc,
    stats.offensive_win_shares,
    stats.defensive_win_shares,
    stats.win_shares,
    stats.win_shares_per_48,
    stats.offensive_box_p_m,
    stats.defensive_box_p_m,
    stats.box_p_m,
    stats.var,
    stats.fg,
    stats.fga,
    stats.fg_perc,
    stats.three_pt_fg,
    stats.three_pt_fga,
    stats.three_pt_fg_perc,
    stats.two_pt_fg,
    stats.two_pt_fga,
    stats.two_pt_fg_perc,
    stats.effective_fg_perc,
    stats.ft,
    stats.fta,
    stats.ft_perc,
    stats.off_reb,
    stats.def_reb,
    stats.reb,
    stats.assists,
    stats.steals,
    stats.blocks,
    stats.turnovers,
    stats.fouls,
    stats.points
from player_salary AS sal
INNER JOIN player_stats AS stats
ON sal.season_start=stats.season AND sal.player_name=stats.player_name

"""



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