"""
Example Automated Abuse Test: Cross-Tenant BOLA / IDOR Verification.
Can be executed with `pytest` to guarantee that multi-tenant isolation is enforced.
"""

import os
import requests
import pytest

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000/api")


def is_api_reachable() -> bool:
    try:
        requests.get(BASE_URL, timeout=0.2)
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not is_api_reachable(),
    reason="Live API test server not running (specify API_BASE_URL to run live verification)",
)

# Test Fixtures: Two distinct tenants with isolated auth tokens
TENANT_A_TOKEN = os.getenv("TENANT_A_TOKEN", "mock-jwt-tenant-a-user-1")
TENANT_B_TOKEN = os.getenv("TENANT_B_TOKEN", "mock-jwt-tenant-b-user-2")


@pytest.fixture
def client_tenant_a():
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {TENANT_A_TOKEN}",
        "Content-Type": "application/json"
    })
    return session


@pytest.fixture
def client_tenant_b():
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {TENANT_B_TOKEN}",
        "Content-Type": "application/json"
    })
    return session


def test_cross_tenant_bola_access_control(client_tenant_a, client_tenant_b):
    """
    Abuse Scenario: Tenant B attempts to read an invoice belonging to Tenant A.
    Expected: HTTP 403 Forbidden or 404 Not Found.
    Vulnerable: HTTP 200 OK with Tenant A's private data.
    """
    # 1. Tenant A creates a private invoice
    create_res = client_tenant_a.post(f"{BASE_URL}/invoices", json={
        "amount": 1500.00,
        "description": "Tenant A Confidential Consulting Services"
    })
    assert create_res.status_code in (200, 201), f"Failed to create setup invoice: {create_res.text}"
    invoice_id = create_res.json()["id"]

    # 2. Tenant A can read their own invoice
    own_read_res = client_tenant_a.get(f"{BASE_URL}/invoices/{invoice_id}")
    assert own_read_res.status_code == 200
    assert own_read_res.json()["id"] == invoice_id

    # 3. Tenant B attempts to read Tenant A's invoice (BOLA / IDOR attack)
    attacker_res = client_tenant_b.get(f"{BASE_URL}/invoices/{invoice_id}")

    # Enforce ASTF-API1 / ASVS V13.1.1 compliance
    assert attacker_res.status_code in (403, 404), (
        f"🚨 CRITICAL BOLA VULNERABILITY DETECTED! Tenant B accessed Tenant A's invoice {invoice_id}. "
        f"Expected 403/404 but got status {attacker_res.status_code} with body: {attacker_res.text}"
    )

    # 4. Tenant B attempts to modify Tenant A's invoice
    tamper_res = client_tenant_b.put(f"{BASE_URL}/invoices/{invoice_id}", json={
        "amount": 0.01,
        "description": "Tampered by Attacker"
    })
    assert tamper_res.status_code in (403, 404), (
        f"🚨 CRITICAL BOLA VULNERABILITY DETECTED! Tenant B modified Tenant A's invoice {invoice_id}."
    )
