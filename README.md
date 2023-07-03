# PurposeGames-Hack

Javascript folder explanation:

The two programs located in the "JavaScript" folder are identical, except one is formatted as a bookmarklet. The program sends a post request containing false score data to trick the server into allowing you to have any score you desire. You can paste the "RequestBypass.js" program into the console or use the "Bookmarklet.js" program as a bookmarklet.

You can utilize these programs on https://www.purposegames.com.

Python folder explanation:

The "main.py" program utilizes requests to interact with purposegames.com in order to falsify scores. The program uses a myriad of different rules to appear human. The quizzes located in "quizzes.txt" were found with the program "Scraper.py." This program uses bs4 and requests to get information from the website, and threading to speed up to process. If you wish to use the program make sure to replace the cookies located in "PurposeGames.py" with your own.
