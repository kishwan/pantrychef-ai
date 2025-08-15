import { useState } from "react";
import config from "./config";
import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import RecipeList from "./components/RecipeList";

export default function App() {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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
      const response = await fetch(`${config.BACKEND_URL}/recipes/suggest`, {
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

  return (
    <div className="App" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header />
      <main style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto', flex: 1 }}>
        <SearchBar onSearch={fetchRecipes} />
        {loading && <p style={{ textAlign: 'center' }}>Loading recipes...</p>}
        {error && <p style={{ color: 'red', textAlign: 'center' }}>Error: {error}</p>}
        <RecipeList recipes={recipes} />
      </main>
    </div>
  );
}