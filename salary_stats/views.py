# from app import db
# print(app)

from salary_stats import app

@app.route('/')
def hello():
    return {"hello": "world"}

