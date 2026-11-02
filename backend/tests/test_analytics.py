"""Analytics and Recommendation endpoints tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_analytics_and_recommendations(client: AsyncClient, auth_headers: dict[str, str]):
    # 1. Analytics Summary
    summary_res = await client.get("/api/analytics/summary", headers=auth_headers)
    assert summary_res.status_code == 200
    data = summary_res.json()
    assert "kpis" in data
    assert "sales_over_time" in data
    assert isinstance(data["kpis"], list)

    # 2. Recommendations
    rec_res = await client.get("/api/recommendations/customer/cust-random-001?limit=5")
    assert rec_res.status_code == 200
    rec_data = rec_res.json()
    assert rec_data["customer_id"] == "cust-random-001"
    assert len(rec_data["recommendations"]) == 5
