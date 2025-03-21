from fastapi import FastAPI
from app.auth import routes as auth_routes
from app.user import routes as user_routes
from app.database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root():
    return {"message": "Server is running"}


app.include_router(auth_routes.router)
app.include_router(user_routes.router)
