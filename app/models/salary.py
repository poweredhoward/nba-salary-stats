from app import db

class Salary(db.Model):
    __tablename__ = "player_salary"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_id = db.Column(db.Integer)
    player_name = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    season_start = db.Column(db.Integer)
    season_end = db.Column(db.Integer)
    team_short = db.Column(db.String(10))
    team_full = db.Column(db.String(100))


    def __repr__(self):
        return "#{}  {}   {}-{}({})".format(self.id, self.player_name, self.season_start, self.season_end, self.team_short)

