from app.agents.reservation_agent import (

    validate_aadhaar,

    validate_license,

    validate_car_number,

    validate_date,

    validate_end_date
)


# =====================================
# AADHAAR TESTS
# =====================================

def test_valid_aadhaar():

    assert validate_aadhaar(
        "123456789012"
    ) == True


def test_invalid_aadhaar():

    assert validate_aadhaar(
        "12345"
    ) == False


# =====================================
# LICENSE TESTS
# =====================================

def test_valid_license():

    assert validate_license(
        "TS0920231234567"
    ) == True


def test_invalid_license():

    assert validate_license(
        "ABC123"
    ) == False


# =====================================
# CAR NUMBER TESTS
# =====================================

def test_valid_car_number():

    assert validate_car_number(
        "TS09AB1234"
    ) == True


def test_invalid_car_number():

    assert validate_car_number(
        "123456"
    ) == False


# =====================================
# DATE TESTS
# =====================================

def test_valid_date():

    assert validate_date(
        "2030-01-01"
    ) == True


def test_invalid_date():

    assert validate_date(
        "2020-01-01"
    ) == False


# =====================================
# END DATE TESTS
# =====================================

def test_valid_end_date():

    assert validate_end_date(

        "2030-01-01",

        "2030-01-05"

    ) == True


def test_invalid_end_date():

    assert validate_end_date(

        "2030-01-10",

        "2030-01-05"

    ) == False