import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [input, setInput] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    onSearch(input);
  };

  return (
    <form onSubmit={handleSubmit} style={{
      marginBottom: '30px',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      gap: '10px'
    }}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
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
  );
}