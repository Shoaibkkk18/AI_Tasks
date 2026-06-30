from fastapi import FastAPI
from fastapi import HTTPException

from app.mcp.reservation_writer import (
    write_reservation
)

app = FastAPI(
    title="Parking Reservation MCP Server"
)


# =====================================
# HOME
# =====================================

@app.get("/")
def home():

    return {
        "message":
        "MCP Server Running"
    }


# =====================================
# HEALTH CHECK
# =====================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =====================================
# WRITE RESERVATION
# =====================================

@app.post(
    "/write-reservation"
)
def save_reservation(
    reservation: dict
):

    required_fields = [

        "reservation_id",

        "first_name",

        "last_name",

        "car_number",

        "start_date",

        "end_date"
    ]

    for field in required_fields:

        if field not in reservation:

            raise HTTPException(

                status_code=400,

                detail=(
                    f"Missing field: "
                    f"{field}"
                )
            )

    return write_reservation(
        reservation
    )