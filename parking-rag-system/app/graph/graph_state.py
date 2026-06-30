from typing import TypedDict


class ParkingGraphState(
    TypedDict
):

    reservation_id: str

    first_name: str

    last_name: str

    parking_type: str

    car_number: str

    start_date: str

    end_date: str

    status: str