# 🎮 Video game tracker
A web app that allows users to view, sort and manage a collection of video games. 
    #Features include:
    -ascending/descending sorting
    -cover image scraping 
    -popup detailed view
    -adding new games to database

## 🧰 Tech Stack
-Frontend: React, Axios, CSS
-Backend: Node.js, Express
-Database, MySQL
-Scraping: Python(IGDB API integration)


## 🧪To run loacally
# 1. Clone the repo
git clone https://github.com/yourusername/video-game-tracker.git

# 2. Install dependencies for backend and frontend
cd server
npm install

cd ../client
npm install

# 3. Run both servers (with concurrently or separate terminals)
npm run dev

# 4. Make sure you have a MySQL DB running and update your .env file accordingly
 

 ## 📦 Database Schema
Games table includes title, cover image path, release date, etc.

Supports multiple developers per game

One publisher per game

Related tables for developers, publishers, platforms

File can be viewed here in [Figma](https://www.figma.com/design/qi7Mlmhu8rHBzoiVC2bH3o/Untitled?node-id=9-40&t=DOhNCx8NkyjJiYrb-1)