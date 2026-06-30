import os
import requests

from datetime import datetime

from app.graph.graph_state import (
    ParkingGraphState
)


# =====================================
# LOGGING
# =====================================

def log_event(message):

    os.makedirs(
        "logs",
        exist_ok=True
    )

    with open(
        "logs/workflow.log",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"[{datetime.now()}] "
            f"{message}\n"
        )


# =====================================
# USER NODE
# =====================================

def user_node(
    state: ParkingGraphState
):

    print(
        "\n[USER NODE]"
    )

    log_event(
        "User node executed"
    )

    return state


# =====================================
# RESERVATION NODE
# =====================================

def reservation_node(
    state: ParkingGraphState
):

    print(
        "\n[RESERVATION NODE]"
    )

    state["status"] = (
        "pending"
    )

    log_event(
        "Reservation node executed"
    )

    return state


# =====================================
# APPROVAL NODE
# =====================================

def approval_node(
    state: ParkingGraphState
):

    print(
        "\n[APPROVAL NODE]"
    )

    log_event(
        "Approval node executed"
    )

    # Used by automated tests
    if state.get(
        "test_mode",
        False
    ):

        decision = "yes"

    else:

        decision = input(
            "Approve reservation? (yes/no): "
        )

    if (
        decision.lower()
        == "yes"
    ):

        state["status"] = (
            "approved"
        )

        log_event(
            "Reservation approved"
        )

    else:

        state["status"] = (
            "rejected"
        )

        log_event(
            "Reservation rejected"
        )

    return state


# =====================================
# MCP NODE
# =====================================

def mcp_node(
    state: ParkingGraphState
):

    print(
        "\n[MCP NODE]"
    )

    log_event(
        "MCP node executed"
    )

    if (
        state["status"]
        != "approved"
    ):

        print(
            "Reservation not approved."
        )

        log_event(
            "MCP skipped because reservation was not approved"
        )

        return state

    try:

        response = requests.post(

            "http://127.0.0.1:8000/write-reservation",

            json=state,

            timeout=10

        )

        print(
            "MCP Response:",
            response.json()
        )

        log_event(
            f"MCP response: {response.json()}"
        )

    except Exception as error:

        print(
            f"MCP Error: {error}"
        )

        log_event(
            f"MCP error: {error}"
        )

    return state


# =====================================
# STORAGE NODE
# =====================================

def storage_node(
    state: ParkingGraphState
):

    print(
        "\n[STORAGE NODE]"
    )

    print(
        "Reservation stored successfully."
    )

    log_event(
        "Storage node executed"
    )

    return state