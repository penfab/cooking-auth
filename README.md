## 2FA authentification with FastAPI, mongoDB, Redis and OTP
## Author: Fabrizio Pensabene, 2022-07-11

## Updates
1. changes in user.py -> new fields + email validator
2. added security.py -> custom managers PasswordManager, OTPManager and JWTManager
3. added config.py for constants and new requirements
4. added tests.py for unittest
5. added MongoDB and Redis databases
6. added methods to interact with MongoDB and Redis instances
7. added mongo-express and RedisInsight to interact with MongoDB/Redis

## TODO's

1. remove all JSONResponse from my previous placeholder template
2. implement OAuth2 with OTP and JWT -> OAuth2PasswordRequestForm
3. added a login method to not repeat the loginc and make the code more readable
4. if I have time, add smtplib to send emails with OTP's
