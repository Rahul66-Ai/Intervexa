import json
from pathlib import Path


QUESTIONS_FOLDER = Path("questions")


def load_questions(topic):
    """
    Load questions for a particular topic.
    """

    topic_files = {
        "Python": "python.json",
        "C": "c.json",
        "C++": "cpp.json",
        "Java": "java.json",
        "HTML": "html.json",
        "CSS": "css.json",
        "JavaScript": "javascript.json",
        "Data Structures": "dsa.json",
        "Computer Fundamentals": "computer_fundamentals.json"
    }

    if topic not in topic_files:
        return []

    file_path = QUESTIONS_FOLDER / topic_files[topic]

    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)