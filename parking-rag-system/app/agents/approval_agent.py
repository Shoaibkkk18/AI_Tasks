import json
import requests

from datetime import datetime


# =====================================
# FILE PATHS
# =====================================

PENDING_FILE = (
    "data/reservations/"
    "pending_reservations.json"
)

APPROVED_FILE = (
    "data/reservations/"
    "approved_reservations.json"
)

REJECTED_FILE = (
    "data/reservations/"
    "rejected_reservations.json"
)


# =====================================
# LOAD JSON
# =====================================

def load_json(file_path):

    with open(file_path, "r") as file:

        return json.load(file)


# =====================================
# SAVE JSON
# =====================================

def save_json(file_path, data):
    

    with open(file_path, "w") as file:

        json.dump(data, file, indent=4)
        
def send_to_mcp_server(
    reservation
):

    try:

        response = requests.post(

            "http://127.0.0.1:8000/write-reservation",

            json=reservation,

            timeout=10

        )

        return response.json()

    except Exception as error:

        print(
            f"\nMCP Server Error: "
            f"{error}\n"
        )

        return None


# =====================================
# DISPLAY RESERVATIONS
# =====================================

def display_reservations(
    reservations
):

    if not reservations:

        print(
            "\nNo reservations found.\n"
        )

        return

    for reservation in reservations:

        print("\n" + "="*60)

        print(
            f"Reservation ID: "
            f"{reservation['reservation_id']}"
        )

        print("="*60)

        for key, value in reservation.items():

            print(f"{key}: {value}")

        print()


# =====================================
# SEARCH RESERVATION
# =====================================

def search_reservation(
    reservation_id
):

    files = [

        PENDING_FILE,

        APPROVED_FILE,

        REJECTED_FILE
    ]

    for file_path in files:

        reservations = load_json(
            file_path
        )

        for reservation in reservations:

            if (

                reservation[
                    "reservation_id"
                ]

                == reservation_id

            ):

                print("\n" + "="*60)

                print(
                    f"Reservation Found: "
                    f"{reservation_id}"
                )

                print("="*60)

                for key, value in reservation.items():

                    print(f"{key}: {value}")

                print()

                return

    print(
        "\nReservation not found.\n"
    )


# =====================================
# APPROVE RESERVATION
# =====================================

def approve_reservation(
    reservation_id
):

    pending = load_json(
        PENDING_FILE
    )

    approved = load_json(
        APPROVED_FILE
    )

    updated_pending = []

    found = False

    for reservation in pending:

        if (

            reservation[
                "reservation_id"
            ]

            == reservation_id

        ):

            reservation[
                "status"
            ] = "approved"

            reservation[
                "reviewed_at"
            ] = str(datetime.now())

            approved.append(
                reservation
            )
            
            send_to_mcp_server(
                reservation
             )

            found = True

        else:

            updated_pending.append(
                reservation
            )

    save_json(
        PENDING_FILE,
        updated_pending
    )

    save_json(
        APPROVED_FILE,
        approved
    )

    if found:

        print(
            f"\nReservation "
            f"{reservation_id} approved.\n"
        )

    else:

        print(
            "\nReservation not found.\n"
        )


# =====================================
# REJECT RESERVATION
# =====================================

def reject_reservation(
    reservation_id
):

    pending = load_json(
        PENDING_FILE
    )

    rejected = load_json(
        REJECTED_FILE
    )

    updated_pending = []

    found = False

    for reservation in pending:

        if (

            reservation[
                "reservation_id"
            ]

            == reservation_id

        ):

            reservation[
                "status"
            ] = "rejected"

            reservation[
                "reviewed_at"
            ] = str(datetime.now())

            rejected.append(
                reservation
            )

            found = True

        else:

            updated_pending.append(
                reservation
            )

    save_json(
        PENDING_FILE,
        updated_pending
    )

    save_json(
        REJECTED_FILE,
        rejected
    )

    if found:

        print(
            f"\nReservation "
            f"{reservation_id} rejected.\n"
        )

    else:

        print(
            "\nReservation not found.\n"
        )


# =====================================
# MAIN ADMIN CHATBOT
# =====================================

def approval_chatbot():

    print("\n" + "="*60)

    print(" ADMIN APPROVAL AGENT ")

    print("="*60)

    print("""
Commands:

list
approve RES-2026-0001
reject RES-2026-0001
search RES-2026-0001
view approved
view rejected
exit
""")

    while True:

        command = input(
            "\nAdmin: "
        )

        # =================================
        # EXIT
        # =================================

        if command.lower() == "exit":

            print("\nGoodbye.\n")

            break

        # =================================
        # LIST PENDING
        # =================================

        elif command.lower() == "list":

            pending = load_json(
                PENDING_FILE
            )

            display_reservations(
                pending
            )

        # =================================
        # VIEW APPROVED
        # =================================

        elif command.lower() == (
            "view approved"
        ):

            approved = load_json(
                APPROVED_FILE
            )

            display_reservations(
                approved
            )

        # =================================
        # VIEW REJECTED
        # =================================

        elif command.lower() == (
            "view rejected"
        ):

            rejected = load_json(
                REJECTED_FILE
            )

            display_reservations(
                rejected
            )

        # =================================
        # SEARCH RESERVATION
        # =================================

        elif command.lower().startswith(
            "search"
        ):

            parts = command.split()

            if len(parts) != 2:

                print(
                    "\nInvalid command.\n"
                )

                continue

            search_reservation(
                parts[1]
            )

        # =================================
        # APPROVE
        # =================================

        elif command.lower().startswith(
            "approve"
        ):

            parts = command.split()

            if len(parts) != 2:

                print(
                    "\nInvalid command.\n"
                )

                continue

            approve_reservation(
                parts[1]
            )

        # =================================
        # REJECT
        # =================================

        elif command.lower().startswith(
            "reject"
        ):

            parts = command.split()

            if len(parts) != 2:

                print(
                    "\nInvalid command.\n"
                )

                continue

            reject_reservation(
                parts[1]
            )

        # =================================
        # UNKNOWN COMMAND
        # =================================

        else:

            print(
                "\nUnknown command.\n"
            )