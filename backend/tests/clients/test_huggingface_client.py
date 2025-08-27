import pytest
from unittest.mock import Mock, patch
from backend.clients import huggingface_client

@pytest.mark.asyncio
async def test_answer_question_success():
    mock_completion = Mock()
    mock_completion.choices = [
        Mock(message={"content": "Use 2 eggs for fluffier pancakes."})
    ]

    with patch.object(huggingface_client, "client", autospec=True) as mock_client:
        mock_client.chat.completions.create.return_value = mock_completion

        result = await huggingface_client.answer_question(
            question="How many eggs?",
            context="Ingredients: eggs, flour, sugar"
        )

        assert result == "Use 2 eggs for fluffier pancakes."
        mock_client.chat.completions.create.assert_called_once()
        kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert kwargs["max_tokens"] == 50


@pytest.mark.asyncio
async def test_answer_question_missing_token(monkeypatch):
    monkeypatch.setattr(huggingface_client, "HF_API_TOKEN", "")

    with pytest.raises(ValueError) as excinfo:
        await huggingface_client.answer_question("Q", "C")

    assert "Token not found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_answer_question_api_error():
    with patch.object(huggingface_client, "client", autospec=True) as mock_client:
        mock_client.chat.completions.create.side_effect = Exception("API failure")

        result = await huggingface_client.answer_question("Q", "C")

        assert result == "An error occurred while generating the AI response."
