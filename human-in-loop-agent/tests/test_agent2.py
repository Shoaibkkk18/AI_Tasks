def process_admin_decision(decision):

    decision = decision.strip().lower()

    if decision == "approve":
        return "approved"

    elif decision == "reject":
        return "rejected"

    else:
        return "invalid"


def test_approve():

    assert process_admin_decision("approve") == "approved"


def test_reject():

    assert process_admin_decision("reject") == "rejected"


def test_invalid():

    assert process_admin_decision("maybe") == "invalid"