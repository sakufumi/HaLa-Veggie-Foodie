from flask import Flask
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
    halal_or_veg = db.Column(db.String(50))


# データベースを作成
with app.app_context():
    db.create_all()

with app.app_context():
    restaurants = [
        Restaurant(
            name="Vegetarian Cafe LOONEY",
            category="Cafe",
            genre="Vegetarian ･ Vegan",
            halal_or_veg="Vegetarian"
        ),
        Restaurant(
            name="Karakoma",
            category="Vegetarian restaurant",
            genre="Vegetable",
            halal_or_veg="Vegetarian"
        ),
        Restaurant(
            name="Chef Indian Curry",
            category="Indian cu",
            genre="Curry",
            halal_or_veg="Halal"
        )
    ]

    db.session.add_all(restaurants)
    db.session.commit()
    print("複数のレストランを追加しました！")
