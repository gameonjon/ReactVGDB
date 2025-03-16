class Queries {
    constructor(db){
        this.db = db; // database connection
    }

    insertNewGame(title, year, genre){
        return new Promise((resolve, reject) => {
            this.db.execute(
                `INSERT INTO Games(g_title, g_year, g_genre)
                    VALUES (?, ?, ?)`,
                [title, year, genre],
                (err, result) =>{
                    if(err) reject(err);
                    else resolve(result.insertId); //return new game's ID
                }
            );
        });
    }
    getPubByName(name){
        return new Promise((resolve, reject) =>{
            this.db.execute(
                `SELECT * FROM Publisher
                    WHERE p_name = (?)`,
                [name],
                (err, result) =>{
                    if(err) reject(err);
                    else resolve(result);
                }
            );
        });
    }

    getDevByName(dev){
        return new Promise((resolve, reject) =>{
            this.db.execute(
                `SELECT * FROM Developer
                    WHERE d_name = (?)`,
                [dev],
                (err, result) =>{
                    if(err) reject(err);
                    else resolve(result);
                }
            );
        });
    }

    insertPublisher(publisher){
        return new Promise((resolve, reject) =>{
            this.db.execute(
                `INSERT INTO Publisher(p_name)
                    VALUES (?)`,
                [publisher],
                (err, result) =>{
                    if(err) reject(err);
                    else resolve(result.insertId); //return new pub ID
                }
            );
        });
    }

    insertDeveloper(developer){
        return new Promise((resolve, reject) =>{
            this.db.execute(
                `INSERT INTO Developer(d_name)
                    VALUES(?)`,
                [developer],
                (err, result) =>{
                    if(err) reject(err);
                    else resolve(result.insertId); //return new dev ID
                }
            );
        });
    }

    insertContract(gameId, devId){
        return new Promise((resolve, reject) =>{
            this.db.execute(
                `INSERT INTO Contracts(c_gameID, c_devkey)
                    VALUES(?, ?)`,
                [gameId, devId],
                (err, result) =>{
                    if(err) reject(err);
                    else resolve(result);
                }
            );
        });
    }

    insertGamePlatform(gameId, plat){
        return new Promise((resolve, reject) =>{
            this.db.execute(
                `INSERT INTO GamePlatform(game_id, platform_id)
                    SELECT ?, pf_id
                        FROM Platform
                        WHERE pf_system = ? `,
                [gameId, plat],
                (err, result) =>{
                    if(err) reject(err);
                    else resolve(result.insertId);
                }
            );
        });
    }

    updateGamePub(gameTitle, pubId){
        return new Promise((resolve, reject) =>{
            this.db.execute(
                `UPDATE Games
                    SET g_pubkey = ?
                    WHERE g_title = ?`,
                [pubId, gameTitle],
                (err, result) =>{
                    if(err) reject(err);
                    else resolve(result);
                }
            );
        });
    }


    

}

export default Queries;
