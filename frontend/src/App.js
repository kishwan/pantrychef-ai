import React, { useState } from 'react';
import './App.css';

function App() {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [ingredientsInput, setIngredientsInput] = useState('');
  
  const BACKEND_URL = 'http://127.0.0.1:8000';

  const fetchRecipes = async (ingredients) => {
    setLoading(true);
    setError(null);
    setRecipes([]);

    if (!ingredients.trim()) {
      setError("Please enter at least one ingredient.");
      setLoading(false);
      return;
    }

    const ingredientList = ingredients.split(',').map(item => item.trim()).filter(item => item !== '');

    try {
      const response = await fetch(`${BACKEND_URL}/recipes/suggest`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ingredients: ingredientList }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setRecipes(data.recipes);
    } catch (err) {
      console.error("Failed to fetch recipes:", err);
      setError(err.message || "An unknown error occurred.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetchRecipes(ingredientsInput);
  };

  return (
    <div className="App">
      <header className="App-header" style={{ backgroundColor: '#29742dff'}}>
        <h1>PantryChef AI</h1>
        <p>Discover recipes based on what you have!</p>
      </header>

      <main style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
        <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
          <input
            type="text"
            value={ingredientsInput}
            onChange={(e) => setIngredientsInput(e.target.value)}
            placeholder="Enter ingredients (e.g., chicken, rice)"
            style={{ width: '70%', padding: '10px', marginRight: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
          />
          <button type="submit" style={{ padding: '10px 20px', borderRadius: '5px', border: 'none', backgroundColor: '#61dafb', color: 'white', cursor: 'pointer' }}>
            Find Recipes
          </button>
        </form>

        {loading && <p>Loading recipes...</p>}
        {error && <p style={{ color: 'red' }}>Error: {error}</p>}

        <div className="recipe-list" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '20px' }}>
          {recipes.length > 0 ? (
            recipes.map((recipe) => (
              <div key={recipe.id} className="recipe-card" style={{ border: '1px solid #eee', borderRadius: '8px', overflow: 'hidden', boxShadow: '0 2px 5px rgba(0,0,0,0.1)' }}>
                {recipe.thumbnail && (
                  <img
                    src={recipe.thumbnail}
                    alt={recipe.name}
                    style={{ width: '100%', height: '180px', objectFit: 'cover' }}
                    onError={(e) => { e.target.onerror = null; e.target.src = 'https://placehold.co/250x180/cccccc/000000?text=No+Image'; }}
                  />
                )}
                <div style={{ padding: '15px' }}>
                  <h3 style={{ margin: '0 0 10px 0', fontSize: '1.2em' }}>{recipe.name}</h3>
                  <p style={{ fontSize: '0.9em', color: '#555' }}>
                    Category: {recipe.category} | Area: {recipe.area}
                  </p>
                  <a href={`https://www.themealdb.com/meal/${recipe.id}`} target="_blank" rel="noopener noreferrer"
                     style={{ display: 'inline-block', marginTop: '10px', padding: '8px 15px', backgroundColor: '#007bff', color: 'white', textDecoration: 'none', borderRadius: '5px' }}>
                    View Details
                  </a>
                </div>
              </div>
            ))
          ) : (
            !loading && !error && <p>Enter ingredients to find recipes!</p>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;