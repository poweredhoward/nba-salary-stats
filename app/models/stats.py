from app import db


class Stats(db.Model):
    __tablename__ = "player_stats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_id = db.Column(db.Integer)
    player_name = db.Column(db.String(100))
    season = db.Column(db.Integer)
    position = db.Column(db.String(100))
    age = db.Column(db.Integer)
    team = db.Column(db.String(100))
    games_played = db.Column(db.Integer)
    games_started = db.Column(db.Integer)
    min_played = db.Column(db.Integer)
    per = db.Column(db.Float)
    true_shooting = db.Column(db.Float)
    three_pt_att_rate = db.Column(db.Float)
    ft_rate = db.Column(db.Float)
    off_reb_perc = db.Column(db.Float)
    def_reb_perc = db.Column(db.Float)
    total_reb_perc = db.Column(db.Float)
    assist_perc = db.Column(db.Float)
    steal_perc = db.Column(db.Float)
    block_perc = db.Column(db.Float)
    to_perc = db.Column(db.Float)
    usage_perc = db.Column(db.Float)
    offensive_win_shares = db.Column(db.Float)
    defensive_win_shares = db.Column(db.Float)
    win_shares = db.Column(db.Float)
    win_shares_per_48 = db.Column(db.Float)
    offensive_box_p_m = db.Column(db.Float)
    defensive_box_p_m = db.Column(db.Float)
    box_p_m = db.Column(db.Float)
    var = db.Column(db.Float)
    fg = db.Column(db.Float)
    fga = db.Column(db.Integer)
    fg_perc = db.Column(db.Float)
    three_pt_fg = db.Column(db.Integer)
    three_pt_fga = db.Column(db.Integer)
    three_pt_fg_perc = db.Column(db.Float)
    two_pt_fg = db.Column(db.Integer)
    two_pt_fga = db.Column(db.Float)
    two_pt_fg_perc = db.Column(db.Float)
    effective_fg_perc = db.Column(db.Float)
    ft = db.Column(db.Integer)
    fta = db.Column(db.Integer)
    ft_perc = db.Column(db.Float)
    off_reb = db.Column(db.Integer)
    def_reb = db.Column(db.Integer)
    reb = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    steals = db.Column(db.Integer)
    blocks = db.Column(db.Integer)
    turnovers = db.Column(db.Integer)
    fouls = db.Column(db.Integer)
    points = db.Column(db.Integer)   



    # def __init__(self, **kwargs):
    #     for k, v in kwargs.iteritems():
    #         self.k = v

    
    def __repr__(self):
        return "#{}  {}   {}-{}({})".format(self.id, self.player_name, self.season_start, self.season_end, self.team_short)

