import json
import random

def smart_title(recipe):
    """Generate a descriptive title based on recipe ingredients and cuisine."""
    cuisine = recipe.get("cuisine", "").title()
    ingredients = recipe.get("ingredients", [])
    lower_ingredients = [i.lower() for i in ingredients]

    main_keywords = ['chicken', 'beef', 'paneer', 'tofu', 'egg', 'fish', 'mushroom', 'pasta', 'rice', 'lentil', 'red lentils', 'potato', 'sweet potato']
    flavor_keywords = ['garlic', 'lime', 'chili', 'basil', 'soy', 'ginger', 'curry', 'tomato', 'butter', 'tumeric']
    style_keywords = {
        "Curry": ['garam masala', 'tumeric', 'curry', 'stew', 'lentil', 'red lentils'],
        "Stir-Fry": ['soy sauce', 'chili sauce', 'bell pepper', 'broccoli', 'sesame'],
        "Soup": ['broth', 'stock', 'noodle'],
        "Salad": ['lettuce', 'spinach', 'cucumber', 'vinaigrette'],
        "Grill": ['barbecue', 'grill', 'skewer']
    }

    # Identify main ingredient
    main = next((word.title() for word in main_keywords if any(word in ing for ing in lower_ingredients)), None)
    if not main:
        main = ingredients[0].title() if ingredients else "Special"

    # Identify flavor
    flavor = next((word.title() for word in flavor_keywords if any(word in ing for ing in lower_ingredients)), None)

    # Identify style
    style = next((st for st, triggers in style_keywords.items() if any(any(trigger in ing for trigger in triggers) for ing in lower_ingredients)), None)
    if not style:
        style = "Dish"

    # Generate title options
    options = []
    if cuisine:
        options.append(f"{cuisine} {style} with {main}")
    if flavor:
        options.append(f"{flavor} {main} {style}")
    if style != "Dish":
        options.append(f"{main} {style}")
    options.append(f"{flavor or 'Delicious'} {main}")  # fallback

    return random.choice([opt for opt in options if opt.strip()])

# Load and process dataset
with open("train.json", "r") as f:
    data = json.load(f)

for recipe in data:
    if "title" not in recipe or not recipe["title"].strip() or recipe["title"].startswith("Recipe #"):
        recipe["title"] = smart_title(recipe)

# Save to updated file
with open("train_updated_smart.json", "w") as f:
    json.dump(data, f, indent=2, sort_keys=True)

print("✅ Smart rule-based titles added. Check 'train_updated_smart.json' for updated recipes.")
