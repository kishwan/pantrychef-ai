import os
import httpx
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

THEMEALDB_API_KEY = os.getenv("THEMEALDB_API_KEY", "1")
BASE_URL = f"https://www.themealdb.com/api/json/v1/{THEMEALDB_API_KEY}"

async def search_recipes_by_ingredients(ingredients: List[str]) -> Optional[List[Dict]]:
    if not ingredients:
        return None
    
    ingredients_str = ",".join(ingredients)
    endpoint = f"{BASE_URL}/filter.php?i={ingredients_str}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(endpoint)
            response.raise_for_status()
            data = response.json()

            if data and data.get("meals"):
                return data["meals"]
            else:
                return None
        except httpx.HTTPStatusError as e:
            print(f"TheMealDB API HTTP error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"TheMealDB API request error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred with TheMealDB API: {e}")
            return None
        
async def get_meal_details_by_id(meal_id: str) -> Optional[Dict]:
    endpoint = f"{BASE_URL}/lookup.php?i={meal_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(endpoint)
            response.raise_for_status()
            data = response.json()

            if data and data.get("meals") and data["meals"][0]:
                return data["meals"][0]
            else:
                return None
        except httpx.HTTPStatusError as e:
            print(f"TheMealDB API HTTP error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"TheMealDB API request error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred with TheMealDB API: {e}")
            return None
