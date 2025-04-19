import './App.css';
import React, {useState} from 'react';
import Header from './Header.js';
import NavBar from './NavBar.js';
import Games from './Games.js';

const App = () => {
  const [gameList, setGameList] = useState([]); //lifted state

  return (
    <div id='body'>
      <Header/>
      
      <NavBar setGameList={setGameList}/>

      <div>
        {/* <gameItem/>    */}
        <Games gameList={gameList}/>

      </div>
      
      
    </div>
  );
}

export default App;
