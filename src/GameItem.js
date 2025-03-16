import React from "react";
import './App.css';

const GameItem = ({game, onClick}) =>{

    return(
        <div className="game-item" onClick={onClick}>
            <h1>{game.g_title}</h1>
            <p>Release Year: {new Date(game.g_year).getFullYear()}</p>
            <p>Genre: {game.g_genre}</p>
    
        </div>

    )

};

export default GameItem;