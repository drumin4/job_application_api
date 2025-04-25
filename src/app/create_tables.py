import asyncio
from app.database import engine
from app.models import Base

async def init_db():
    try:
        async with engine.begin() as conn:
            print("📦 Creating database tables...")
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Tables created successfully!")
    except Exception as e:
        print("❌ Error creating tables:", e)

if __name__ == "__main__":
    asyncio.run(init_db())
