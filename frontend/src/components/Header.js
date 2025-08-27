export default function Header() {
  return (
    <header style={{
      padding: '15px',
      textAlign: 'center',
      backgroundColor: '#d35400',
      borderBottom: '1px solid #ccc',
      color: 'white'
    }}>
      <h1 style={{ margin: '0', fontSize: '2em' }}>PantryChef</h1>
      <p style={{ margin: '0', fontSize: '1em' }}>Discover recipes based on what you have</p>
    </header>
  );
}