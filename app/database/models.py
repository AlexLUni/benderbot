from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    rank: Mapped[str] = mapped_column(String(24))
    tg_id = mapped_column(BigInteger)


class File(Base):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(primary_key=True)
    file_id = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(64))
    category: Mapped[str] = mapped_column(String(40))


class TemporaryMessage(Base):       # имеющие дату
    __tablename__ = 'temporary_messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    admin_id = mapped_column(BigInteger, ForeignKey('admins.id'))
    chat_id = mapped_column(BigInteger)
    message_id = mapped_column(String(64))
    date: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(64))
    category: Mapped[str] = mapped_column(String(40))


class ConstantMessage(Base):        # без даты
    __tablename__ = 'constant_messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    admin_id = mapped_column(BigInteger, ForeignKey('admins.id'))
    chat_id = mapped_column(BigInteger)
    message_id = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(64))
    category: Mapped[str] = mapped_column(String(40))


class Event(Base):        # регулярные встречи, мероприятия
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    admin_id = mapped_column(BigInteger, ForeignKey('admins.id'))
    name: Mapped[str] = mapped_column(String(64))
    city: Mapped[str] = mapped_column(String(40))
    address: Mapped[str] = mapped_column(String(64))
    time: Mapped[str] = mapped_column(String(64))
    day_schedule: Mapped[str] = mapped_column(String(64))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

