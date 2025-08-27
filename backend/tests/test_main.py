import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from backend.main import app


def make_client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_root_endpoint():
    async with make_client() as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to PantryChef AI Backend!"}


@pytest.mark.asyncio
async def test_suggest_recipes_empty_ingredients():
    async with make_client() as ac:
        response = await ac.post("/recipes/suggest", json={"ingredients": []})
    assert response.status_code == 400
    assert response.json()["detail"] == "No recipes found for given ingredients"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_return,expected_status,expected_key",
    [
        ([], 404, None),                      # no recipes found
        (Exception("Boom"), 500, "detail"),   # server error
    ],
)
async def test_suggest_recipes_failure_cases(mock_return, expected_status, expected_key):
    if isinstance(mock_return, Exception):
        mock = AsyncMock(side_effect=mock_return)
    else:
        mock = AsyncMock(return_value=mock_return)

    with patch("backend.main.recipe_service.suggest_recipes", mock):
        async with make_client() as ac:
            response = await ac.post("/recipes/suggest", json={"ingredients": ["chicken"]})

        assert response.status_code == expected_status
        if expected_key:
            assert expected_key in response.json()


@pytest.mark.asyncio
async def test_suggest_recipes_success():
    fake_recipe = {
        "id": "1",
        "name": "Chicken Curry",
        "category": "Chicken",
        "area": "Indian",
        "instructions": "Cook chicken.",
        "thumbnail": "thumb.jpg",
        "youtube_link": "yt.com",
        "ingredients": ["Chicken"],
        "measures": ["1 lb"],
    }
    with patch("backend.main.recipe_service.suggest_recipes", AsyncMock(return_value=[fake_recipe])):
        async with make_client() as ac:
            response = await ac.post("/recipes/suggest", json={"ingredients": ["chicken"]})
        assert response.status_code == 200
        data = response.json()
        assert data["recipes"][0]["name"] == "Chicken Curry"


@pytest.mark.asyncio
async def test_ask_question_missing_fields():
    async with make_client() as ac:
        response = await ac.post("/recipes/ask", json={"question": "", "recipe_context": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Missing question"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "side_effect,expected_status,expected_body",
    [
        (AsyncMock(return_value="Mocked Answer"), 200, {"answer": "Mocked Answer"}),
        (AsyncMock(side_effect=ValueError("Bad input")), 400, {"detail": "Bad input"}),
        (AsyncMock(side_effect=Exception("Boom")), 500, {"detail": "Boom"}),
    ],
)
async def test_ask_question_various_cases(side_effect, expected_status, expected_body):
    with patch("backend.main.recipe_service.answer_question", side_effect):
        async with make_client() as ac:
            response = await ac.post(
                "/recipes/ask",
                json={"question": "Q", "recipe_context": "C"},
            )

        assert response.status_code == expected_status
        for key, value in expected_body.items():
            assert response.json()[key] == value
