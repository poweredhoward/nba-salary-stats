import os
import glob
from flask import current_app as application
from flask import request as flask_request
from flask import render_template
from flask import Response
from numpy import histogram
import numpy as np
from joblib import dump, load


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


TODAYS_SALARY_CAP = 101869000
pd.set_option('float_format', '{:.2f}'.format)

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
@application.route('/')
def index():
    all_data = entire_dataset()

    stat_options = stats_column_mapping.items()
    stat_options = list(stat_options)[6:]

    # stat_options = list(all_data.columns.values)
    years = db.session.query(Stats)\
        .distinct(Stats.season)\
        .filter(Stats.season > 1995)\
        .order_by(Stats.season.desc()).all()
    year_options = [ year.season for year in years ]
    position_options = ['PG', 'SG', 'G', 'SF', 'PF', 'F', 'C', 'All']

    optimized_fields = all_data[['% of cap', 'salary', 'cap', 'age', 'per', 'ppg', 'min_per_game', 'def_reb_per_game', 'fg_per_game', 'fga_per_game']]

    described = optimized_fields.describe()
    described.columns = ['% of Cap', 'Salary', 'Cap', 'Age', 'PER', 'PPG', 'MPG', 'DRPG', 'FG Made Per Game', 'FGA Per Game']
    described['Salary'] = described['Salary'].apply(lambda x: "${0:,.2f}".format(x))
    described['Cap'] = described['Cap'].apply(lambda x: "${0:,.2f}".format(x))
    relevant_data = described.loc[["mean", "std", "min", "25%", "50%", "75%", "max"]]


    return render_template(
        'dashboard.html',
        stat_options=stat_options,
        year_options = year_options[1:],
        position_options = position_options,
        description_table_data=[relevant_data.to_html(classes="table table-striped", header="false")],
        description_table_cols = relevant_data.columns.values
        )



@application.route('/clear-pictures/sdfpgup9fdsfsd9f2345', methods=['GET'])
def clear_pics():
    files = glob.glob("./app/static/generated/*")
    for f in files:
        os.remove(f)
    return "success"


@application.route('/prediction/salary', methods=['POST'])
def get_prediction():
    params = flask_request.get_json(force=True)
    print(params)

    input = np.array([[
        float(params['age']),
        float(params['per']), 
        float(params['ppg']), 
        float(params['min_per_game']), 
        float(params['def_reb_per_game']), 
        float(params['fg_per_game']), 
        float(params['fga_per_game'])
    ]])


    model = load('random_forest_model_2000_final.joblib')
    salary_prediction = model.predict(input)

    raw_prediction = (float(salary_prediction[0]) / 100) * TODAYS_SALARY_CAP
    formatted_float = "${:,.2f}".format(raw_prediction)

    return {
        "salary_prediction": formatted_float
    }



@application.route('/seed/6516854352asdffsdg')
def get():
    seed_salary_table()
    seed_stats_table()
    return {"hello": "world"}


@application.route('/getVisual/scatterplot', methods=['POST'])
def post():
    params = flask_request.get_json(force=True)
    stat_selected = str(params['stat_selected'])
    year_selected = int(params['year_selected'])
    position_selected = "%{}%".format(str(params['position_selected']))

    img = io.BytesIO()

    
    filters = [Salary.season_start > year_selected]
    if position_selected and "All" not in position_selected:
        filters.append((Stats.position.like(position_selected)))

    f = and_(*filters)
 
    results1 = db.session\
            .query(Stats.player_name, Salary.salary, Stats.season, Stats.team, getattr(Stats,stat_selected) )\
            .join(Salary, and_(Stats.season==Salary.season_start, Stats.player_name==Salary.player_name))\
            .filter(f)\
            .limit(4000)
        
    
    df = pd.read_sql(results1.statement, db.session.bind)


    # TODO: Set boundaries of Y axis for max salary
    scatterplot = sns.lmplot(
        data = df,
        x=stat_selected,
        y="salary"
    )

    file_path, scatterplot_filename = generate_filename()
    scatterplot.savefig("{}".format(file_path))


    histogram = sns.displot(df["salary"], bins=100)
    file_path, histogram_filename = generate_filename()
    histogram.savefig("{}".format(file_path))


    return {
        "scatterplot_filename": scatterplot_filename,
        "histogram_filename": histogram_filename
    }




def generate_filename():
    filename = uuid.uuid4().hex
    return "app/static/generated/{}.png".format(filename), "static/generated/{}.png".format(filename)



def entire_dataset():
    stats_dataset = pd.read_csv("salary-data_2000.csv")
    stats_dataset.dropna()
    stats_dataset['ppg'] = stats_dataset['points'] / stats_dataset['games_played']
    stats_dataset['min_per_game'] = stats_dataset['min_played'] / stats_dataset['games_played']
    stats_dataset['off_reb_per_game'] = stats_dataset['off_reb'] / stats_dataset['games_played']
    stats_dataset['assists_per_game'] = stats_dataset['assists'] / stats_dataset['games_played']
    stats_dataset['reb_per_game'] = stats_dataset['reb'] / stats_dataset['games_played']
    stats_dataset['off_reb_per_game'] = stats_dataset['off_reb'] / stats_dataset['games_played']
    stats_dataset['def_reb_per_game'] = stats_dataset['def_reb'] / stats_dataset['games_played']
    stats_dataset['ft_per_game'] = stats_dataset['ft'] / stats_dataset['games_played']
    stats_dataset['fta_per_game'] = stats_dataset['fta'] / stats_dataset['games_played']
    stats_dataset['fg_per_game'] = stats_dataset['fg'] / stats_dataset['games_played']
    stats_dataset['fga_per_game'] = stats_dataset['fga'] / stats_dataset['games_played']
    stats_dataset['blocks_per_game'] = stats_dataset['blocks'] / stats_dataset['games_played']
    stats_dataset['steals_per_game'] = stats_dataset['steals'] / stats_dataset['games_played']
    stats_dataset['turnovers_per_game'] = stats_dataset['turnovers'] / stats_dataset['games_played']
    stats_dataset['fouls_per_game'] = stats_dataset['fouls'] / stats_dataset['games_played']

    salary_caps = pd.read_csv("salary-cap.csv", index_col=0).to_dict()
    cap = salary_caps['Salary Cap']
    stats_dataset['cap'] = stats_dataset['season'].map(cap)
    stats_dataset["% of cap"] = (stats_dataset['salary']/stats_dataset['cap'])*100


    return stats_dataset






optimized_fields = ['% of cap', 'age', 'per', 'ppg', 'min_per_game', 'def_reb_per_game', 'fg_per_game', 'fga_per_game']

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