from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import IngredientListRequest, RecipeSuggestionResponse
from services import recipe_service

app = FastAPI(
    title="PantryChef AI Backend",
    description="API for smart recipe recommendations based on available ingredients.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO KISH: FIGURE OUT WHAT SHOULD GO IN CORS FOR PROD
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post(
    "/recipes/suggest",
    response_model=RecipeSuggestionResponse,
    summary="Suggest recipes based on available ingredients"
)
async def suggest_recipes_endpoint(request: IngredientListRequest):
    if not request.ingredients:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No recipes found for given ingredients"
        )
    try:
        suggested_recipes = await recipe_service.suggest_recipes(request.ingredients)
        if not suggested_recipes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
        return RecipeSuggestionResponse(recipes=suggested_recipes)
    except Exception as e:
        print(f"Error suggesting recipes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while suggesting recipes."
        )

@app.get("/meals", summary="Get a list of sample meal names")
async def get_meals():
    meal_names = [
        "Spaghetti Carbonara",
        "Chicken Stir-fry",
        "Lentil Soup",
        "Vegetable Curry",
        "Breakfast Burrito"
    ]
    return {"meals": meal_names}

@app.get("/", summary="Root endpoint for API status check")
async def root():
    """
    Returns a simple message to confirm the API is running.
    """
    return {"message": "Welcome to PantryChef AI Backend!"}