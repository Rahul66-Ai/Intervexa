from utils.interview_engine import InterviewSession
from utils.answer_evaluator import evaluate_answer


print("\n==========================================")
print("           INTERVEXA INTERVIEW")
print("==========================================\n")


# Temporary skills
# Later these will come automatically from resume.
skills = [
    "Python",
    "C++",
    "JavaScript",
    "Data Structures"
]


print("Your detected skills:")

for skill in skills:
    print("-", skill)


print("\n------------------------------------------")
print("Interview is starting...")
print("------------------------------------------\n")


# Create interview session
session = InterviewSession(skills)


TOTAL_QUESTIONS = 5


for question_number in range(1, TOTAL_QUESTIONS + 1):

    # Get next question
    question = session.get_next_question()

    if question is None:

        print("\nNo more questions available.")

        break


    # Display question
    print("\n==========================================")
    print(f"Question {question_number}/{TOTAL_QUESTIONS}")
    print("==========================================")

    print("\nTopic:")
    print(question["topic"])

    print("\nDifficulty:")
    print(question["difficulty"])

    print("\nQuestion:")
    print(question["question"])


    # Get student's answer
    print("\n------------------------------------------")

    student_answer = input("Your Answer: ")


    # Evaluate answer
    result = evaluate_answer(
        question,
        student_answer
    )


    # Save answer and score
    session.submit_answer(
        student_answer,
        result["score"]
    )


    # Show result
    print("\n------------------------------------------")
    print("INTERVEXA EVALUATION")
    print("------------------------------------------")

    print(
        f"\nScore: {result['score']}/10"
    )


    print("\nConcepts Covered:")

    if result["matched_concepts"]:

        for concept in result["matched_concepts"]:
            print("✓", concept)

    else:

        print("None")


    print("\nMissing Concepts:")

    if result["missing_concepts"]:

        for concept in result["missing_concepts"]:
            print("✗", concept)

    else:

        print("None")


    print("\nFeedback:")
    print(result["feedback"])


# Final report

print("\n\n==========================================")
print("          INTERVIEW COMPLETED")
print("==========================================\n")


print("Questions Attempted:")
print(len(session.answers))


print("\nScores:")

for index, score in enumerate(session.scores, start=1):

    print(
        f"Question {index}: {score}/10"
    )


print("\nAverage Score:")

print(
    f"{session.get_average_score()}/10"
)


print("\n==========================================")
print("       THANK YOU FOR USING INTERVEXA")
print("==========================================")