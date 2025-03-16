import React, {useState, useEffect} from "react";
import axios from 'axios';

import GameItem from './GameItem.js';
import Popup from "./Popup.js";
import './App.css';


const Games = () =>{

    const [games, setGames] = useState([]);
    const [loading, setLoading] = useState(true); //handle loading
    const [selectedGame, setSelectedGame] = useState(null); // state for pop up 

    useEffect(() => {
        //fetch data
        axios
            .get("http://localhost:5000/api/games") 
            .then((response) =>{
                setGames(response.data);  
                // console.log(response.data);
                setLoading(false);

            })
            .catch((error) =>{
                console.error("Error fetching game data", error);
                setLoading(false);
            });
    }, []); //empty dependency array means this runs once

    if(loading) {
        return <p>Loading...</p>;
    }

    const handleGameClick = (game) =>{
        setSelectedGame(game); //set selected game, open popup
        console.log(game);
    };

    const closePopup = () =>{
        setSelectedGame(null); // close pop up
    }

    return (
        <div>
            <div className="gameList">
                {games.map((game) =>(
                    <GameItem key={game.g_id} game={game} onClick={() => handleGameClick(game)}/>
                ))}
            </div>

            {/* pop-up */}
            {selectedGame && <Popup game={selectedGame} onClose={() => closePopup()}/>}
        </div>
    );

};

export default Games;