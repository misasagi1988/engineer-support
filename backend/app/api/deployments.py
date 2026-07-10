from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.deployment import Deployment
from app.schemas.deployment import DeploymentCreate, DeploymentUpdate, DeploymentResponse

router = APIRouter(prefix="/deployments", tags=["deployments"])


@router.get("", response_model=list[DeploymentResponse])
async def list_deployments(
    customer_id: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Deployment).order_by(Deployment.name)
    if customer_id:
        query = query.where(Deployment.customer_id == customer_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("", response_model=DeploymentResponse, status_code=201)
async def create_deployment(data: DeploymentCreate, db: AsyncSession = Depends(get_db)):
    deployment = Deployment(**data.model_dump())
    db.add(deployment)
    await db.commit()
    await db.refresh(deployment)
    return deployment


@router.put("/{deployment_id}", response_model=DeploymentResponse)
async def update_deployment(deployment_id: str, data: DeploymentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Deployment).where(Deployment.id == deployment_id))
    deployment = result.scalar_one_or_none()
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(deployment, key, value)
    await db.commit()
    await db.refresh(deployment)
    return deployment
