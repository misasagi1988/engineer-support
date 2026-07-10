from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate

# Valid state transitions: current_status -> [allowed_next_statuses]
VALID_TRANSITIONS = {
    "pending": ["processing"],
    "processing": ["resolved", "closed"],
    "resolved": ["closed"],
    "closed": [],
}


async def create_ticket(db: AsyncSession, data: TicketCreate) -> Ticket:
    ticket = Ticket(**data.model_dump())
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket

async def get_ticket(db: AsyncSession, ticket_id: str) -> Ticket | None:
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    return result.scalar_one_or_none()

async def list_tickets(db: AsyncSession, status: str | None = None, priority: str | None = None, assignee_id: str | None = None, module_id: str | None = None, skip: int = 0, limit: int = 20) -> list[Ticket]:
    query = select(Ticket)
    if status: query = query.where(Ticket.status == status)
    if priority: query = query.where(Ticket.priority == priority)
    if assignee_id: query = query.where(Ticket.assignee_id == assignee_id)
    if module_id: query = query.where(Ticket.module_id == module_id)
    query = query.offset(skip).limit(limit).order_by(Ticket.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())

async def update_ticket(db: AsyncSession, ticket: Ticket, data: TicketUpdate) -> Ticket:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(ticket, key, value)
    return ticket

async def resolve_ticket(db: AsyncSession, ticket: Ticket, solution: str) -> Ticket:
    ticket.status = "resolved"
    ticket.solution = solution
    ticket.resolved_at = datetime.now(timezone.utc)
    return ticket


def validate_status_transition(current_status: str, new_status: str) -> bool:
    """Check if a status transition is valid per the defined state machine."""
    allowed = VALID_TRANSITIONS.get(current_status, [])
    return new_status in allowed
