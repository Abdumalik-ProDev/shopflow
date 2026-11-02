"""Customer controller router."""

import uuid

from fastapi import APIRouter, Query, status

from app.controllers.deps import CurrentUserDep, SessionDep
from app.dtos.customer import CustomerCreateRequest, CustomerResponse
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    payload: CustomerCreateRequest,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> CustomerResponse:
    service = CustomerService(session)
    customer_dto = await service.create_customer(payload)
    await session.commit()
    return customer_dto


@router.get("", response_model=list[CustomerResponse])
async def list_customers(
    session: SessionDep,
    current_user: CurrentUserDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[CustomerResponse]:
    service = CustomerService(session)
    return await service.list_customers(skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> CustomerResponse:
    service = CustomerService(session)
    return await service.get_customer(customer_id)
