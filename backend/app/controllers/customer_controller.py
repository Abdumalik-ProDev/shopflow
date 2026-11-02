"""Customer controller router."""

from fastapi import APIRouter, Query, status

from app.controllers.deps import OptionalUserDep, SessionDep
from app.dtos.customer import CustomerCreateRequest, CustomerResponse, CustomerUpdateRequest
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    payload: CustomerCreateRequest,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> CustomerResponse:
    service = CustomerService(session)
    customer_dto = await service.create_customer(payload)
    await session.commit()
    return customer_dto


@router.get("", response_model=list[CustomerResponse])
async def list_customers(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: OptionalUserDep = None,
) -> list[CustomerResponse]:
    service = CustomerService(session)
    return await service.list_customers(skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: str,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> CustomerResponse:
    service = CustomerService(session)
    return await service.get_customer(customer_id)


@router.patch("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    payload: CustomerUpdateRequest,
    session: SessionDep,
    current_user: OptionalUserDep = None,
) -> CustomerResponse:
    service = CustomerService(session)
    updated = await service.update_customer(customer_id, payload)
    await session.commit()
    return updated
