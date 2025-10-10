from app import app, db, Restaurant

def create_db():
    with app.app_context():  # ← これが水の器！
        db.create_all()

        restaurants = [
            Restaurant(name="Vegetarian Cafe LOONEY", category="Cafe", genre="Vegetarian・Vegan", halal_or_veg="Vegetarian"),
            Restaurant(name="Karakoma", category="Vegetarian restaurant", genre="Vegetable", halal_or_veg="Vegetarian"),
            Restaurant(name="Chef Indian Curry", category="Indian cu", genre="Curry", halal_or_veg="Halal")
        ]

        db.session.add_all(restaurants)
        db.session.commit()
        print("複数のレストランを追加しました！")

if __name__ == "__main__":
    create_db()


