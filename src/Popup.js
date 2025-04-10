import React, {useState, useEffect} from "react";
import axios from 'axios';

import './App.css';

const Popup = ({game, onClose}) => {
    const [devs, setDevs] = useState([]);
    const [rating, setRating] = useState([]);
    const [platforms, setPlatforms] = useState([]);
    const [pub, setPub] = useState({});

    const imageName = game.g_title.replace(/[\s:]+/g, "_")+".jpg";
    const imagePath = `/images/${imageName}`;

    useEffect(() => {
        //prevent background scrolling when open
        document.body.classList.add("popup-open");
        return () =>{
            //re-enable background scrolling when closed
            document.body.classList.remove("popup-open");
        };
    }, []);

    useEffect(() => {
        if(!game) return;

        const fetchDevs = axios.get(`http://localhost:5000/api/devs?gameId=${game.g_id}`);
        const fetchPlatforms = axios.get(`http://localhost:5000/api/platforms?gameId=${game.g_id}`);
        const fetchPub = axios.get(`http://localhost:5000/api/pub?gameId=${game.g_id}`);
        // const fetchMedia = axios.get(`http://localhost:500/api/media?gameId=${game.g_id}`);

        //fetch developers
        Promise.all([fetchDevs, fetchPlatforms, fetchPub])
            .then(([devsResponse, platResponse, pubResponse]) =>{
                setDevs(devsResponse.data);
                setPlatforms(platResponse.data);
                setPub(pubResponse.data);
                // console.log(pubResponse.data);
                // console.log(platResponse.data);
                
            })
            .catch((error) => {
                console.error("error fetching game data", error);
                
            });
    }, [game]); //trigger effect whenever the selected game changes

    if(!game){
        return null;
    }
    
    return(
        <div className="popOverlay" onClick={onClose}>
            <div className="popContent" onClick={(e) => e.stopPropagation()}>
                <button className="closePop" onClick={onClose}>
                    X
                </button>

                <div>
                    <h1>{game.g_title}</h1>

                    <h3>Publisher</h3>
                    <p>{pub.p_name}</p>

                    <h3>Release Year: </h3>
                    <p>{new Date(game.g_year).getFullYear()}</p>

                    <h3>Genre: </h3>
                    <p>{game.g_genre}</p>

                    <h3>Platforms:</h3>
                    <ul>
                        {platforms.map((plat) => (
                            <li key={plat.pf_id}>{plat.pf_system}</li>
                        ))}
                    </ul>

                    <h3>Developers: </h3>
                    <ul>
                        {devs.map((dev) => (
                            <li key={dev.d_devkey}>{dev.d_name}</li>
                        ))}
                    </ul>

                </div>

                <img src={imagePath}
                className="img" 
                alt={imageName} 
                onError={(e) => e.target.src = "/default.jpg"} 
                />      


                
            </div>
            
        </div>
    )
};

export default Popup;