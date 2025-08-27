from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import IngredientListRequest, RecipeSuggestionResponse, AnswerResponse, QuestionRequest
from .services import recipe_service

app = FastAPI(
    title="PantryChef AI Backend",
    description="API for smart recipe recommendations based on available ingredients.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    except HTTPException:
        print(f"HTTPException occurred while suggesting recipes.")
        raise
    except Exception as e:
        print(f"Error suggesting recipes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while suggesting recipes."
        )

@app.post(
    "/recipes/ask",
    response_model=AnswerResponse,
    summary="Ask question about recipe to AI"
)
async def ask_question_endpoint(request: QuestionRequest):
    if not request.question or not request.recipe_context:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing question"
        )
    try:
       answer = await recipe_service.answer_question(request.question, request.recipe_context)
       return AnswerResponse(answer=answer)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = str(e)
        )
    except Exception as e:
        print(f"Error answering question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e)
        )

@app.get("/", summary="Root endpoint for API status check")
async def root():
    """
    Returns a simple message to confirm the API is running.
    """
    return {"message": "Welcome to PantryChef AI Backend!"}