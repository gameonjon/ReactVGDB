import React, { useState } from "react";
import axios from 'axios';

import AddData from "./AddData.js";
import './App.css';


const NavBar = () =>{
    const [selectedOption, setSelectedOption] = useState('');
    const [response, setResponse] = useState('');   //response from API
    const [addData, setAddData] = useState(null);

    //handle option selected
    const handleOptionClick = (selectedOption) => {
        const option = selectedOption.target.value;
        setSelectedOption(option);
        makeApiCall(option);// make call 

        console.log({selectedOption});
    }

    const makeApiCall = (option) => {
        const API_URL = `http://localhost:8000/api/menu/${option}`;

        axios
            .get(API_URL)
            .then((res) => {
                setResponse(res.data);//set the API response data
            })
            .catch((err) => {
                console.error('Error: ', err);
            });
            
    };

    const handleDataClick = () => {
        setAddData(true);

    };

    const closePopup = () =>{
        setAddData(null);   //close popup
    }


    return (
        <nav>
            <div className="customSelect">
                Menu
                <ul className="dropDown">
                    <li className="dropDownItem" onClick={() =>{handleOptionClick("Games")}}>
                        Games
                    </li>
                    <li className="dropDownItem" onClick={() =>{handleOptionClick("Reviews")}}>
                        Reviews
                    </li>
                    <li className="dropDownItem double" onClick={() =>{handleOptionClick("PubsDevs")}}>
                        Publishers and Developers
                    </li>
                    <li className="dropDownItem" onClick={() =>{handleOptionClick("Platform")}}>
                        Platform
                    </li>

                </ul>
            </div>

            <p>{response}</p>
            

            <div className="customSelect" onClick={() => handleDataClick()}>
                Add Data
            </div>

            {addData && <AddData onClose={closePopup}/>}

        </nav>
    );
};
export default NavBar;