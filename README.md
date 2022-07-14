## 2FA authentification with FastAPI, mongoDB, Redis and OTP
## Author: Fabrizio Pensabene, 2022-07-11


# Instructions

1. Within the main folder execute ```docker compose up --build``` and wait for everything to be built and initialized

2. The SwaggerUI is then available at http://127.0.0.1:8000/docs to test the API

3. To run the unittest make sure you meet the requirements in your Python environment

   You can run these commands to install everything if needed:

   ```pip install --no-cache-dir -U pip setuptools wheel```

   ```pip install --no-cache-dir -r requirements```

   Then you can execute the tests from your shell by ```python tests.py``` and wait for the tests results to show

4. To execute the automated tests, from the main folder make sure the services are running by typing ```docker ps```

   If not, run again ```docker compose up --build``` from the main folder and leave the services a live

   Then, execute the automated test by typing ```python tests_automated.py``` from a new shell (active your env)

# UPDATES

   I restructered my project placeholder project (mainly databases.py and security.py)

   Removed my prefix_url as well as I had issues for redirects and did not like the URL

# NOTES

   I did not finished the project as I wanted to, the JWT/Session is not completed

   Wanted to implemented an OAuth2 to the project but it felt overkill and time consuming

   Had no time to implement a mail sender as well

   Did not refactor my code for the login/login2fa part when querying MongoDB
   for the email and password
