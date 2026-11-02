"""Customer business logic service."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.customer import CustomerCreateRequest, CustomerResponse
from app.mappers.mappers import customer_to_dto
from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository


class CustomerService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.customer_repo = CustomerRepository(session)

    async def create_customer(self, req: CustomerCreateRequest) -> CustomerResponse:
        existing = await self.customer_repo.get_by_unique_id(req.customer_unique_id)
        if existing:
            return customer_to_dto(existing)
        cust = Customer(
            customer_unique_id=req.customer_unique_id,
            customer_zip_code_prefix=req.customer_zip_code_prefix,
            customer_city=req.customer_city,
            customer_state=req.customer_state,
            user_id=uuid.UUID(req.user_id) if req.user_id else None,
        )
        created = await self.customer_repo.create(cust)
        return customer_to_dto(created)

    async def get_customer(self, customer_id: uuid.UUID) -> CustomerResponse:
        cust = await self.customer_repo.get_by_id(customer_id)
        if not cust:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )
        return customer_to_dto(cust)

    async def list_customers(self, skip: int = 0, limit: int = 100) -> list[CustomerResponse]:
        customers = await self.customer_repo.list_all(skip=skip, limit=limit)
        return [customer_to_dto(c) for c in customers]
