import pytest
import httpx
from unittest.mock import Mock, patch, AsyncMock

from backend.clients import themealdb_client


@pytest.fixture
def mock_httpx_get():
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None

        mock_get.return_value = mock_response
        yield mock_get, mock_response

@pytest.mark.asyncio
async def test_search_recipes_by_ingredients_success(mock_httpx_get):
    mock_get, mock_response = mock_httpx_get

    mock_response.json.return_value = {
        "meals": [
            {"idMeal": "52815", "strMeal": "Dino Nuggets", "strMealThumb": "thumb1.jpg"},
            {"idMeal": "52856", "strMeal": "Chicken Fajita Mac and Cheese", "strMealThumb": "thumb2.jpg"}
        ]
    }

    ingredients = ["chicken", "breading"]
    result = await themealdb_client.search_recipes_by_ingredients(ingredients)

    assert result is not None
    assert len(result) == 2
    assert result[0]["strMeal"] == "Dino Nuggets"
    mock_get.assert_called_once()
    assert "filter.php?i=chicken,breading" in mock_get.call_args[0][0]


@pytest.mark.asyncio
async def test_search_recipes_by_ingredients_no_results(mock_httpx_get):
    mock_get, mock_response = mock_httpx_get
    mock_response.json.return_value = {"meals": None}

    ingredients = ["imaginary_ingredient"]
    result = await themealdb_client.search_recipes_by_ingredients(ingredients)

    assert result is None
    mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_search_recipes_by_ingredients_empty_input():
    result = await themealdb_client.search_recipes_by_ingredients([])
    assert result is None


@pytest.mark.asyncio
async def test_search_recipes_by_ingredients_http_error(mock_httpx_get):
    mock_get, mock_response = mock_httpx_get
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "404",
        request=httpx.Request("GET", "url"),
        response=mock_response,
    )
    mock_response.json.return_value = {}

    ingredients = ["test"]
    result = await themealdb_client.search_recipes_by_ingredients(ingredients)

    assert result is None
    mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_search_recipes_by_ingredients_network_error(mock_httpx_get):
    mock_get, _ = mock_httpx_get
    mock_get.side_effect = httpx.RequestError(
        "Network is unreachable", request=httpx.Request("GET", "url")
    )

    ingredients = ["test"]
    result = await themealdb_client.search_recipes_by_ingredients(ingredients)

    assert result is None
    mock_get.assert_called_once()

@pytest.mark.asyncio
async def test_get_meal_details_by_id_success(mock_httpx_get):
    mock_get, mock_response = mock_httpx_get
    mock_response.json.return_value = {
        "meals": [
            {
                "idMeal": "52815",
                "strMeal": "Dino Nuggets",
                "strInstructions": "Heat oil...",
                "strCategory": "Chicken",
                "strArea": "Jurassic",
                "strIngredient1": "chicken",
                "strMeasure1": "1.5 kg",
            }
        ]
    }

    meal_id = "52815"
    result = await themealdb_client.get_meal_details_by_id(meal_id)

    assert result is not None
    assert result["strMeal"] == "Dino Nuggets"
    assert "strInstructions" in result
    mock_get.assert_called_once()
    assert "lookup.php?i=52815" in mock_get.call_args[0][0]


@pytest.mark.asyncio
async def test_get_meal_details_by_id_not_found(mock_httpx_get):
    mock_get, mock_response = mock_httpx_get
    mock_response.json.return_value = {"meals": None}

    meal_id = "99999"
    result = await themealdb_client.get_meal_details_by_id(meal_id)

    assert result is None
    mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_get_meal_details_by_id_http_error(mock_httpx_get):
    mock_get, mock_response = mock_httpx_get
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "500",
        request=httpx.Request("GET", "url"),
        response=mock_response,
    )
    mock_response.json.return_value = {}

    meal_id = "123"
    result = await themealdb_client.get_meal_details_by_id(meal_id)

    assert result is None
    mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_get_meal_details_by_id_network_error(mock_httpx_get):
    mock_get, _ = mock_httpx_get
    mock_get.side_effect = httpx.RequestError(
        "Connection Refused", request=httpx.Request("GET", "url")
    )

    meal_id = "123"
    result = await themealdb_client.get_meal_details_by_id(meal_id)

    assert result is None
    mock_get.assert_called_once()
