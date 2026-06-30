def test_full_workflow():

    reservation = {
        "name": "Shoaib",
        "status": "approved"
    }

    assert reservation["status"] == "approved"


def test_rejected_workflow():

    reservation = {
        "name": "Ali",
        "status": "rejected"
    }

    assert reservation["status"] == "rejected"