import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import load_and_prepare_data
from app.routes.get_network import get_network
from app.services.database import Database
from prisma import Prisma

app = FastAPI(
    title="MeloMind API",
    description="API for MeloMind",
    version="0.1.0",
)

app.include_router(load_and_prepare_data.router, tags=["Load Data"])

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
database: Database = Database()


# Prisma Client Dependency
async def get_prisma_client() -> Prisma:
    prisma = Prisma()
    await prisma.connect()
    try:
        yield prisma
    finally:
        await prisma.disconnect()


@app.get("/")
async def root():
    data = load_and_prepare_data.load_and_prepare_data()

    network_response = get_network(
        np.array(data['x_train']),
        np.array(data['y_train']),
        np.array(data['x_val']),
        np.array(data['y_val']),
        # np.array(data['x_test'])
    )
    print(network_response)
    return {"message": "Model trained and evaluated"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
