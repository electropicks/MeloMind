from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth

app = FastAPI(
    title="MeloMind API",
    description="API for MeloMind",
    version="0.1.0",
)

app.include_router(auth.router)
origins = [
    "localhost:8000",
    "melomind.vercel.app",
    "localhost:8000/*",
    "melomind.vercel.app/*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
