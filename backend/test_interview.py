from utils.interview_engine import InterviewSession


skills = [
    "Python",
    "C++",
    "JavaScript"
]


session = InterviewSession(skills)


print("\n================================")
print("       INTERVEXA INTERVIEW")
print("================================\n")


print("Student Skills:")

for skill in skills:
    print("-", skill)


print("\nInterview Started!\n")


for i in range(5):

    question = session.get_next_question()

    if question is None:
        print("No more questions available.")
        break

    print(f"Question {i + 1}:")
    print(question["question"])

    print("Topic:", question["topic"])
    print("Difficulty:", question["difficulty"])

    print("--------------------------------")