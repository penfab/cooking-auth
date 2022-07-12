class BaseConfig:
    MONGO_DATABASE_URI = "mongodb://fab:baf@localhost:27017/"
    REDIS_DATABASE_URI = "redis://:baf@localhost:6379/0"
    DATABASE_NAME = "cooking"
    OTP_EXPIRES_IN_180_SECONDS = 180
    JWT_ALGORITHM = "HS512"
    JWT_EXPIRES_IN_480_MINUTES = 480


class DockerizedConfig(BaseConfig):
    MONGO_DATABASE_URI = "mongodb://fab:baf@mongo:27017/"
    REDIS_DATABASE_URI = "redis://:baf@redis:6379/0"
