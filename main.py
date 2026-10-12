from config import logger, settings as cfg

from get_data_from_db import clean_and_merge_foods, get_table_data
from db.create_connection import engine

from flask import Flask, render_template, request, flash, redirect, session

app = Flask(__name__)
app.secret_key = cfg.flask.secret_key.get_secret_value()
app.config["SESSION_TYPE"] = cfg.flask.session_type

table_data: dict[str, dict[str, list]] = get_table_data(engine)
foods = clean_and_merge_foods(table_data, sort_by="name", none_char="-")
print(foods)

_ATTRIBUTES = [
    "id",
    "name",
    "meal_type",
    "company",
    "kcal",
    "fats",
    "protein",
    "carbs",
    "fiber",
    "is_ingredient",
    "ingredients",
    "default_servings",
]


def get_meal_data(form_data: dict, attribute_name: str) -> str:
    return form_data.get(attribute_name, "").strip()


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", meal_results=foods)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        form_data = request.form.to_dict()
        for attribute in _ATTRIBUTES:
            form_data[attribute] = get_meal_data(form_data, attribute)
        return redirect("/add")
    
    ingredients = [food for food in foods if food['is_ingredient']]    
    return render_template("add.html", ingredients=ingredients)

if __name__ == "__main__":
    app.run(host=cfg.flask.host, port=cfg.flask.port, debug=cfg.DEBUG)