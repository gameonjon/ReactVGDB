import React from "react";
import './App.css';

const GameItem = ({game, onClick}) =>{
    const imageName = game.g_title.replace(/[\s:]+/g, "_") + ".jpg";
//     \s → Matches any whitespace (space, tab, newline).
    // : → Specifically matches colons.
    // + → Ensures multiple spaces or colons are replaced with a single underscore.
    // g → Global flag, ensuring all occurrences are replaced.
    const imagePath = `/images/${imageName}`; //even in public, dont need /public/images
    // console.log(imageName, imagePath);

    return(
        <div className="game-item" onClick={onClick}>
            <div className="game-info">
                <h1>{game.g_title}</h1>
                <p>Release Year: {new Date(game.g_year).getFullYear()}</p>
                <p>Genre: {game.g_genre}</p>
            </div>
            <img src={imagePath}
                className="img" 
                alt={imageName} 
                onError={(e) => e.target.src = "/default.jpg"} 
            />
        
        </div>

    )

};

export default GameItem;