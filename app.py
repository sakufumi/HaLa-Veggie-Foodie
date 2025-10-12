from csv import register_dialect
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Float

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///restaurants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "your_secret_key"  # セッション管理などに必要

db = SQLAlchemy(app)


# レストランモデル
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    halal_or_veg = db.Column(db.String(100))
    area = db.Column(db.String(100))
    latitude = db.Column(Float)
    longtitude = db.Column(Float)


# 🔍 検索ページ（トップ）
@app.route("/")
def index():
    genre = request.args.get("genre")
    type = request.args.get("type")
    area = request.args.get("area")
    query = Restaurant.query
    if genre:
        query = query.filter(Restaurant.genre.contains(genre))
    if type:
        query = query.filter(Restaurant.halal_or_veg.contains(type))
    if area:
        query = query.filter(Restaurant.area.contains(area))
    restaurants = query.all()
    return render_template("index.html", restaurants=restaurants)


# 🗺️ 地図ページ
@app.route("/map")
def map():
    return render_template("map.html")


# # 🔐 管理ページ（表示）
# @app.route("/admin")
# def admin():
#     return render_template("admin.html")


# ✏️ 管理ページ（追加処理）
@app.route("/admin/add", methods=["GET", "POST"])
def add_restaurant():
    if request.method == "POST":
        try:
            new_restaurant = Restaurant(
                name=request.form["name"],
                category=request.form["category"],
                genre=request.form["genre"],
                halal_or_veg=request.form["halal_or_veg"],
                area=request.form["area"],
                latitude=float(request.form["latitude"]),
                longtitude=float(request.form["longtitude"]),
            )
            db.session.add(new_restaurant)
            db.session.commit()
            return redirect(url_for("index"))
        except Exception as e:
            return f"追加に失敗しました: {e}", 400
            return redirect(url_for("add_restaurant"))    
    return render_template("admin.html")    


if __name__ == "__main__":
    app.run(debug=True)
