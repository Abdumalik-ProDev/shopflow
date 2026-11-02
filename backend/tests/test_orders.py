"""Orders, checkout, payment, and review endpoints tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_order_creation_and_lifecycle(client: AsyncClient, auth_headers: dict[str, str]):
    # 1. Create Customer
    cust_res = await client.post(
        "/api/customers",
        json={
            "customer_unique_id": "cust-test-1234",
            "customer_zip_code_prefix": "01310",
            "customer_city": "Sao Paulo",
            "customer_state": "SP",
        },
        headers=auth_headers,
    )
    assert cust_res.status_code == 201
    customer_id = cust_res.json()["id"]

    # 2. Create Product
    prod_res = await client.post(
        "/api/products",
        json={
            "sku": "SKU-BOOK-001",
            "name": "Machine Learning Guide",
            "price": 49.99,
            "stock_quantity": 20,
        },
        headers=auth_headers,
    )
    assert prod_res.status_code == 201
    product_id = prod_res.json()["id"]

    # 3. Create Order
    order_payload = {
        "customer_id": customer_id,
        "items": [
            {
                "product_id": product_id,
                "seller_id": "seller-001",
                "price": 49.99,
                "freight_value": 10.0,
                "quantity": 2,
            }
        ],
    }
    order_res = await client.post("/api/orders", json=order_payload, headers=auth_headers)
    assert order_res.status_code == 201
    order_data = order_res.json()
    assert order_data["customer_id"] == customer_id
    assert order_data["status"] == "pending"
    assert order_data["total"] == 99.98
    order_id = order_data["id"]

    # 4. Check Stock Decrement
    check_prod = await client.get(f"/api/products/{product_id}")
    assert check_prod.json()["stock_quantity"] == 18

    # 5. Add Payment
    pay_res = await client.post(
        "/api/payments",
        json={
            "order_id": order_id,
            "payment_sequential": 1,
            "payment_type": "credit_card",
            "payment_installments": 3,
            "payment_value": 109.98,
        },
        headers=auth_headers,
    )
    assert pay_res.status_code == 201
    assert pay_res.json()["payment_value"] == 109.98

    # 6. Update Status to delivered
    status_res = await client.patch(
        f"/api/orders/{order_id}/status",
        json={"status": "delivered"},
        headers=auth_headers,
    )
    assert status_res.status_code == 200
    assert status_res.json()["status"] == "delivered"
    assert status_res.json()["delivered_customer_date"] is not None

    # 7. Add Review
    rev_res = await client.post(
        "/api/reviews",
        json={
            "order_id": order_id,
            "review_score": 5,
            "comment_title": "Excellent book",
            "comment_message": "Arrived promptly and well packed.",
        },
        headers=auth_headers,
    )
    assert rev_res.status_code == 201
    assert rev_res.json()["review_score"] == 5
