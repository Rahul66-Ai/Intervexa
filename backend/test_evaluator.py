from utils.question_loader import load_questions
from utils.answer_evaluator import evaluate_answer


# Load Python questions
questions = load_questions("Python")


# Take first question
question = questions[0]


print("\n======================================")
print("       INTERVEXA ANSWER TEST")
print("======================================\n")


print("Question:")
print(question["question"])

print("\nExpected Concepts:")

for concept in question["expected_concepts"]:
    print("-", concept)


print("\n--------------------------------------")


# Temporary student answer
student_answer = input("\nEnter your answer: ")


# Evaluate answer
result = evaluate_answer(
    question,
    student_answer
)


print("\n======================================")
print("           EVALUATION")
print("======================================\n")


print("Score:", result["score"], "/ 10")


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


print("\n======================================")