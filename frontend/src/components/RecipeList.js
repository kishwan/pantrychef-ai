import RecipeCard from "./RecipeCard";

export default function RecipeList({ recipes }) {
  if (!recipes.length) {
    return <p style={{ textAlign: 'center' }}>Enter ingredients to find recipes</p>;
  }

  return (
    <div className="recipe-list">
      {recipes.map((recipe) => (
        <RecipeCard key={recipe.id} recipe={recipe} />
      ))}
    </div>
  );
}