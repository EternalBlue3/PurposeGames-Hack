# PurposeGames-Hack

Javascript folder explanation:

The two programs located in the "JavaScript" folder are identical, except one is formatted as a bookmarklet. The program sends a post request containing false score data to trick the server into allowing you to have any score you desire. You can paste the "RequestBypass.js" program into the console or use the "Bookmarklet.js" program as a bookmarklet.

You can utilize these programs on https://www.purposegames.com.

Python folder explanation:

The "main.py" program utilizes requests to interact with purposegames.com in order to falsify scores. By using bs4 for web scraping, it can automatically find quizzes and calculates reasonable scores. Then it submits the manipulated scores in a human-looking manner. The delay is set to sixty seconds because that is roughly how long the PurposeGames backend takes to update the "Gameplay Details" page under a player's stats. The program requires two libraries: bs4 and requests.
