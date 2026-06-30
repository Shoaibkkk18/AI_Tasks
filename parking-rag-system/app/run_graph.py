from app.graph.workflow import (
    graph
)

state = {

    "reservation_id":
    "RES-2026-0001",

    "first_name":
    "Shoaib",

    "last_name":
    "Khan",

    "parking_type":
    "VIP",

    "car_number":
    "TS09AB1234",

    "start_date":
    "2026-07-01",

    "end_date":
    "2026-07-03",

    "status":
    "new"
}

result = graph.invoke(
    state
)

print("\nFINAL STATE:\n")

print(result)