from flask import Flask, render_template, request
import pandas as pd
import os
import re

app = Flask(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "HaLaVeggie.xlsx")

# Excel 読み込み（存在しない場合のフォールバック）
try:
    df = pd.read_excel(DATA_PATH, engine="openpyxl")
except FileNotFoundError:
    df = pd.DataFrame()

# 列名・主要列の前処理
df.columns = df.columns.str.strip()
for col in ["Halal or Veg", "Genre"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()
    else:
        # 列が無い場合に備えて空列を作成
        df[col] = ""

# カテゴリ選択肢（ユニーク値）
categories = ["すべて"] + sorted(
    [v for v in df["Halal or Veg"].dropna().unique() if str(v).strip() != ""]
)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    selected_category = "すべて"
    selected_genre = ""

    filtered = df.copy()

    if request.method == "POST":
        selected_category = request.form.get("category") or "すべて"
        selected_genre = request.form.get("genre") or ""

        # カテゴリは完全一致（用途的にこちらが安全）
        if selected_category and selected_category != "すべて":
            filtered = filtered[filtered["Halal or Veg"] == selected_category]

        # ジャンルは部分一致（ユーザー入力を正規表現エスケープして安全に）
        if selected_genre:
            pattern = re.escape(selected_genre)
            filtered = filtered[filtered["Genre"].str.contains(pattern, case=False, na=False, regex=True)]

        results = filtered.to_dict(orient="records")



    selected_genres=selected_genre


if __name__ == "__main__":
    # 本番では debug=False 推奨
    app.run(debug=True)
