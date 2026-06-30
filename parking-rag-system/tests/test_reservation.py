from app.utils.reservation import (
    get_next_missing_field
)


def test_next_missing_field():

    state = {
        "name": None,
        "car": "TS09AB1234"
    }

    result = get_next_missing_field(state)

    assert result == "name"


def test_no_missing_field():

    state = {
        "name": "Shoaib",
        "car": "TS09AB1234"
    }

    result = get_next_missing_field(state)

    assert result is None