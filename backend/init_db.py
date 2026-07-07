import asyncio

from app.db.database import Base, engine
from app.models.user import User
from app.services.auth_service import hash_password


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    from sqlalchemy import text

    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
        if count == 0:
            user_id = "admin-0000-0000-0000-000000000001"
            stmt = text(
                "INSERT INTO users (id, username, email, password_hash, role) "
                "VALUES (:id, :username, :email, :password_hash, :role)"
            )
            await conn.execute(
                stmt,
                {
                    "id": user_id,
                    "username": "admin",
                    "email": "admin@ops.local",
                    "password_hash": hash_password("admin123"),
                    "role": "admin",
                },
            )
            await conn.commit()
            print("Created default admin user (password: admin123)")


if __name__ == "__main__":
    asyncio.run(init_db())
