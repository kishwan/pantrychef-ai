from typing import List, Dict, Optional
from clients import themealdb_client

async def suggest_recipes(ingredients: List[str]) -> List[Dict]:
    received_recipes = await themealdb_client.search_recipes_by_ingredients(ingredients)

    if not received_recipes:
        return []

    full_recipes = []
    for meal in received_recipes:
        meal_id = meal.get("idMeal")
        if meal_id:
            details = await themealdb_client.get_meal_details_by_id(meal_id)
            if details:
                processed_recipe = {
                    "id": details.get("idMeal"),
                    "name": details.get("strMeal"),
                    "category": details.get("strCategory"),
                    "area": details.get("strArea"),
                    "instructions": details.get("strInstructions"),
                    "thumbnail": details.get("strMealThumb"),
                    "youtube_link": details.get("strYoutube"),
                    "ingredients": [],
                    "measures": []
                }

                for i in range(1, 21): # 20 ingredient MAX
                    ingredient = details.get(f"strIngredient{i}")
                    measure = details.get(f"strMeasure{i}")
                    if ingredient and ingredient.strip():
                        processed_recipe["ingredients"].append(ingredient.strip())
                        processed_recipe["measures"].append(measure.strip() if measure else "")
                full_recipes.append(processed_recipe)
    return full_recipes   