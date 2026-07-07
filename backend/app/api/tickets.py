from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketStatusUpdate, TicketResponse
from app.services import ticket_service

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("/", response_model=list[TicketResponse])
async def list_tickets(
    status: str | None = Query(None),
    priority: str | None = Query(None),
    assignee_id: str | None = Query(None),
    module_id: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    return await ticket_service.list_tickets(
        db, status=status, priority=priority, assignee_id=assignee_id, module_id=module_id, skip=skip, limit=limit
    )


@router.post("/", response_model=TicketResponse, status_code=201)
async def create_ticket(data: TicketCreate, db: AsyncSession = Depends(get_db)):
    return await ticket_service.create_ticket(db, data)


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: str, db: AsyncSession = Depends(get_db)):
    ticket = await ticket_service.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: str, data: TicketUpdate, db: AsyncSession = Depends(get_db)):
    ticket = await ticket_service.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    await ticket_service.update_ticket(db, ticket, data)
    await db.commit()
    await db.refresh(ticket)
    return ticket


@router.put("/{ticket_id}/status", response_model=TicketResponse)
async def update_ticket_status(ticket_id: str, data: TicketStatusUpdate, db: AsyncSession = Depends(get_db)):
    ticket = await ticket_service.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if data.status == "resolved":
        await ticket_service.resolve_ticket(db, ticket, solution="")
    else:
        ticket.status = data.status
    await db.commit()
    await db.refresh(ticket)
    return ticket
