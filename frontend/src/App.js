import { useState } from 'react';
import './App.css';
import RecipeCard from './RecipeCard';

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

    const ingredientList = ingredients
      .split(',')
      .map(item => item.trim())
      .filter(item => item !== '');

    try {
      const response = await fetch(`${BACKEND_URL}/recipes/suggest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
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
    <div className="App" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header className="App-header" style={{
        padding: '15px',
        textAlign: 'center',
        backgroundColor: '#29742dff',
        borderBottom: '1px solid #ccc',
        color: 'white'
      }}>
        <h1 style={{ margin: '0', fontSize: '2em' }}>PantryChef</h1>
        <p style={{ margin: '0', fontSize: '1em' }}>Discover recipes based on what you have</p>
      </header>

      <main style={{
        padding: '20px',
        maxWidth: '1200px',
        margin: '0 auto',
        flex: 1
      }}>
        <form onSubmit={handleSubmit} style={{
          marginBottom: '30px',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          gap: '10px'
        }}>
          <input
            type="text"
            value={ingredientsInput}
            onChange={(e) => setIngredientsInput(e.target.value)}
            placeholder="Enter ingredients (e.g., chicken, rice, onions)"
            style={{
              width: 'clamp(200px, 70%, 500px)',
              padding: '14px',
              borderRadius: '8px',
              border: '1px solid #ccc',
              fontSize: '1em'
            }}
          />
          <button type="submit" style={{
            padding: '14px 24px',
            borderRadius: '8px',
            border: 'none',
            backgroundColor: '#4CAF50',
            color: 'white',
            cursor: 'pointer',
            fontSize: '1em',
            fontWeight: 'bold',
            boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
          }}>
            Find Recipes
          </button>
        </form>

        {loading && <p style={{ textAlign: 'center' }}>Loading recipes...</p>}
        {error && <p style={{ color: 'red', textAlign: 'center' }}>Error: {error}</p>}

        <div className="recipe-list">
          {recipes.length > 0 ? (
            recipes.map((recipe) => (
              <RecipeCard key={recipe.id} recipe={recipe} backendUrl={BACKEND_URL} />
            ))
          ) : (
            !loading && !error && <p style={{ textAlign: 'center' }}>Enter ingredients to find recipes</p>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;