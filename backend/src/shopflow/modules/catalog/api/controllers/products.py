"""Catalog API controllers."""

from fastapi import APIRouter, Depends, HTTPException, status

from shopflow.core.database.session import get_session
from shopflow.modules.catalog.infrastructure.repositories import SqlAlchemyProductRepository

router = APIRouter(prefix="/products", tags=["catalog"])


@router.get("")
async def list_products(session=Depends(get_session)):
    repo = SqlAlchemyProductRepository(session)
    products = await repo.list()
    return products


__all__ = ["router"]
