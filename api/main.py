from api.databases import create_mongo_client, create_redis_client


mongo_client = create_mongo_client()
redis_client = create_redis_client()

def serve_api():
    from fastapi import FastAPI
    from auth.router import router as auth_router


    api = FastAPI()
    api.include_router(auth_router, prefix="/auth_router")
    return api
