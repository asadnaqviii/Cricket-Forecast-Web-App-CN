# Cricket-Forecast-Web-App-CN

This is a part of my Computer Network assignment in 6th semester of BS-Computer Science degree. I have created a web server which uses web scraping to fetch live cricket scorecard data from Cricbuzz website. The user will be able to enter URL of the live game and predict score of current batsman from the list of players in the dropdown menu. Once this is submitted, Users can make a prediction and other users can vote on that prediction as thumbs up, dn or ridiculous. Person with max dn vote but get their prediction right will win.

Here's a summary of the technologies used:
1. Flask: A lightweight Python web framework that handles HTTP requests and responses, as well as URL routing. It serves as the backend of our application.
2. HTML, CSS, and JavaScript: The core building blocks of the frontend, responsible for rendering the user interface and handling user interactions.
3. Bootstrap: A popular CSS framework that simplifies the process of designing responsive and visually appealing web pages.
4. jQuery: A widely-used JavaScript library that simplifies DOM manipulation, event handling, and AJAX requests.
5. BeautifulSoup: A Python library used for web scraping purposes. In this project, it's utilized to extract live cricket match data from an external website.
6. SQLite: A lightweight, serverless, self-contained SQL database engine used to store prediction data locally.
7. Firebase: (Will integrate it in future)
