from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prisma import Prisma

from app.models.kaggle_dataset import load_songs_from_csv, DatasetSong
from app.routes import auth, spotify
from app.services.database import Database

app = FastAPI(
    title="MeloMind API",
    description="API for MeloMind",
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(spotify.router)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
songs: list[DatasetSong] = load_songs_from_csv('sorted_songs_no_lyrics.csv', 100)

database: Database = Database()


# Prisma Client Dependency
async def get_prisma_client() -> Prisma:
    prisma = Prisma()
    await prisma.connect()
    try:
        yield prisma
    finally:
        await prisma.disconnect()


@app.get("/load_and_get_songs")
async def load_and_get_songs():
    global songs
    return songs


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
