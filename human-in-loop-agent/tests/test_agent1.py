def test_reservation_data_structure():

    reservation_data = {
        "name": "Shoaib",
        "date": "Tomorrow",
        "time": "8 PM",
        "guests": 4
    }

    assert reservation_data["name"] == "Shoaib"
    assert reservation_data["guests"] == 4


def test_missing_fields():

    reservation_data = {
        "name": "",
        "date": "",
        "time": "",
        "guests": 0
    }

    assert reservation_data["name"] == ""
    assert reservation_data["guests"] == 0