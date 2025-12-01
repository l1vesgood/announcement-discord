from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, BigInteger, select
from settings import DATABASE_URL

Base = declarative_base()


class Mute(Base):
    __tablename__ = "mutes"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True, nullable=False)


class Database:
    def __init__(self):
        self.engine = create_async_engine(DATABASE_URL, echo=False)
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def is_muted(self, user_id: int) -> bool:
        async with self.async_session() as session:
            result = await session.execute(select(Mute).where(Mute.user_id == user_id))
            return result.scalar_one_or_none() is not None

    async def get_all_muted(self) -> list:
        """Get list of all muted user IDs"""
        async with self.async_session() as session:
            result = await session.execute(select(Mute.user_id))
            return [row[0] for row in result.all()]

    async def mute_user(self, user_id: int):
        async with self.async_session() as session:
            result = await session.execute(select(Mute).where(Mute.user_id == user_id))
            if result.scalar_one_or_none():
                return

            new_mute = Mute(user_id=user_id)
            session.add(new_mute)
            await session.commit()

    async def unmute_user(self, user_id: int):
        async with self.async_session() as session:
            result = await session.execute(select(Mute).where(Mute.user_id == user_id))
            mute_entry = result.scalar_one_or_none()
            if mute_entry:
                await session.delete(mute_entry)
                await session.commit()
