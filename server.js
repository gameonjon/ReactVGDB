import { hostname } from 'os';
import express from 'express';
import mysql from 'mysql2';
import cors from 'cors';
import Queries from './Queries.js';


const app = express();
const PORT = 5000;

//call to scrap img
import {spawn} from "child_process";

function runScraper(gameName){
    console.log(`running scraper for : ${gameName}`);

    return new Promise((resolve, reject) =>{
        const pythonProcess = spawn("python", ["./scraper.py", gameName]);

        pythonProcess.stdout.on("data", (data) =>{
            console.log(`Python Output: ${data}`);
        });

        pythonProcess.stderr.on("data", (data) =>{
            console.error(`Python Error: ${data}`);
        });

        pythonProcess.on("close", (code) =>{
            console.log(`Python process exited with code ${code}`);
            if(code === 0) resolve();
            else reject(new Error(`Scraper exited with code ${code}`));
        });
    });
    
    
}

app.use(cors());
app.use(express.json()); //middleware to parse JSON requests
    //Java Script Ojbect Notation
    //converts objects that would be undef. to readable JS

const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'Mysq1',
    database: "vgdb"
});

const queries = new Queries(db);

app.get('/api/games', (req,res) =>{
    db.query('SELECT * FROM Games', (err, results) =>{
        if(err) throw err;
        res.json(results);
    });
});

app.get('/api/menu/title_asc', async (req, res) =>{
    try{
        const games = await queries.getGameByTitleASC();
        res.json(games);
    } catch (error){
        console.error('Error fetching ascending titles:', error);
        res.status(500).json({ error: 'Internal Server Error'});
    }
});
app.get('/api/menu/title_desc', async (req, res) =>{
    try{
        const games = await queries.getGameByTitleDesc();
        res.json(games);
    } catch (error){
        console.error('Error fetching descending titles:', error);
        res.status(500).json({ error: 'Internal Server Error'});
    }
});

app.get('/api/pub', (req, res) =>{
    const gameId = req.query.gameId;
    const query = `SELECT Publisher.p_name 
        FROM Publisher, Games
        WHERE Publisher.p_pubkey = Games.g_pubkey
        AND Games.g_id = ?`;

    db.query(query, [gameId], (err, results) =>{
        if(err){
            console.error('Error fetching publsiher: ', err);
            res.status(500).json({ error: 'Failed to fetch publisher' });
        } else{
            res.json(results[0]);
        }
    });
});

app.get('/api/devs', (req, res) =>{
    const gameId = req.query.gameId; //get gameid for query parameters
    const query = `SELECT * FROM Developer
        JOIN Contracts on Developer.d_devkey = Contracts.c_devkey
        WHERE Contracts.c_gameID = ? `;

    db.query(query, [gameId], (err, results) =>{
        if (err) {
            console.error('Error fetching developers:', err);
            res.status(500).json({ error: 'Failed to fetch developers' });
        } else {
            res.json(results);
        }
    });
});

app.get('/api/platforms', (req, res) =>{
    const gameId = req.query.gameId;
    const query = `SELECT * FROM Platform
        JOIN GamePlatform on Platform.pf_id = GamePlatform.platform_id
        WHERE GamePlatform.game_id = ?`;

    db.query(query, [gameId], (err, results) =>{
        if(err){
            console.error('Error fetching Platforms: ', err);
            res.status(500).json({ error: 'Failed to fetch platforms' });
        } else{
            res.json(results);
        }
    });
});

//async/await are better for making execution sequential
//  and avoids errors like inserting related data before game exists
// Ensures each step is done before moving on (not needing 
// setTimeou() anymore)
//try/catch will stop execution if any operation fails and send an 
//  error message
app.post("/api/newGame/", async (req, res) =>{
    try {
        const errors = [];

        //required fields
        if (!req.body.GameTitle) errors.push("No Title entry");
        if (!req.body.ReleaseDate) errors.push("No year specified");
        if (!req.body.Genre) errors.push("No genre specified");
        if (!req.body.Publisher) errors.push("No publisher specified");
        if (!req.body.Developers || !req.body.Developers.length) errors.push("No Developers specified");
        if (!req.body.Platform || !req.body.Platform.length) errors.push("No Platform specified");

        if(errors.length){ 
            return res.status(400).json({error: errors.join(", ")});
        }

        //Extract game data
        const data = {
            gameTitle: req.body.GameTitle,
            year: req.body.ReleaseDate,
            genre: req.body.Genre,
            publisher: req.body.Publisher,
            developers: req.body.Developers,
            platforms: req.body.Platform
        };

        const gameName = data.gameTitle;


        //Insert game first
        const gameId = await queries.insertNewGame(data.gameTitle, data.year, data.genre);

        //insert publisher
        let publisherID;
        const [existingPub] = await queries.getPubByName(data.publisher);

        if(!existingPub){
            publisherID = await queries.insertPublisher(data.publisher);
        }else{
            publisherID = existingPub.p_pubkey;
        }
        
        await queries.updateGamePub(data.gameTitle, publisherID);


        //insert developers (handle multiple)
        for(const dev of data.developers){
            let devId; 
            const [existingDev] = await queries.getDevByName(dev);
            if(!existingDev){
                devId = await queries.insertDeveloper(dev);
            }else{
                devId = existingDev.d_devkey;
            }
            await queries.insertContract(gameId, devId);
        }

        //insert platforms (handle multiple)
        for(const plat of data.platforms){
            await queries.insertGamePlatform(gameId, plat);
        }

        //run scraper
        await runScraper(gameName); // await pauses until image is downloaded
        
 
        return res.json({
            message: "SUCCESS! Inserted new game",
            data: data
        });
    } catch (error) {
        console.error("Error adding new game: ", error);
        return res.status(500).json({error: "Failed to insert new game" });
    }
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));