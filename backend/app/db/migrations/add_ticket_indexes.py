"""Add indexes to tickets table for query performance.

Usage:
    cd backend
    python -m app.db.migrations.add_ticket_indexes
"""
import asyncio
from sqlalchemy import text
from app.db.database import engine


INDEXES = [
    ("idx_tickets_status", "tickets", "status"),
    ("idx_tickets_priority", "tickets", "priority"),
    ("idx_tickets_assignee_id", "tickets", "assignee_id"),
    ("idx_tickets_module_id", "tickets", "module_id"),
    ("idx_tickets_created_at", "tickets", "created_at"),
]


async def run_migration():
    async with engine.begin() as conn:
        # Check existing indexes
        result = await conn.execute(text(
            "SHOW INDEX FROM tickets"
        ))
        existing = {row[2] for row in result}  # index name is column 3 (0-based index 2)

        for idx_name, table, column in INDEXES:
            if idx_name in existing:
                print(f"  SKIP {idx_name} (already exists)")
                continue
            sql = text(f"CREATE INDEX {idx_name} ON {table} ({column})")
            print(f"  Creating index {idx_name} on {table}({column})...")
            await conn.execute(sql)
        print("Done. All indexes created/verified.")


if __name__ == "__main__":
    asyncio.run(run_migration())
