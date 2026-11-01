"""Customers API controllers."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.customers.api.schemas.customer import (
    CustomerCreateRequest, CustomerUpdateRequest, CustomerResponse,
)
from shopflow.modules.customers.application.services.customer import CustomerService
from shopflow.modules.customers.infrastructure.repositories import SqlAlchemyCustomerRepository

router = APIRouter(prefix="/customers", tags=["customers"])


def _service(session: AsyncSession = Depends(get_session)) -> CustomerService:
    return CustomerService(SqlAlchemyCustomerRepository(session))


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(payload: CustomerCreateRequest, svc: CustomerService = Depends(_service), session: AsyncSession = Depends(get_session)):
    c = await svc.create(payload)
    await session.commit()
    return CustomerResponse.model_validate(c)


@router.get("", response_model=list[CustomerResponse])
async def list_customers(skip: int = 0, limit: int = 100, svc: CustomerService = Depends(_service)):
    return await svc.list(skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: str, svc: CustomerService = Depends(_service)):
    c = await svc.get_by_id(customer_id)
    if c is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerResponse.model_validate(c)


@router.patch("/{customer_id}", response_model=CustomerResponse)
async def update_customer(customer_id: str, payload: CustomerUpdateRequest, svc: CustomerService = Depends(_service), session: AsyncSession = Depends(get_session)):
    c = await svc.update(customer_id, payload)
    await session.commit()
    return CustomerResponse.model_validate(c)


__all__ = ["router"]
