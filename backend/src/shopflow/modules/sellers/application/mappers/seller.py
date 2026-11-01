"""Sellers mappers."""

from shopflow.modules.sellers.application.dtos.seller import SellerCreate, SellerOut, SellerUpdate
from shopflow.modules.sellers.domain.models.seller import Seller


def domain_to_dto(s: Seller) -> SellerOut:
    return SellerOut(
        id=str(s.id), seller_zip_code_prefix=s.seller_zip_code_prefix,
        seller_city=s.seller_city, seller_state=s.seller_state, user_id=s.user_id,
    )


def dto_to_domain(dto: SellerCreate) -> Seller:
    return Seller(
        seller_zip_code_prefix=dto.seller_zip_code_prefix,
        seller_city=dto.seller_city, seller_state=dto.seller_state,
    )


def update_domain_from_dto(s: Seller, dto: SellerUpdate) -> None:
    for field, value in dto.model_dump(exclude_unset=True).items():
        setattr(s, field, value)
    s.touch()


__all__ = ["domain_to_dto", "dto_to_domain", "update_domain_from_dto"]
