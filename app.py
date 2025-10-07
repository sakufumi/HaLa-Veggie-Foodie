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

# 列名・主要列の前処理（列名が非文字列でも安全にトリム）
df.columns = pd.Index([("" if pd.isna(c) else str(c).strip()) for c in df.columns])

for col in ["Halal or Veg", "Genre"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()
    else:
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

        # カテゴリは完全一致
        if selected_category and selected_category != "すべて":
            filtered = filtered[filtered["Halal or Veg"] == selected_category]

        # ジャンルは部分一致（大文字小文字無視）
        if selected_genre:
            pattern = re.escape(selected_genre)
            filtered = filtered[
                filtered["Genre"].astype(str).str.contains(pattern, case=False, na=False, regex=True)
            ]

        results = filtered.to_dict(orient="records")

    return render_template(
        "index.html",
        categories=categories,
        selected_category=selected_category,
        selected_genre=selected_genre,
        results=results,
    )

if __name__ == "__main__":
    # 本番では debug=False 推奨
    app.run(debug=True)
