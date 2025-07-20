import json
import os
import joblib
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Load nutrition and training data
with open("nutrition_data.json") as f:
    nutrition_data = json.load(f)

with open("train.json") as f:
    recipe_data = json.load(f)

# Load user data
shopping_list = json.load(open("shopping_list.json")) if os.path.exists("shopping_list.json") else []
user_recipes = json.load(open("user_recipes.json")) if os.path.exists("user_recipes.json") else []

# Load model and vectorizer
model = joblib.load("recipe_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# ----------------------------
# HOME / DASHBOARD
# ----------------------------

@app.route("/")
def home():
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    ingredients_data = load_ingredients()
    current_ingredients = [item.lower() for item in ingredients_data]

    def get_match_count(recipe_ingredients):
        return sum(1 for ing in recipe_ingredients if ing.lower() in current_ingredients)

    filtered_recipes = [
        {
            "title": r["title"],
            "cuisine": r["cuisine"],
            "ingredients": r["ingredients"],
            "instructions": r.get("instructions", "Instructions not available."),
            "match_count": get_match_count(r["ingredients"])
        }
        for r in recipe_data if get_match_count(r["ingredients"]) > 0
    ]

    filtered_recipes.sort(key=lambda x: x["match_count"], reverse=True)
    top_recipes = filtered_recipes[:15]

    for recipe in top_recipes:
        recipe["nutrition"] = calculate_nutrition(recipe["ingredients"])

    return render_template("dashboard.html",
                       recipes=top_recipes,
                       inventory=ingredients_data,
                       shopping_list=shopping_list,
                       user_recipes=user_recipes,
                       nutrition_info=calculate_nutrition(ingredients_data))

# ----------------------------
# NUTRITION CALCULATION
# ----------------------------

def calculate_nutrition(ingredients):
    total = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
    for ing in ingredients:
        entry = nutrition_data.get(ing.lower())
        if entry:
            for key in total:
                total[key] += entry.get(key, 0)
    return total


# ----------------------------
# INVENTORY MANAGEMENT
# ----------------------------

@app.route("/inventory", methods=["GET", "POST"])
def manage_inventory():
    ingredients = load_ingredients()

    # Add item (POST)
    if request.method == "POST":
        new_item = request.form.get("new_item", "").strip()
        if new_item and new_item.lower() not in [i.lower() for i in ingredients]:
            ingredients.append(new_item)
            save_ingredients(ingredients)
        return redirect(url_for("manage_inventory"))

    # Delete item (GET)
    delete_item = request.args.get("delete", "").strip().lower()
    if delete_item:
        ingredients = [i for i in ingredients if i.strip().lower() != delete_item]
        save_ingredients(ingredients)
        return redirect(url_for("manage_inventory"))

    return render_template("inventory.html", ingredients=ingredients)


def load_ingredients():
    try:
        if not os.path.exists("ingredients.json"):
            return []
        with open("ingredients.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_ingredients(ingredients):
    with open("ingredients.json", "w") as f:
        json.dump(ingredients, f, indent=2)

# ----------------------------
# RECIPE MANAGEMENT
# ----------------------------

@app.route("/ingredients", methods=["GET", "POST"])
def manage_ingredients():
    ingredients = load_ingredients()
    return render_template("ingredients.html", ingredients=ingredients, recipes=user_recipes)

@app.route("/add-user-recipe", methods=["POST"])
def add_user_recipe():
    title = request.form.get("title", "").strip()
    ingredients = request.form.get("ingredients", "").split(",")
    instructions = request.form.get("instructions", "").strip()

    if title and ingredients:
        new_recipe = {
            "id": len(user_recipes) + 1,
            "title": title,
            "ingredients": [i.strip().lower() for i in ingredients],
            "instructions": instructions,
            "cuisine": predict_cuisine(ingredients)
        }
        user_recipes.append(new_recipe)
        with open("user_recipes.json", "w") as f:
            json.dump(user_recipes, f, indent=2)

    return redirect(url_for("manage_ingredients"))

@app.route("/delete-user-recipe/<int:rid>")
def delete_user_recipe(rid):
    global user_recipes
    user_recipes = [r for r in user_recipes if r["id"] != rid]
    with open("user_recipes.json", "w") as f:
        json.dump(user_recipes, f, indent=2)
    return redirect(url_for("manage_ingredients"))

# ----------------------------
# SHOPPING LIST
# ----------------------------

@app.route("/shopping-list", methods=["GET", "POST"])
def shopping():
    if request.method == "POST":
        new_item = request.form.get("new_item", "").strip().lower()
        if new_item and new_item not in shopping_list:
            shopping_list.append(new_item)
            with open("shopping_list.json", "w") as f:
                json.dump(shopping_list, f, indent=2)
        return redirect(url_for("shopping"))
    return render_template("shopping_list.html", shopping_list=shopping_list)

@app.route("/delete-shopping/<item>")
def delete_shopping(item):
    if item in shopping_list:
        shopping_list.remove(item)
        with open("shopping_list.json", "w") as f:
            json.dump(shopping_list, f, indent=2)
    return redirect(url_for("shopping"))

# ----------------------------
# CUISINE PREDICTION
# ----------------------------

def predict_cuisine(ingredients):
    text = " ".join(ingredients).lower()
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]

# ----------------------------
# RUN
# ----------------------------

if __name__ == "__main__":
    app.run(debug=True)
