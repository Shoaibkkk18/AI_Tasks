import json
import os

DATABASE_FILE = "temp_test.json"


def test_save_reservation():

    reservation = {
        "name": "Shoaib"
    }

    with open(DATABASE_FILE, "w") as file:
        json.dump([reservation], file)

    with open(DATABASE_FILE, "r") as file:
        data = json.load(file)

    assert data[0]["name"] == "Shoaib"

    os.remove(DATABASE_FILE)


def test_multiple_reservations():

    reservations = [
        {"name": "Shoaib"},
        {"name": "Ali"}
    ]

    with open(DATABASE_FILE, "w") as file:
        json.dump(reservations, file)

    with open(DATABASE_FILE, "r") as file:
        data = json.load(file)

    assert len(data) == 2

    os.remove(DATABASE_FILE)