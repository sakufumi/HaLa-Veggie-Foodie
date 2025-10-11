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
    area = db.Column(db.String(100))

# 🔍 検索ページ（トップ）
@app.route("/")
def index():
    genre = request.args.get("genre")
    type = request.args.get("type")
    area = request.args.get("area")  # 地域フィルターも追加！
    print(area)
    query = Restaurant.query
    if genre:
        query = query.filter(Restaurant.genre.contains(genre))
    if type:
        query = query.filter(Restaurant.halal_or_veg.contains(type))
    if area:
        query = query.filter(Restaurant.area.contains(area))  # 地域はcategory列で管理

    restaurants = query.all()
    return render_template("index.html", restaurants=restaurants)


# 🗺️ 地図ページ
@app.route("/map")
def map():
    return render_template("map.html")


if __name__ == "__main__":
    app.run(debug=True)
