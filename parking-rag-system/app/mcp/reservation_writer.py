from datetime import datetime
import os


OUTPUT_DIR = "data/storage"

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "confirmed_reservations.txt"
)


def write_reservation(
    reservation
):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    reservation_id = reservation.get(
        "reservation_id",
        "UNKNOWN"
    )

    # Read existing records
    if os.path.exists(
        OUTPUT_FILE
    ):

        with open(
            OUTPUT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            existing_data = file.read()

            if (
                reservation_id
                in existing_data
            ):

                return {
                    "status":
                    "duplicate_reservation"
                }

    line = (

        f"{reservation_id} | "

        f"{reservation['first_name']} "
        f"{reservation['last_name']} | "

        f"{reservation['car_number']} | "

        f"{reservation['start_date']} "
        f"to "
        f"{reservation['end_date']} | "

        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )

    with open(
        OUTPUT_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(line)

    return {
        "status":
        "success"
    }