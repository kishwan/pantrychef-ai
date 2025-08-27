import pytest
from unittest.mock import AsyncMock, patch
from backend.services import recipe_service as service

@pytest.mark.asyncio
async def test_suggest_recipes_no_results():
    with patch.object(service, "themealdb_client") as mock_client:
        mock_client.search_recipes_by_ingredients = AsyncMock(return_value=None)

        result = await service.suggest_recipes(["chicken"])
        assert result == []
        mock_client.search_recipes_by_ingredients.assert_awaited_once_with(["chicken"])


@pytest.mark.asyncio
async def test_suggest_recipes_with_valid_recipes():
    with patch.object(service, "themealdb_client") as mock_client:
        mock_client.search_recipes_by_ingredients = AsyncMock(
            return_value=[{"idMeal": "123"}]
        )

        mock_client.get_meal_details_by_id = AsyncMock(
            return_value={
                "idMeal": "123",
                "strMeal": "Chicken Curry",
                "strCategory": "Chicken",
                "strArea": "Indian",
                "strInstructions": "Cook chicken with curry.",
                "strMealThumb": "thumb.jpg",
                "strYoutube": "youtube.com/example",
                "strIngredient1": "Chicken",
                "strMeasure1": "1 lb",
                "strIngredient2": " Curry Powder ",
                "strMeasure2": "2 tbsp",
                "strIngredient3": " ",
                "strMeasure3": "",
            }
        )

        result = await service.suggest_recipes(["chicken"])

        assert len(result) == 1
        recipe = result[0]
        assert recipe["id"] == "123"
        assert recipe["name"] == "Chicken Curry"
        assert recipe["category"] == "Chicken"
        assert recipe["area"] == "Indian"
        assert recipe["instructions"] == "Cook chicken with curry."
        assert recipe["thumbnail"] == "thumb.jpg"
        assert recipe["youtube_link"] == "youtube.com/example"
        assert recipe["ingredients"] == ["Chicken", "Curry Powder"]
        assert recipe["measures"] == ["1 lb", "2 tbsp"]

        mock_client.search_recipes_by_ingredients.assert_awaited_once()
        mock_client.get_meal_details_by_id.assert_awaited_once_with("123")


@pytest.mark.asyncio
async def test_suggest_recipes_skips_missing_details():
    with patch.object(service, "themealdb_client") as mock_client:
        mock_client.search_recipes_by_ingredients = AsyncMock(
            return_value=[{"idMeal": "111"}]
        )
        mock_client.get_meal_details_by_id = AsyncMock(return_value=None)

        result = await service.suggest_recipes(["test"])
        assert result == []


@pytest.mark.asyncio
async def test_answer_question_delegates_to_huggingface():
    with patch.object(service, "huggingface_client") as mock_client:
        mock_client.answer_question = AsyncMock(return_value="Mocked Answer")

        result = await service.answer_question("What is this?", "Recipe context")
        assert result == "Mocked Answer"

        mock_client.answer_question.assert_awaited_once_with(
            "What is this?", "Recipe context"
        )
