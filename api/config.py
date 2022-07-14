class BaseConfig:
    SECRET_KEY = "notasecretanymore"
    MONGO_DATABASE_URI = "mongodb://fab:baf@localhost:27017/"
    REDIS_DATABASE_URI = "redis://:baf@localhost:6379/0"
    DATABASE_NAME = "cooking"
    JWT_SECRET_KEY = "9ed0c3aabe1e1d6b54c8beb796f76f129e36af7a6cde42a8804b1611f5ff1fcb"
    JWT_ALGORITHM = "HS512"
    JWT_EXPIRES_IN_SECONDS = 60 * 60
    OTP_EXPIRES_IN_SECONDS = 60


class DockerizedConfig(BaseConfig):
    MONGO_DATABASE_URI = "mongodb://fab:baf@mongo:27017/"
    REDIS_DATABASE_URI = "redis://:baf@redis:6379/0"
