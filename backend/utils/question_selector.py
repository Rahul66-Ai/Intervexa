import random

from utils.question_loader import load_questions


def get_random_question(topic, difficulty=None):

    questions = load_questions(topic)

    if not questions:
        return None

    # If difficulty is specified
    if difficulty:

        filtered_questions = [
            question
            for question in questions
            if question["difficulty"] == difficulty
        ]

        if filtered_questions:
            questions = filtered_questions

    return random.choice(questions)