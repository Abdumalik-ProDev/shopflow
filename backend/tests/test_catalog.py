"""Catalog and product endpoints tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_category_and_product_crud(client: AsyncClient, auth_headers: dict[str, str]):
    # 1. Create Category
    cat_res = await client.post(
        "/api/products/categories",
        json={"name": "electronics", "name_english": "Electronics"},
        headers=auth_headers,
    )
    assert cat_res.status_code == 201
    cat_data = cat_res.json()
    assert cat_data["name"] == "electronics"
    category_id = cat_data["id"]

    # 2. List Categories
    cat_list = await client.get("/api/products/categories")
    assert cat_list.status_code == 200
    assert len(cat_list.json()) >= 1

    # 3. Create Product
    prod_res = await client.post(
        "/api/products",
        json={
            "sku": "SKU-HEADPHONES-001",
            "name": "Wireless Headphones",
            "description": "Noise cancelling headphones",
            "price": 149.99,
            "stock_quantity": 50,
            "category_id": category_id,
            "is_active": True,
        },
        headers=auth_headers,
    )
    assert prod_res.status_code == 201
    prod_data = prod_res.json()
    assert prod_data["sku"] == "SKU-HEADPHONES-001"
    assert prod_data["price"] == 149.99
    assert prod_data["stock_quantity"] == 50
    prod_id = prod_data["id"]

    # 4. Get Product by ID
    get_res = await client.get(f"/api/products/{prod_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Wireless Headphones"

    # 5. Update Product
    update_res = await client.patch(
        f"/api/products/{prod_id}",
        json={"price": 129.99, "name": "Wireless ANC Headphones"},
        headers=auth_headers,
    )
    assert update_res.status_code == 200
    assert update_res.json()["price"] == 129.99
    assert update_res.json()["name"] == "Wireless ANC Headphones"

    # 6. Adjust Stock via query param
    stock_res = await client.post(
        f"/api/products/{prod_id}/stock?delta=-5",
        headers=auth_headers,
    )
    assert stock_res.status_code == 200
    assert stock_res.json()["stock_quantity"] == 45

    # 7. Adjust Stock via JSON body
    stock_body_res = await client.post(
        f"/api/products/{prod_id}/stock",
        json={"delta": 10},
        headers=auth_headers,
    )
    assert stock_body_res.status_code == 200
    assert stock_body_res.json()["stock_quantity"] == 55
