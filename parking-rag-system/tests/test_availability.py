from app.utils.availability import (
    check_availability
)


def test_standard_availability():

    result = check_availability("Standard")

    assert result >= 0


def test_vip_availability():

    result = check_availability("VIP")

    assert result >= 0