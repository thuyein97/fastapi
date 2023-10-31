from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .databasetest import engine
from .routers import post, user, auth, vote
# from config import settings


# model.Base.metadata.create_all(bind=engine)
origins = ["https://www.google.com", "https://www.youtube.com"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello World, FUCK YOU BITCHES"}
