"""Make cases.ticket_id nullable for manual knowledge entry.

Usage:
    cd backend
    python -m app.db.migrations.make_case_ticket_id_nullable
"""
import asyncio
from sqlalchemy import text
from app.db.database import engine


async def run_migration():
    async with engine.begin() as conn:
        # Check current column nullability
        result = await conn.execute(text("""
            SELECT IS_NULLABLE
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'cases'
              AND COLUMN_NAME = 'ticket_id'
        """))
        row = result.fetchone()
        if row and row[0] == 'YES':
            print("  Column ticket_id is already nullable. Skipping.")
            return

        print("  Dropping foreign key constraint cases_ibfk_1...")
        await conn.execute(text(
            "ALTER TABLE cases DROP FOREIGN KEY cases_ibfk_1"
        ))

        print("  Modifying cases.ticket_id to allow NULL...")
        await conn.execute(text(
            "ALTER TABLE cases MODIFY COLUMN ticket_id VARCHAR(36) NULL"
        ))

        print("  Re-adding foreign key constraint with ON DELETE SET NULL...")
        await conn.execute(text(
            "ALTER TABLE cases ADD CONSTRAINT cases_ibfk_1 "
            "FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE SET NULL"
        ))
        print("  Done. ticket_id is now nullable.")


if __name__ == "__main__":
    asyncio.run(run_migration())
