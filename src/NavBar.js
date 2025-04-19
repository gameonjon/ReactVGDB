import React, { useState } from "react";
import axios from 'axios';

import AddData from "./AddData.js";
import './App.css';


const NavBar = ({setGameList}) =>{
    // const [selectedOption, setSelectedOption] = useState('');
    const [response, setResponse] = useState('');   //response from API
    const [addData, setAddData] = useState(null);

    //handle option selected
    // const handleOptionClick = (option) => {
    //     setSelectedOption(option);
    //     makeApiCall(option);// make call 

    //     console.log({option});
    // }

    const makeApiCall = (option) => {
        const API_URL = `http://localhost:5000/api/menu/${option}`;
        console.log('selected: ', option);
        console.log(API_URL);

        axios
            .get(API_URL)
            .then((res) => {
                setGameList(res.data);//set the API response data
                    //and update state in App.js
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
                    <li className="dropDownItem" onClick={() =>{makeApiCall("title_asc")}}>
                        Games (ASC)
                    </li>
                    {/* <li className="dropDownItem" onClick={() =>{handleOptionClick("Reviews")}}>
                        Reviews
                    </li>
                    <li className="dropDownItem double" onClick={() =>{handleOptionClick("PubsDevs")}}>
                        Publishers and Developers
                    </li>
                    <li className="dropDownItem" onClick={() =>{handleOptionClick("Platform")}}>
                        Platform
                    </li> */}
                    <li className="dropDownItem" onClick={() =>{makeApiCall("title_desc")}}>
                        Games (DES)
                    </li>

                </ul>
            </div>

            {/* <p>{response}</p> */}
            

            <div className="customSelect" onClick={() => handleDataClick()}>
                Add Data
            </div>

            {addData && <AddData onClose={closePopup}/>}

        </nav>
    );
};
export default NavBar;