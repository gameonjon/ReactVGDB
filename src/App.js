import './App.css';
import Header from './Header.js';
import NavBar from './NavBar.js';
import Games from './Games.js';

function App() {
  return (
    <body>
      <Header/>
      
      <NavBar/>

      <div>
        {/* <gameItem/>    */}
        <Games/>

      </div>
      
      
    </body>
  );
}

export default App;
