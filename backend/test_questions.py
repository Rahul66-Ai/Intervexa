from utils.question_loader import load_questions


topics = [
    "Python",
    "C",
    "C++",
    "Java",
    "HTML",
    "CSS",
    "JavaScript",
    "Data Structures",
    "Computer Fundamentals"
]


print("\n========== QUESTION BANK TEST ==========\n")


for topic in topics:

    questions = load_questions(topic)

    print(f"{topic}: {len(questions)} questions")


print("\n========================================")