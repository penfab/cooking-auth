## 2FA authentification with FastAPI, MongoDB, Redis and OTP
## Author: Fabrizio Pensabene, 2022-07-11


# Instructions

1. Within the main folder execute ```docker compose up --build``` and wait for everything to be built and initialized

2. The SwaggerUI is then available at http://127.0.0.1:8000/docs to test the API manually

3. To run the unittest make sure you meet the requirements in your Python environment

   You can run these commands to install everything if needed (you might for step 4.):

   ```pip install --no-cache-dir -U pip setuptools wheel```

   ```pip install --no-cache-dir -r requirements```

   Then you can execute the tests from your shell by ```python tests.py``` and wait for the tests results to show

4. To execute the automated tests, from the main folder make sure the services are still running by typing ```docker ps```

   If not, run again ```docker compose up --build``` from the main folder and leave the services running

   Then, execute the automated test by typing ```python tests_automated.py``` from a new shell (activate your env, you might need to do step 3.)

5. A web interface (mongo-express) to interact with MongoDB collections is available at: http://127.0.0.1:8081

   username/password are fab/baf to log in
   
6. Another web interface (RedisInsight) is available at: http://127.0.0.1:8001 to interact with Redis
   
   To log in, select "Connect to a Redis Database" (first option)
   
   Fill the form as follow: ```redis``` for the Host, ```6379``` for the Port, ```0``` for the Name and ```baf``` as the Password

# UPDATES

   I restructured my previous placeholder project mainly fpr databases.py and security.py

   Removed my prefix_url as well as I had issues for redirects and did not like the base URL

# NOTES

   I did not finished the project as I wanted to, the JWT/Session is not completed

   Wanted to implemented an OAuth2 to the project but it felt overkill and time consuming

   Had no time to implement a mail sender as well

   Did not refactor my code for the login/login2fa part when querying MongoDB for the email and password
   
   There is no sanitizing in my automated tests. You will have to delete the user collection manually to run some of them again
