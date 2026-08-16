import re


def clean_text(text):
    """
    Convert text into a simple set of words.
    """

    text = text.lower()

    words = re.findall(r"[a-zA-Z0-9+#]+", text)

    return set(words)


def evaluate_answer(question, answer):
    """
    Evaluate a student's answer based on
    expected concepts of the question.
    """

    expected_concepts = question.get("expected_concepts", [])

    answer_words = clean_text(answer)

    matched_concepts = []
    missing_concepts = []

    for concept in expected_concepts:

        concept_words = clean_text(concept)

        # Check whether concept words are present
        if concept_words.issubset(answer_words):
            matched_concepts.append(concept)
        else:
            missing_concepts.append(concept)

    total_concepts = len(expected_concepts)

    if total_concepts == 0:
        score = 0
    else:
        score = round(
            (len(matched_concepts) / total_concepts) * 10,
            1
        )

    # Generate feedback
    if score >= 8:
        feedback = "Excellent answer. You covered the important concepts."

    elif score >= 6:
        feedback = "Good answer, but some important concepts are missing."

    elif score >= 4:
        feedback = "Your answer has some relevant points, but needs more explanation."

    else:
        feedback = "The answer needs significant improvement."

    return {
        "score": score,
        "matched_concepts": matched_concepts,
        "missing_concepts": missing_concepts,
        "feedback": feedback
    }