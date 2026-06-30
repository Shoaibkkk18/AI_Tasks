from fastapi.testclient import TestClient

from app.mcp.reservation_server import app


client = TestClient(app)


def test_health_endpoint():

    response = client.get(
        "/health"
    )

    assert (
        response.status_code
        == 200
    )

    assert (
        response.json()
        ==
        {"status": "healthy"}
    )


def test_write_reservation():

    sample = {

        "reservation_id":
        "API-001",

        "first_name":
        "Test",

        "last_name":
        "User",

        "car_number":
        "TS09AB1234",

        "start_date":
        "2030-01-01",

        "end_date":
        "2030-01-02"
    }

    response = client.post(
        "/write-reservation",
        json=sample
    )

    assert (
        response.status_code
        == 200
    )


def test_missing_field():

    sample = {

        "first_name":
        "OnlyName"
    }

    response = client.post(
        "/write-reservation",
        json=sample
    )

    assert (
        response.status_code
        == 400
    )