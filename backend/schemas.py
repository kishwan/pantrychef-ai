from pydantic import BaseModel
from typing import List, Optional

class IngredientListRequest(BaseModel):
    ingredients: List[str] # ex. ["chicken", "rice"]

# Response model for single recipe
class Recipe(BaseModel):
    id: str
    name: str
    category: Optional[str] = None
    area: Optional[str] = None
    instructions: Optional[str] = None
    thumbnail: Optional[str] = None
    youtube_link: Optional[str] = None
    ingredients: List[str]
    measures: List[str]

# Response model for overall recipe suggestion
class RecipeSuggestionResponse(BaseModel):
    recipes: List[Recipe]

class QuestionRequest(BaseModel):
    question: str
    recipe_context: str

class AnswerResponse(BaseModel):
    answer: str