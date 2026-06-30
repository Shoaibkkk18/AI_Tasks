import re

from datetime import datetime

from app.agents.state_manager import (
    reservation_state
)


# =========================================
# RESERVATION QUESTIONS
# =========================================

reservation_questions = {

    "first_name":
        "Enter first name:",

    "last_name":
        "Enter last name:",

    "verification_type":
        (
            "Choose verification type "
            "(Aadhaar/License):"
        ),

    "verification_id":
        (
            "Enter verification ID:"
        ),
        
        "parking_type":
    (
        "Choose parking type "
        "(Standard/VIP/EV):"
    ),

    "car_number":
        (
            "Enter car number "
            "(Format: TS09AB1234):"
        ),

    "start_date":
        (
            "Enter reservation start date "
            "(YYYY-MM-DD):"
        ),

    "end_date":
        (
            "Enter reservation end date "
            "(YYYY-MM-DD):"
        )
}


# =========================================
# AADHAAR VALIDATION
# =========================================

def validate_aadhaar(aadhaar):

    aadhaar = aadhaar.replace("-", "")

    return (
        aadhaar.isdigit()
        and
        len(aadhaar) == 12
    )


# =========================================
# LICENSE VALIDATION
# =========================================

def validate_license(license_id):

    pattern = r"^[A-Z]{2}[0-9]{2}[0-9]{11}$"

    return bool(
        re.match(pattern, license_id)
    )


# =========================================
# MASK SENSITIVE ID
# =========================================

def mask_sensitive_id(value):

    if len(value) <= 4:
        return value

    return (
        "X" * (len(value) - 4)
        + value[-4:]
    )

# VALIDATE PARKING TYPE

    if missing_field == "parking_type":

        valid_types = [
        "standard",
        "vip",
        "ev"
    ]

    if user_input.lower() not in valid_types:

              return (
            "Invalid parking type. "
            "Choose Standard, VIP, or EV:"
        )

    user_input = user_input.upper()
# =========================================
# CAR NUMBER VALIDATION
# FORMAT: TS09AB1234
# =========================================

def validate_car_number(car_number):

    pattern = (
        r"^[A-Z]{2}"
        r"[0-9]{2}"
        r"[A-Z]{2}"
        r"[0-9]{4}$"
    )

    return bool(
        re.match(pattern, car_number)
    )


# =========================================
# DATE VALIDATION
# =========================================

def validate_date(date_string):

    try:

        reservation_date = datetime.strptime(
            date_string,
            "%Y-%m-%d"
        ).date()

        today = datetime.today().date()

        return reservation_date >= today

    except ValueError:

        return False


# =========================================
# END DATE VALIDATION
# =========================================

def validate_end_date(
    start_date,
    end_date
):

    try:

        start = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        ).date()

        end = datetime.strptime(
            end_date,
            "%Y-%m-%d"
        ).date()

        return end >= start

    except ValueError:

        return False


# =========================================
# GET NEXT MISSING FIELD
# =========================================

def get_next_missing_field():

    for field, value in reservation_state.items():

        if field == "status":
            continue

        if value is None:
            return field

    return None


# =========================================
# MAIN RESERVATION COLLECTION
# =========================================

def collect_reservation_details(
    user_input=None
):

    missing_field = get_next_missing_field()

    if user_input and missing_field:

        # =================================
        # VALIDATE VERIFICATION TYPE
        # =================================

        if missing_field == "verification_type":

            valid_types = [
                "aadhaar",
                "license"
            ]

            if user_input.lower() not in valid_types:

                return (
                    "Invalid type. "
                    "Choose Aadhaar or License:"
                )

        # =================================
        # VALIDATE VERIFICATION ID
        # =================================

        if missing_field == "verification_id":

            verification_type = (
                reservation_state[
                    "verification_type"
                ].lower()
            )

            if verification_type == "aadhaar":

                if not validate_aadhaar(
                    user_input
                ):

                    return (
                        "Invalid Aadhaar number. "
                        "Enter 12 digits:"
                    )

            if verification_type == "license":

                if not validate_license(
                    user_input
                ):

                    return (
                        "Invalid license format."
                    )

            # MASK BEFORE STORING

            user_input = mask_sensitive_id(
                user_input
            )

        # =================================
        # VALIDATE CAR NUMBER
        # =================================

        if missing_field == "car_number":

            if not validate_car_number(
                user_input
            ):

                return (
                    "Invalid car number format. "
                    "Use format like TS09AB1234:"
                )

        # =================================
        # VALIDATE START DATE
        # =================================

        if missing_field == "start_date":

            if not validate_date(
                user_input
            ):

                return (
                    "Invalid start date. "
                    "Use YYYY-MM-DD "
                    "and avoid past dates:"
                )

        # =================================
        # VALIDATE END DATE
        # =================================

        if missing_field == "end_date":

            if not validate_date(
                user_input
            ):

                return (
                    "Invalid end date. "
                    "Use YYYY-MM-DD "
                    "and avoid past dates:"
                )

            if not validate_end_date(

                reservation_state[
                    "start_date"
                ],

                user_input

            ):

                return (
                    "End date cannot be "
                    "before start date:"
                )

        # =================================
        # STORE VALUE
        # =================================

        reservation_state[
            missing_field
        ] = user_input

    # =====================================
    # NEXT QUESTION
    # =====================================

    next_field = get_next_missing_field()

    if next_field:

        return reservation_questions[
            next_field
        ]

    return "Reservation details completed."