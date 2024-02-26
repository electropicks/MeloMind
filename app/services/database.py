import json

from prisma import Prisma


class Database:
    def __init__(self):
        self.db = Prisma()

    async def connect(self):
        await self.db.connect()

    async def disconnect(self):
        await self.db.disconnect()


# Asynchronous context manager for database connection
async def get_db():
    database = Database()
    await database.connect()
    try:
        yield database
    finally:
        await database.disconnect()
