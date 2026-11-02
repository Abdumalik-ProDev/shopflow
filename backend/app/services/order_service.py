"""Order business logic service."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.order import (
    OrderCreateRequest,
    OrderResponse,
    OrderStatusUpdateRequest,
)
from app.dtos.payment import PaymentCreateRequest, PaymentResponse
from app.dtos.review import ReviewCreateRequest, ReviewResponse
from app.mappers.mappers import order_to_dto, payment_to_dto, review_to_dto
from app.models.customer import Customer
from app.models.payment import Payment
from app.models.review import Review
from app.repositories.customer_repository import CustomerRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.review_repository import ReviewRepository


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(session)
        self.payment_repo = PaymentRepository(session)
        self.review_repo = ReviewRepository(session)
        self.customer_repo = CustomerRepository(session)

    async def create_order(self, req: OrderCreateRequest) -> OrderResponse:
        cust_uuid = None
        if req.customer_id:
            try:
                parsed = uuid.UUID(req.customer_id)
                existing = await self.customer_repo.get_by_id(parsed)
                if existing:
                    cust_uuid = existing.id
                else:
                    by_user = await self.customer_repo.get_by_user_id(parsed)
                    if by_user:
                        cust_uuid = by_user.id
                    else:
                        cust_uuid = parsed
            except ValueError:
                cust = await self.customer_repo.get_by_unique_id(req.customer_id)
                if cust:
                    cust_uuid = cust.id
                else:
                    new_cust = Customer(
                        customer_unique_id=req.customer_id,
                        customer_zip_code_prefix="00000",
                        customer_city="Marketplace",
                        customer_state="BR",
                    )
                    created_cust = await self.customer_repo.create(new_cust)
                    cust_uuid = created_cust.id

        if cust_uuid is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid customer identification for order creation",
            )

        items_payload = [it.model_dump() for it in req.items]
        order = await self.order_repo.create(
            customer_id=cust_uuid,
            items_data=items_payload,
            estimated_delivery_date=req.estimated_delivery_date,
        )
        return order_to_dto(order)

    async def get_order(self, order_id: uuid.UUID) -> OrderResponse:
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        return order_to_dto(order)

    async def list_orders(
        self,
        skip: int = 0,
        limit: int = 100,
        customer_id: str | None = None,
        status_filter: str | None = None,
    ) -> list[OrderResponse]:
        cust_uuid = None
        if customer_id:
            try:
                parsed = uuid.UUID(customer_id)
                existing = await self.customer_repo.get_by_id(parsed)
                if existing:
                    cust_uuid = existing.id
                else:
                    by_user = await self.customer_repo.get_by_user_id(parsed)
                    if by_user:
                        cust_uuid = by_user.id
                    else:
                        cust_uuid = parsed
            except ValueError:
                cust = await self.customer_repo.get_by_unique_id(customer_id)
                if cust:
                    cust_uuid = cust.id

        orders = await self.order_repo.list_orders(
            skip=skip, limit=limit, customer_id=cust_uuid, status=status_filter
        )
        return [order_to_dto(o) for o in orders]

    async def update_status(
        self, order_id: uuid.UUID, req: OrderStatusUpdateRequest
    ) -> OrderResponse:
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        updated = await self.order_repo.update_status(order, req.status)
        return order_to_dto(updated)

    async def create_payment(self, req: PaymentCreateRequest) -> PaymentResponse:
        pay = Payment(
            order_id=uuid.UUID(req.order_id),
            payment_sequential=req.payment_sequential,
            payment_type=req.payment_type,
            payment_installments=req.payment_installments,
            payment_value=req.payment_value,
        )
        created = await self.payment_repo.create(pay)
        return payment_to_dto(created)

    async def list_payments_by_order(self, order_id: uuid.UUID) -> list[PaymentResponse]:
        payments = await self.payment_repo.list_by_order(order_id)
        return [payment_to_dto(p) for p in payments]

    async def create_review(self, req: ReviewCreateRequest) -> ReviewResponse:
        rev = Review(
            order_id=uuid.UUID(req.order_id),
            review_score=req.review_score,
            comment_title=req.comment_title,
            comment_message=req.comment_message,
        )
        created = await self.review_repo.create(rev)
        return review_to_dto(created)

    async def list_reviews_by_order(self, order_id: uuid.UUID) -> list[ReviewResponse]:
        reviews = await self.review_repo.list_by_order(order_id)
        return [review_to_dto(r) for r in reviews]
