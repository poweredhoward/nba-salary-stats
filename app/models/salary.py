from app import db

class Salary(db.Model):
    __tablename__ = "player_salary"

    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    season_start = db.Column(db.Integer)
    season_end = db.Column(db.Integer)
    team_short = db.Column(db.String(10))
    team_full = db.Column(db.String(100))

    def __init__(self, id, name, salary, season_start, season_end, team_short, team_full):
        id = db.Column(db.Integer, primary_key=True)
        player_name = self.player_name
        salary = self.salary
        season_start = self.season_start
        season_end = self.season_end
        team_short = self.team_short
        team_full = self.team_full
    

    def __repr__(self):
        return "#{}  {}   {}-{}({})".format(self.id, self.player_name, self.season_start, self.season_end, self.team_short)

