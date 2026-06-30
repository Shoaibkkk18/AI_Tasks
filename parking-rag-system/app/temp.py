from app.mcp.reservation_writer import (
    write_reservation
)

sample = {

    "first_name": "Shoaib",

    "last_name": "Khan",

    "car_number": "TS09AB1234",

    "start_date": "2026-07-01",

    "end_date": "2026-07-03"
}

result = write_reservation(
    sample
)

print(result)