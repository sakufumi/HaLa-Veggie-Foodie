from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///restaurants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    halal_or_veg = db.Column(db.String(100))

@app.route('/')
def index():
    genre = request.args.get('genre')
    type = request.args.get('type')

    query = Restaurant.query
    if genre:
        query = query.filter(Restaurant.genre.contains(genre))
    if type:
        query = query.filter(Restaurant.halal_or_veg.contains(type))

    restaurants = query.all()
    return render_template('index.html', restaurants=restaurants)

if __name__ == '__main__':
    app.run(debug=True)
