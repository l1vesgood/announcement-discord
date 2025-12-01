import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://user:password@postgres/db"
)


async def init_db():
    """Инициализация базы данных"""
    from services.database import Database

    db = Database()
    await db.init_db()
