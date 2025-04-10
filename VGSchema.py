import mysql.connector
from getpass import getpass
from mysql.connector import Error

def dropTables(cur, conn):
    print("++++++++++++++++++++++++++++++++++")
    print("dropping tables")
    try: 
        sql = "DROP TABLE IF EXISTS Media"
        cur.execute(sql)

        sql = "DROP TABLE IF EXISTS GamePlatform"
        cur.execute(sql)

        sql = "DROP TABLE IF EXISTS Contracts"
        cur.execute(sql)

        sql = "DROP TABLE IF EXISTS Games"
        cur.execute(sql)

        sql = "DROP TABLE IF EXISTS GamePlay"
        cur.execute(sql)

        sql = "DROP TABLE IF EXISTS Reviews"
        cur.execute(sql)

        sql = "DROP TABLE IF EXISTS Platform"
        cur.execute(sql)

        sql = "DROP TABLE IF EXISTS Developer"
        cur.execute(sql)

        sql = "DROP TABLE IF EXISTS Publisher"
        cur.execute(sql)

        conn.commit()
        print("success")
    
    except Error as e:
        cur.rollback()
        print(e)
    
    print("+++++++++++++++++++++++++++++++++++++++")


def createTables(cur, conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Creating tables")

    try:
        #foreign key: creates a link between two tables referencing primrary 
            #key of another table
        #on delete cascade: maintains referential integrity between linked 
            # tables by deleting  rows in a child table when related parent 
            # table is deleted.
        #USE IF NOT EXISTS to avoid data loss on creating new tables
        sql = """CREATE TABLE IF NOT EXISTS Publisher(
                    p_pubkey INTEGER PRIMARY KEY AUTO_INCREMENT,
                    p_name VARCHAR(80) UNIQUE NOT NULL
                )"""
        cur.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS Developer(
                    d_devkey INTEGER PRIMARY KEY AUTO_INCREMENT,
                    d_name VARCHAR(80) UNIQUE NOT NULL
                )"""
        cur.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS Platform(
                    pf_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    pf_system varchar(25) NOT NULL
                )"""
        cur.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS Reviews (
                    r_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    r_rating DECIMAL(3, 1) NOT NULL,
                    r_resource VARCHAR(50) NOT NULL,
                    r_comment VARCHAR(1250)
                )"""
        cur.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS GamePlay(
                    gp_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    gp_url VARCHAR(125) NOT NULL,
                    gp_platform VARCHAR(45)
                )"""
        cur.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS Games(
                    g_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    g_title varchar(80) UNIQUE NOT NULL,
                    g_year DATE NOT NULL,
                    g_genre VARCHAR(55) DEFAULT NULL,
                    g_pubkey INTEGER,
                    FOREIGN KEY (g_pubkey) REFERENCES Publisher(p_pubkey) ON DELETE SET NULL
                )"""
        cur.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS Contracts(
                    c_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    c_gameID INTEGER,
                    c_devkey INTEGER,
                    FOREIGN KEY (c_gameID) REFERENCES Games(g_id) ON DELETE CASCADE,
                    FOREIGN KEY (c_devkey) REFERENCES Developer(d_devkey) ON DELETE CASCADE
                )"""
        cur.execute(sql)


        sql = """CREATE TABLE IF NOT EXISTS GamePlatform(
                    gpf_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    game_id INTEGER,
                    platform_id INTEGER,
                    FOREIGN KEY (game_id) REFERENCES Games(g_id) ON DELETE CASCADE,
                    FOREIGN KEY (platform_id) REFERENCES Platform(pf_id) ON DELETE CASCADE
                )"""
        cur.execute(sql)


        sql = """CREATE TABLE IF NOT EXISTS Media(
                    m_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    image_url VARCHAR(255),
                    game_id INTEGER,
                    review_id INTEGER,
                    gameplay_id INTEGER,
                    FOREIGN KEY (game_id) REFERENCES Games(g_id) ON DELETE CASCADE,
                    FOREIGN KEY (review_id) REFERENCES Reviews(r_id) ON DELETE CASCADE,
                    FOREIGN KEY (gameplay_id) REFERENCES GamePlay(gp_id) ON DELETE CASCADE 
                )"""
        cur.execute(sql)

        conn.commit()
        print("success")


    except Error as e:
        cur.rollback()
        print(e)
    
    print("++++++++++++++++++++++++++++")

def populateParentTables(cur, conn):
    print("++++++++++++++++++++++++++++++++++")
    print("populating Parent tables...")

    try:
        pubs = [
            ("Square Enix", 10001),
            ("Feral Interactive", 10002),
            ("Xbox Game Studios", 10003),
            ("Electronic Arts", 10004),
            ("Sony Interactive Entertainment", 10005),
            ("505 Games", 10006), 
            ("Blizzard Entertainment", 10007), 
            ("2K Games", 10008),
            ("Take-Two Interactive", 10009),
            ("Techland", 10010),
            ("Warner Bros. Interactive Entertainment", 10011),
            ("Activision", 10012),
            ("Ubisoft", 10013),
            ("Gameloft", 10014),
            ("Aspyr", 10015),
            ("Frontier Groove, Inc.", 10016),
            ("Sony Interactive Entertainment Europe", 10017)

        ]
        pubDict = [
            {
                "p_name": pub[0],
                "p_pubkey": pub[1]
            }
            for pub in pubs
        ]
        
        sql = """INSERT INTO Publisher Values(%(p_pubkey)s, %(p_name)s)"""
        cur.executemany(sql, pubDict)

        devs = [
            ("Crystal Dynamics", 20001),
            ("Eidos-Montreal", 20002),
            ("Feral Interactive", 20003),
            ("Cameron Suey", 20004),
            ("Respawn Entertainment", 20005),
            ("DICE", 20006),
            ("Motive Studios", 20007),
            ("Criterion Software", 20008),
            ("Kojima Productions", 20009),
            ("Blizzard Entertainment", 20010),
            ("Iron Galaxy", 20011),
            ("Irrational Games", 20012),
            ("2K Marin", 20013),
            ("2K Australia", 20014),
            ("Blind Squirrel Games", 20015),
            ("Digital Extremes", 20016),
            ("Techland", 20017),
            ("Infinity Ward", 20018),
            ("Raven Software", 20019),
            ("Beenox", 20020),
            ("Ubisoft", 20021),
            ("Ubisoft Paris", 20022),
            ("Red Storm Entertainment", 20023),
            ("Guerrilla Games", 20024),
            ("Naughty Dog", 20025), 
            ("Electronic Arts", 20026),
            ("Insomniac Games", 20027),
            ("Sledgehammer Games", 20028),
            ("DICE Los Angeles", 20029),
            ("Ubisoft Milan", 20030),
            ("Ubisoft Romania", 20031),
            ("Gameloft", 20032),
            ("Ubisoft Reflections", 20033),
            ("Ubisoft Shanghai", 20034),
            ("Ubisoft Montpellier", 20035),
            ("Ubisoft Annecy", 20036),
            ("Grin", 20037),
            ("Ubisoft Singapore", 20038),
            ("Ubisoft Ukraine", 20039),
            ("Virtuos", 20040),
            ("Next Level Games", 20041),
            ("High Voltage Software", 20042),
            ("Ubisoft Sofia", 20043),
            ("Loot Drop", 20044),
            ("Darkworks", 20045),
            ("Ubisoft Belgrade", 20046),
            ("Ubisoft Barcelona", 20047),
            ("i5works", 20048),
            ("EA Gothenburg", 20049)
        ]
        devDict = [
            {
                "d_name": dev[0],
                "d_devkey": dev[1]
            }
            for dev in devs
        ]
        sql = """INSERT INTO Developer Values(%(d_devkey)s, %(d_name)s)"""
        cur.executemany(sql, devDict)

        plats = [ #platform(id, system)
            (1, "Playstation"),
            (2, "Xbox"),
            (3, "PC"),
            (4, "Nintendo")
        ]
        sql = """INSERT INTO Platform(pf_id, pf_system) VALUES(%s, %s)"""
        cur.executemany(sql, plats)

        reviews = [ #Revews(gameID, rating, resource, comment)
                    #Reviews(r_id, r_rating, r_resource, r_comment)
            #12, 
            (10, "IGN", "With The Last of Us: Remastered, PlayStation 3's best game just became PlayStation 4's, too."),
            #12, 
            (9, "Metro GameCentral", "Still a stunning achievement in both storytelling and third person adventure, and although this is the definitive version the differences are still minor."),
            #12, 
            (10, "Game Informer", "The punishing world dares you to press on, and the story is an emotional punch to the gut. In short, this is one of the best video games ever made"),
            #18, 
            (8, "IGN", "Call of Duty: Modern Warfare's varied gameplay modes and excellent gunplay suggest the series is headed in a promising direction."),
            #18, 
            (8, "GamesRadar+", "Modern Warfare is fast and frenetic, setting a new benchmark for fidelity and high-pressure FPS action."),
            #17, 
            (8.7, "IGN", "I wanted Marvel's Spider-Man on PS4 to make me feel like Spider-Man: To sail between the highrises of New York City, to nimbly web up hordes of enemies, and tussle with familiar, animal-themed villains. Insomniac Games' first foray into the world of Marvel handily delivers on all of that. But what I didn't expect from Spider-Man was to come away feeling just as fulfilled to have inhabited the life of Peter Parker. Aside from a few odd pacing issues, which momentarily took me out of the experience of being a superhero, and a world of optional missions that don't always quite live up to the heft of the main story, Insomniac has delivered a Spider-Man story that both surprised and delighted me, coupled with gameplay that made me feel like Spider-Man nearly every step of the way. The Wall Crawler's open world doesn't consistently deliver the thrilling moments of its main campaign, but the foundation laid here is undoubtedly a spectacular one."),
            #4, 
            (8.5, "PC Gamer", "Slow, weird, and indulgent, but a true original, and a journey that will linger in your mind long after it's over."),
            #4, 
            (7, "GamesRadar+", "Kojima's mysterious would be epic has its moments but can't carry the weight of expectation."),
            #5, 
            (8.8, "PC Gamer", "It's not flawless, but Overwatch is still one of the best new multiplayer shooters to arrive in years."),
            #5, 
            (10, "IGN", "Overwatch is a masterpiece. A dizzying amalgam of unique characters, stunning style, and compellingly dynamic action."),
            #6, 
            (8, "Game Revolution", "If you are a PS4 or Xbox One owner, Bioshock: The Collection should be in your, um, collection, whether in the 2-disc physical format or digital download. Unfortunately, I’ve read reports that the PC version has issues. (Like bad ones.) As such PC players should wait for the (fingers crossed) eventual patches."),
            #6, 
            (9, "Hobby Consolas", "Three great adventures masterfully ported to Nintendo Switch. They only missing feature is they're not running at 60 fps, but the rest is on spot, showing an adaptation on par with the PS4 and Xbox One remasters. Also, keep in mind that if you buy it, physical or digital, you will need a big microSD, because the download is quite big..."),
            #6, 
            (8, "Metro GameCentral", "Time has worn some holes in each games’ reputation, but these are still three of the most ambitious and daring action games of modern times."),
            #8, 
            (8.4, "PC Gamer", "Although familiar to BF3, but BF4 remains a visually and sonically satisfying, reliably intense FPS. Improved by Commander Mode and a terrific and diverse map set."),
            #8, 
            (9, "GamesRadar+", "Multiplayer shooters don't get better than Battlefield 4. Incredible destruction, smart map design, and solid tech combine to produce a true showcase for PS4 and PC. While solo play still lags behind, it's a big step up from BF3."),
            #2, 
            (9, "Easy Allies", "NULL"),
            #2, 
            (9, "IGN", "Star Wars Jedi: Fallen Order makes up for a lot of lost time with a fantastic single-player action-adventure that marks the return of the playable Jedi."),
            #2, 
            (7.3, "PC Gamer", "Technical issues marr an otherwise slick adventure. A must for Star Wars fans."),
            #14, 
            (9, "GamesRadar+", "An open-world that tailors to each and every interest, Horizon: Zero Dawn keeps combat fresh, with an intriguing protagonist to match."),
            #14, 
            (8.6, "PC Gamer", "A classy sandbox that stands out from the pack thanks to its brilliant battles against an array of fantastic beasts."),
            #14, 
            (9.3, "IGN", "Horizon Zero Dawn presents us with a beautiful world full of unforgettable challenges.")
        ]
        revDict = [
            {
                "rating": rev[0],
                "resource": rev[1],
                "comment": rev[2]
            }
            for rev in reviews
        ]
        sql = """
            INSERT INTO Reviews(r_rating, r_resource, r_comment)
            Values(%(rating)s, %(resource)s, %(comment)s)
            """
        cur.executemany(sql, revDict)

        
        gamePlay = [#(gp_id, gp_url, gp_platform)
            #18, 
            ("https://www.twitch.tv/directory/game/Call%20Of%20Duty%3A%20Modern%20Warfare", "Twitch"),
            #18, 
            ("https://www.youtube.com/results?search_query=call+of+duty+modern+warfare", "Youtube"),
            #5, 
            ("https://www.twitch.tv/directory/game/Overwatch", "Twitch"),
            #5, 
            ("https://www.youtube.com/results?search_query=overwatch", "Youtube"),
            #12, 
            ("https://www.twitch.tv/directory/game/The%20Last%20of%20Us", "Twitch"),
            #12, 
            ("https://www.youtube.com/results?search_query=the+last+of+us+remastered", "Youtube"),
            #6,
            ("https://www.twitch.tv/directory/game/BioShock%3A%20The%20Collection", "Twitch"),
            #6, 
            ("https://www.youtube.com/results?search_query=bioshock+the+collection", "Youtube"),
            #2, 
            ("https://www.youtube.com/results?search_query=star+wars+jedi+fallen+order", "Youtube"),
            #2,
            ("https://www.twitch.tv/directory/game/Horizon%20Zero%20Dawn", "Twitch"),
            #8,
            ("https://www.youtube.com/results?search_query=battlefield+4", "Youtube")
        ]
        playDict = [
            {
                "url": gp[0],
                "platform": gp[1]
            }
            for gp in gamePlay
        ]
        sql = """
            INSERT INTO GamePlay(gp_url, gp_platform)
            Values(%(url)s, %(platform)s)
            """
        
        cur.executemany(sql, playDict)
        

        conn.commit()
        print("success")

    except Error as e:
        cur.rollback()
        print(e)
        
    print("++++++++++++++++++++++++++++")

def populateChildTables(cur, conn):
    print("++++++++++++++++++++++++++++++++++")
    print("populating child tables...")

    try:
        games = [               #(title, year, genre, gameID, pubkey) # devkey)

            #Platform:
            # ps4, xbox1, xbox360, MSW, Mac OS, Linux
            ("Rise of the Tomb Raider", '2016-02-09', "action-adventure", 1, 10001),# 20001),
            #Platform: ps4, xbox1, MSW
            ("Star Wars Jedi: Fallen Order",'2019-11-15', "action-adventure", 2, 10004),# 20005),
            #Platform: ps4, xbox1, MSW
            ("Star Wars: BattleFront 2", '2017-11-17', "shooter", 3, 10004), #, 20006),
            #Platform: ps4, MSW
            ("Death Stranding", '2019-11-08', "action", 4, 10006), # , 20009),
            #Platform: ps4, nintendo, xbox 1, msw
            ("Overwatch", "2016-05-24", "shooter", 5, 10007), #, 20010),
            #Platform: ps4, xbox1, msw, nintendo
            ("Bioshock: The Collection", '2016-09-13', "shooter", 6, 10008), #, 20012),
            #Platform: ps4, xbox1, msw, linux, classic Mac os
            ("Dying Light", '2015-01-26', "action", 7, 10010), # , 20017), 
            #Platform: ps4, xbox1, ps3, xbox360, msw
            ("Battlefield 4", '2013-10-29', "shooter", 8, 10004), # , 20006),
            #Platform: ps4, xbox1, msw
            ("Call of Duty: Modern Warfare Remastered", '2016-11-04', "shooter", 9, 10012), #, 20018),
            #Platform: ps4, xbox1, msw
            ("Tom Clancy's Ghost Recon: Wildlands", '2017-03-07', "tactical shooter", 10, 10013), #, 20021),
            #Platform: ps4 
            ("Killzone Shadow Fall", '2013-11-15', "shooter", 11, 10005), # , 20024),
            #Platform: ps4
            ("The Last of Us Remastered", '2014-07-29', "survival-horror", 12, 10005), #, 20025),
            #Platform: ps4, msw, xbox1
            ("Star Wars: Battlefront", '2015-11-16', "shooter", 13, 10004), #, 20006),
            #Platform: ps4, msw
            ("Horizon Zero Dawn", '2017-02-28', "action", 14, 10005), #, 20024),
            #Platform: ps4, xbox1, msw
            ("Battlefield 1", '2016-10-21', "shooter", 15, 10004), #, 20006),
            #Platform: ps4, xbox1, msw
            ("Need for Speed", '2015-11-03', "racing", 16, 10004), # , 20026),
            #Platform: ps4
            ("Marvel's Spider-Man", '2018-09-07', "action-adventure", 17, 10005), #, 20027),
            #Platform: ps4, xbox1, msw
            ("Call of Duty: Modern Warfare", '2019-08-23', "shooter", 18, 10012), #, 20018)
        ]
        games_dict = [
            {
                "g_title": game[0],
                "g_year": game[1],
                "g_genre": game[2],
                "g_id": game[3],
                "g_pubkey": game[4]
            }
            for game in games
        ]
        sql = """
            INSERT INTO Games (g_title, g_year, g_genre, g_id, g_pubkey)
            VALUES(%(g_title)s, %(g_year)s, %(g_genre)s, %(g_id)s, %(g_pubkey)s)
            """
        cur.executemany(sql, games_dict)
        
        conn.commit()
        print("success")

    except Error as e:
        cur.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def populateJoinTables(cur, conn):
    print("+++++++++++++++++++++++++++++++++")
    print("populating Joins table")
    
    try:
        contracts = [ # contracts(c_id, c_gameid, c_devkey)
            #rise of the tomb raider
            (1, 20001),
            (1, 20002),
            (1, 20003),
            (1, 20004),
            #Star  wars jedi fallen order
            (2, 20005),
            #star wars : battlefront 2
            (3, 20006),
            (3, 20007),
            (3, 20008),
            #death stranding
            (4, 20009),
            (4, None),
            #overwatch
            (5, 20010),
            (5, 20011),
            #bioshock the collection
            (6, 20012),
            (6, 20013),
            (6, 20014),
            (6, 20015),
            (6, 20016),
            #dying light
            (7, 20017),
            (7, None),
            #battlefield 4
            (8, 20006),
            (8, 20029),
            #COD mw remastered
            (9, 20018),
            (9, 20019),
            (9, 20020),
            #tom clancy ghost recon
            (10, 20021),
            (10, 20022),
            (10, 20023),
            (10, 20030),
            (10, 20031),
            (10, 20032),
            (10, 20033),
            (10, 20034),
            (10, 20035),
            (10, 20036),
            (10, 20037),
            (10, 20038),
            (10, 20039),
            (10, 20040),
            (10, 20041),
            (10, 20042),
            (10, 20043),
            (10, 20044),
            (10, 20045),
            (10, 20046),
            (10, 20047),
            (10, 20048),
            #killzone shadow fall
            (11, 20024),
            #TLOU Remastered
            (12, 20025),
            #star wars battlefront
            (13, 20006),
            (13, 20008),
            #horizon zero dawn
            (14, 20024),
            #Battlefield 1
            (15, 20006),
            #need for speed
            (16, 20049),
            #spider man
            (17, 20027),
            (17, None),
            #cod MW 2019
            (18, 20018),
            (18, 20028)
        ]

        conDict = [ #c_id will automatically input
            {
                "c_gameID": contract[0],
                "c_devkey": contract[1]
            }
            for contract in contracts
        ]

        sql = """
            INSERT INTO Contracts(c_gameID, c_devkey)
            VALUES(%(c_gameID)s, %(c_devkey)s)
            """
        cur.executemany(sql, conDict)

        gamePlatform = [ #(gpf_id, game_id, platform_id)
            # 11, 1
            (1, 1),
            (1, 2),
            (1, 3),
            # 11, 2
            (2, 1),
            (2, 2),
            (2, 3),
            # 11, 3
            (3, 1),
            (3, 2),
            (3, 3),
            # 5, 4
            (4, 1),
            (4, 3),
            # 13, 5
            (5, 1),
            (5, 3),
            (5, 4),
            # 13, 6
            (6, 1),
            (6, 3),
            (6, 4),
            # 11, 7
            (7, 1),
            (7, 2),
            (7, 3),
            # 11, 8
            (8, 1),
            (8, 2),
            (8, 3),
            # 11, 9
            (9, 1),
            (9, 2),
            (9, 3),
            # 11, 10
            (10, 1),
            (10, 2),
            (10, 3),
            # 1, 11
            (11, 1),
            # 1, 12
            (12, 1),
            # 11, 13
            (13, 1),
            (13, 2), 
            (13, 3),
            # 5, 14
            (14, 1),
            (14, 3),
            # 11, 15
            (15, 1),
            (15, 2),
            (15, 3),
            # 11, 16
            (16, 1),
            (16, 2),
            (16, 3),
            # 1, 17
            (17, 1),
            # 11, 18
            (18, 1),
            (18, 2),
            (18, 3)
        ]

        gpfDict = [
            {
                "game_id": gpf[0], 
                "platform_id": gpf[1]
            }
            for gpf in gamePlatform
        ]

        sql = """
            INSERT INTO GamePlatform(game_id, platform_id)
            VALUES(%(game_id)s, %(platform_id)s)
        """
        cur.executemany(sql, gpfDict)


        media = [ # (m_id, game_id, review_id, gameplay_id)
            (12, 1, 5), 
            (12, 2, 6),
            (12, 3, None),
            (18, 4, 1),
            (18, 5, 2),
            (17, 6, None),
            (4, 7, None),
            (4, 8, None), 
            (5, 9, 3),
            (5, 10, 4),
            (6, 11, 7),
            (6, 12, 8),
            (6, 13, None),
            (8, 14, None),
            (8, 15, 11),
            (2, 16, 9),
            (2, 17, 10),
            (2, 18, None),
            (14, 19, None),
            (14, 20, None),
            (14, 21, None)
        ]
        mediaDict = [
            {
                "gameid": medi[0],
                "reviewid": medi[1],
                "gameplayid": medi[2]
            }
            for medi in media
        ]
        sql = """
            INSERT INTO Media(game_id, review_id, gameplay_id)
            VALUES (%(gameid)s, %(reviewid)s, %(gameplayid)s)
            """
        cur.executemany(sql, mediaDict)

        conn.commit()
        print("success")

    except Error as e: 
        cur.rollback()
        print(e)
    
    print("+++++++++++++++++++++++++++++++++++++")

def main():


    # password = getpass("Enter MySQL password: ")

    #connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Mysq1",
        database="vgdb" 
    )
    #cursor object to interact with db
    cursor = conn.cursor()


    #execute a query
    # cursor.execute("CREATE DATABASE IF NOT EXISTS vgdb")
    # print('Creating db...')

    # Create tables 
    with cursor:
        dropTables(cursor, conn)
        createTables(cursor, conn)
        populateParentTables(cursor, conn)
        populateChildTables(cursor, conn)
        populateJoinTables(cursor, conn)
        



    #close connection
    cursor.close()
    conn.close()


# if __name__ == '__main__':
#     main()
main()

