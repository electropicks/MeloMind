import asyncio

from prisma import Prisma


class Database:
    def __init__(self):
        self.db = Prisma()

    async def connect(self):
        await self.db.connect()

    async def disconnect(self):
        await self.db.disconnect()

    # Example query method
    async def example_query(self):
        # Your query logic here
        pass


# Global database instance
database = Database()


# Asynchronous context manager for database connection
async def get_db():
    await database.connect()
    try:
        yield database
    finally:
        await database.disconnect()


# Main function for testing
async def main():
    async with get_db() as db:
        # Example usage of database within context manager
        await db.example_query()


if __name__ == '__main__':
    asyncio.run(main())
