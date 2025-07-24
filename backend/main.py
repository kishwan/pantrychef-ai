from fastapi import FastAPI

app = FastAPI(
    title="PantryChef AI Backend",
    description="API for smart recipe recommendations based on available ingredients.",
    version="0.1.0"
)

@app.get("/meals", summary="Get a list of sample meal naems")
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