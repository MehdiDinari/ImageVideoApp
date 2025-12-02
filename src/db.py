# src/db.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# URL de connexion (nécessite: uv add aiosqlite)
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Classe de base pour tes modèles SQL
class Base(DeclarativeBase):
    pass


# Ton modèle de base de données (Table "posts")
class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]


# Fonction pour créer les tables au démarrage
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Dépendance pour récupérer la session
async def get_async_session():
    async with async_session_maker() as session:
        yield session