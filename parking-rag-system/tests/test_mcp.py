from app.mcp.reservation_writer import (
    write_reservation
)


def test_write_reservation():

    sample = {

        "reservation_id": "TEST-001",

        "first_name": "Test",

        "last_name": "User",

        "car_number": "TS09AB1234",

        "start_date": "2030-01-01",

        "end_date": "2030-01-02"
    }

    result = write_reservation(
        sample
    )

    assert (
        result["status"]
        == "success"
        or
        result["status"]
        == "duplicate_reservation"
    )


def test_duplicate_reservation():

    sample = {

        "reservation_id": "TEST-DUP",

        "first_name": "Test",

        "last_name": "User",

        "car_number": "TS09AB1234",

        "start_date": "2030-01-01",

        "end_date": "2030-01-02"
    }

    write_reservation(
        sample
    )

    result = write_reservation(
        sample
    )

    assert (
        result["status"]
        ==
        "duplicate_reservation"
    )