"""Mappers for converting between SQLAlchemy models and Pydantic DTOs."""

from app.dtos.auth import UserResponse
from app.dtos.category import CategoryResponse
from app.dtos.customer import CustomerResponse
from app.dtos.order import OrderItemResponse, OrderResponse
from app.dtos.payment import PaymentResponse
from app.dtos.product import ProductResponse
from app.dtos.review import ReviewResponse
from app.dtos.seller import SellerResponse
from app.models.category import Category
from app.models.customer import Customer
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.product import Product
from app.models.review import Review
from app.models.seller import Seller
from app.models.user import User


def user_to_dto(user: User) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        role=user.role,
        created_at=user.created_at,
    )


def category_to_dto(category: Category) -> CategoryResponse:
    return CategoryResponse(
        id=str(category.id),
        name=category.name,
        name_english=category.name_english,
    )


def product_to_dto(product: Product) -> ProductResponse:
    return ProductResponse(
        id=str(product.id),
        sku=product.sku,
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity,
        category_id=str(product.category_id) if product.category_id else None,
        seller_id=str(product.seller_id) if product.seller_id else None,
        is_active=product.is_active,
        weight_g=product.weight_g,
        length_cm=product.length_cm,
        height_cm=product.height_cm,
        width_cm=product.width_cm,
        photos_qty=product.photos_qty,
    )


def customer_to_dto(customer: Customer) -> CustomerResponse:
    return CustomerResponse(
        id=str(customer.id),
        customer_unique_id=customer.customer_unique_id,
        customer_zip_code_prefix=customer.customer_zip_code_prefix,
        customer_city=customer.customer_city,
        customer_state=customer.customer_state,
        user_id=str(customer.user_id) if customer.user_id else None,
    )


def seller_to_dto(seller: Seller) -> SellerResponse:
    return SellerResponse(
        id=str(seller.id),
        seller_zip_code_prefix=seller.seller_zip_code_prefix,
        seller_city=seller.seller_city,
        seller_state=seller.seller_state,
        user_id=str(seller.user_id) if seller.user_id else None,
    )


def order_item_to_dto(item: OrderItem) -> OrderItemResponse:
    return OrderItemResponse(
        id=str(item.id),
        order_id=str(item.order_id),
        product_id=item.product_id,
        seller_id=item.seller_id,
        price=item.price,
        freight_value=item.freight_value,
        quantity=item.quantity,
    )


def order_to_dto(order: Order) -> OrderResponse:
    items_dtos = [order_item_to_dto(it) for it in order.items] if order.items else []
    return OrderResponse(
        id=str(order.id),
        customer_id=str(order.customer_id),
        status=order.status,
        purchase_timestamp=order.purchase_timestamp,
        approved_at=order.approved_at,
        delivered_carrier_date=order.delivered_carrier_date,
        delivered_customer_date=order.delivered_customer_date,
        estimated_delivery_date=order.estimated_delivery_date,
        total=order.total,
        items=items_dtos,
    )


def payment_to_dto(payment: Payment) -> PaymentResponse:
    return PaymentResponse(
        id=str(payment.id),
        order_id=str(payment.order_id),
        payment_sequential=payment.payment_sequential,
        payment_type=payment.payment_type,
        payment_installments=payment.payment_installments,
        payment_value=payment.payment_value,
        created_at=payment.created_at,
    )


def review_to_dto(review: Review) -> ReviewResponse:
    return ReviewResponse(
        id=str(review.id),
        order_id=str(review.order_id),
        review_score=review.review_score,
        comment_title=review.comment_title,
        comment_message=review.comment_message,
        created_at=review.created_at,
    )
