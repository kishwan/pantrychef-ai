import { useState } from 'react';

export default function RecipeCard({ recipe, backendUrl }) {
  const [aiQuestion, setAiQuestion] = useState('');
  const [aiAnswer, setAiAnswer] = useState('');
  const [loadingAi, setLoadingAi] = useState(false);

  const handleAskQuestion = async (event) => {
    event.preventDefault();
    if (!aiQuestion.trim()) {
      alert("Please type a question.");
      return;
    }

    setLoadingAi(true);
    setAiAnswer('');

    try {
      const response = await fetch(`${backendUrl}/recipes/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: aiQuestion,
          recipe_context: recipe.instructions
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`HTTP Error: ${errorData.detail} ${response.status}`);
      }

      const data = await response.json();
      setAiAnswer(data.answer);
    } catch (err) {
      console.error("Failed inference:", err);
      setAiAnswer(`Error: ${err.message || "An unknown error occurred."}`);
    } finally {
      setLoadingAi(false);
    }
  };

  return (
    <div className="recipe-card">
      {recipe.thumbnail && (
        <img
          src={recipe.thumbnail}
          alt={recipe.name}
          onError={(e) => { e.target.src = 'https://placehold.co/300x220/cccccc/000000?text=No+Image'; }}
        />
      )}
      <div className="recipe-content">
        <h3>{recipe.name}</h3>
        <p>Category: {recipe.category} | Area: {recipe.area}</p>

        {recipe.instructions && (
          <div className="ai-section">
            <form onSubmit={handleAskQuestion}>
              <input
                type="text"
                value={aiQuestion}
                onChange={(e) => setAiQuestion(e.target.value)}
                placeholder="Ask about this recipe..."
              />
              <button type="submit">Ask AI</button>
            </form>

            {loadingAi && <p className="thinking">Thinking...</p>}
            {aiAnswer && (
              <div className="ai-answer">
                <strong>Answer:</strong> {aiAnswer}
              </div>
            )}
          </div>
        )}

        <a
          href={`https://www.themealdb.com/meal/${recipe.id}`}
          target="_blank"
          rel="noopener noreferrer"
          className="details-link"
        >
          View Details
        </a>
      </div>
    </div>
  );
}