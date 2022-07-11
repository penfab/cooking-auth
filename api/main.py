from fastapi import FastAPI


def serve_api():
    from auth.router import router as auth_router


    api = FastAPI()
    api.include_router(auth_router, prefix="/auth_router")

    return api
