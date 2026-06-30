from app.graph.workflow import (
    graph
)


def test_graph_execution():

    state = {

        "reservation_id":
        "TEST-001",

        "first_name":
        "Test",

        "last_name":
        "User",

        "parking_type":
        "VIP",

        "car_number":
        "TS09AB1234",

        "start_date":
        "2030-01-01",

        "end_date":
        "2030-01-02",

        "status":
        "approved"
    }

    result = graph.invoke(
        state
    )

    assert (
        result["status"]
        in
        [
            "approved",
            "rejected"
        ]
    )