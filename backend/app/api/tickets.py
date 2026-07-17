from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user_id
from app.db.session import get_db
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketStatusUpdate, TicketResponse
from app.services import ticket_service

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("", response_model=list[TicketResponse])
async def list_tickets(
    status: str | None = Query(None),
    priority: str | None = Query(None),
    assignee_id: str | None = Query(None),
    module_id: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    return await ticket_service.list_tickets(
        db, status=status, priority=priority, assignee_id=assignee_id, module_id=module_id, skip=skip, limit=limit
    )


@router.post("", response_model=TicketResponse, status_code=201)
async def create_ticket(data: TicketCreate, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    return await ticket_service.create_ticket(db, data)


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: str, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    ticket = await ticket_service.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: str, data: TicketUpdate, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    ticket = await ticket_service.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    await ticket_service.update_ticket(db, ticket, data)
    await db.commit()
    await db.refresh(ticket)
    return ticket


@router.put("/{ticket_id}/status", response_model=TicketResponse)
async def update_ticket_status(ticket_id: str, data: TicketStatusUpdate, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    ticket = await ticket_service.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if not ticket_service.validate_status_transition(ticket.status, data.status):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition: {ticket.status} -> {data.status}",
        )
    if data.status == "resolved":
        await ticket_service.resolve_ticket(db, ticket, data.solution or "")
    else:
        ticket.status = data.status
    await db.commit()
    await db.refresh(ticket)
    return ticket


@router.post("/{ticket_id}/generate-case")
async def generate_case(ticket_id: str, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    from app.services.recommendation_service import generate_case_draft
    from app.schemas.case import CaseCreate
    from app.services import case_service

    ticket = await ticket_service.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    draft = await generate_case_draft(db, ticket)
    case_data = CaseCreate(
        title=draft["title"],
        module_id=draft["module_id"],
        deploy_mode=draft.get("deploy_mode"),
        root_cause=draft["root_cause"],
        solution=draft["solution"],
        troubleshooting_path=draft.get("troubleshooting_path", []),
        tags=draft.get("tags", []),
        ticket_id=ticket.id,
        customer_id=ticket.customer_id,
    )
    case = await case_service.create_case(db, case_data, created_by=user_id)
    return case
