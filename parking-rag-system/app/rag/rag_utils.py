def calculate_recall_at_k(results, expected_keyword):

    retrieved_text = " ".join(
        [doc.page_content for doc in results]
    )

    if expected_keyword.lower() in retrieved_text.lower():
        return 1

    return 0


def calculate_precision_at_k(results, expected_keyword):

    relevant_docs = 0

    for doc in results:

        if expected_keyword.lower() in doc.page_content.lower():
            relevant_docs += 1

    precision = relevant_docs / len(results)

    return precision