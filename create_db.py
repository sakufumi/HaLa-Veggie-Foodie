from peewee import *

# SQLiteファイル名を指定（このファイルが作られる！）
db = SqliteDatabase('restaurants.db')

class Restaurant(Model):
    name = CharField()
    category = CharField()
    genre = CharField()
    halal_or_veg = CharField()
    address = TextField()
    map_url = TextField()

    class Meta:
        database = db

# DB接続＆テーブル作成（ここで .db ファイルが生成される！）
db.connect()
db.create_tables([Restaurant])
