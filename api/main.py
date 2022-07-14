from api.databases.mongo import create_mongo_client
from api.databases.redis import create_redis_client


mongo_client = create_mongo_client()
redis_client = create_redis_client()

def serve_api():
    from fastapi import FastAPI
    from starlette.middleware.sessions import SessionMiddleware

    from api.config import BaseConfig
    from api.router import router as auth_router


    api = FastAPI()
    api.add_middleware(SessionMiddleware, secret_key=BaseConfig.SECRET_KEY)
    api.include_router(auth_router)

    return api
