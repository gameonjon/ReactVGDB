import React, {useEffect, useState} from "react";
import axios from 'axios';
import './App.css';;

const AddData = ({onClose}) =>{

    const [formData, setFormData] = useState({
        GameTitle: "",
        Genre: "",
        ReleaseDate: "",
        Publisher: "",
        Developers: [""], //array for multiple developers
        Platform: []
    }, []);


    //adds a CSS class (popup-open) to the <body> element.
    //to disable scrolling (or apply styles) to the page when a popup/modal is open.
    useEffect(() =>{
        document.body.classList.add("popup-open")
        return() =>{
            document.body.classList.remove("popup-open")
        }
    })

    // ... is the spread operator in JavaScript. 
    // used to create shallow copy of an object or array 
    // so that we can modify it without affecting the original state.
    const handleInputChange = (e) =>{
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleDeveloperChange = (index, value) =>{
        const updatedDevelopers = [...formData.Developers];
        updatedDevelopers[index] = value;
        setFormData({ ...formData, Developers: updatedDevelopers});
    };

    //e is changing the target, like value and checked. 
    //in ...prevstate we keep everything the same and only change the value
    const handlePlatformChange = (e) =>{
        const {value, checked} = e.target;
        setFormData((prevState) => ({
            ...prevState,
            Platform: checked
                ? [...prevState.Platform, value]
                : prevState.Platform.filter((platform) => platform !== value),
        }));
    };
    
    //keep all previous data, keep previous developer, and add new dev ""
    const addDeveloperField = () => {
        setFormData({ ...formData, Developers: [...formData.Developers, ""] });
    };

    //.filter keeps all the wanted developers and 
    //removes the developer at chosen index
    const removeDeveloperField = (index) => {
        const updatedDevelopers = formData.Developers.filter((_, i) => i !== index);
        setFormData({ ...formData, Developers:updatedDevelopers});
    };

    const handleSubmit = (e) =>{
        e.preventDefault(); //prevents default page refresh on submit
        axios
            .post("http://localhost:5000/api/newGame/", formData)
            .then((response) => {
                console.log("Game Add Successful", response.data);
                onClose(); // after game added
                window.location.reload();//refresh after changes
            })
            .catch((error) => {
                console.error("Error adding game: ", error);
            });
    };


    return(
        <div className="dataPop" onClick={(e) => e.stopPropagation()}>
            <div className="dataCont" onClick={(e) => e.stopPropagation()}>
                <form onSubmit={handleSubmit}>
                    <button className="closePop" type="button" onClick={onClose}>
                        X
                    </button>
                    Game Title: <br/>
                    <input type="text" placeholder="GameTitle" name="GameTitle" value={formData.GameTitle} onChange={handleInputChange} required/><br/>
                    Release Date:<br/>
                    <input type="date" placeholder="ReleaseDate" name="ReleaseDate" onChange={(e) => setFormData({...formData, ReleaseDate: e.target.value})} required/><br/>
                    Genre: <br/>
                    <input type="text" placeholder="Genre" name="Genre" value={formData.Genre} onChange={handleInputChange} required/><br/>
                    Publisher: <br/>
                    <input type="text" placeholder="Publisher" name="Publisher" value={formData.Publisher} onChange={handleInputChange} required/><br/>
                    {/* Developer: <input type="text" placeholder="Developer" name="Developer"/><br/> */}
                    Developer(s): <br/>
                    {formData.Developers.map((developer, index) => (
                        <div key={index}>
                            <input type="text" value={developer} placeholder="Developer"
                                onChange={(e) => handleDeveloperChange(index, e.target.value)}
                            required/>

                            <button type="button" onClick={() => removeDeveloperField(index)}>
                                Remove
                            </button>
                        </div>
                    ))}
                    <button type="button" onClick={addDeveloperField}>
                        Add Developer
                    </button><br/>

                    platform(s):<br/>
                    <label><input type="checkbox" onChange={handlePlatformChange} value="PC"/> PC</label><br/>
                    <label><input type="checkbox" onChange={handlePlatformChange} value="Playstation"/> Playstation</label><br/>
                    <label><input type="checkbox" onChange={handlePlatformChange} value="Xbox"/> Xbox</label><br/>
                    <label><input type="checkbox" onChange={handlePlatformChange} value="Nintendo"/> Nintendo</label><br/>

                    <button type="submit" id="btn">Execute</button>
                </form>
            </div>
        </div>

    )
};

export default AddData;