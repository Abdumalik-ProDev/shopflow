"""Customers API controllers."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shopflow.core.database.session import get_session
from shopflow.modules.customers.api.schemas.customer import (
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerResponse,
)
from shopflow.modules.customers.application.use_cases.customer import (
    CreateCustomerUseCase,
    GetCustomerUseCase,
    UpdateCustomerUseCase,
    ListCustomersUseCase,
)
from shopflow.modules.customers.infrastructure.repositories import (
    SqlAlchemyCustomerRepository,
)

router = APIRouter(prefix="/customers", tags=["customers"])


def _repo(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyCustomerRepository(session)


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    payload: CustomerCreateRequest, repo=Depends(_repo), session: AsyncSession = Depends(get_session)
):
    use_case = CreateCustomerUseCase(repo)
    customer = await use_case.execute(payload)
    await session.commit()
    return CustomerResponse.model_validate(customer)


@router.get("", response_model=list[CustomerResponse])
async def list_customers(
    skip: int = 0, limit: int = 100, repo=Depends(_repo)
):
    use_case = ListCustomersUseCase(repo)
    return await use_case.execute(skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: str, repo=Depends(_repo)):
    use_case = GetCustomerUseCase(repo)
    customer = await use_case.execute(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerResponse.model_validate(customer)


@router.patch("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    payload: CustomerUpdateRequest,
    repo=Depends(_repo),
    session: AsyncSession = Depends(get_session),
):
    use_case = UpdateCustomerUseCase(repo)
    customer = await use_case.execute(customer_id, payload)
    await session.commit()
    return CustomerResponse.model_validate(customer)


__all__ = ["router"]
