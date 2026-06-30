from app.rag.rag_utils import (
    calculate_recall_at_k,
    calculate_precision_at_k
)


class MockDocument:

    def __init__(self, content):
        self.page_content = content


def test_recall_at_k():

    docs = [
        MockDocument("Parking price is $5/hour")
    ]

    result = calculate_recall_at_k(
        docs,
        "$5/hour"
    )

    assert result == 1


def test_precision_at_k():

    docs = [
        MockDocument("Parking price is $5/hour"),
        MockDocument("Working hours are 24/7")
    ]

    precision = calculate_precision_at_k(
        docs,
        "$5/hour"
    )

    assert precision == 0.5