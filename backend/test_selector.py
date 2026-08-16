from utils.question_selector import get_random_question


print("\n========== RANDOM QUESTION ==========\n")


question = get_random_question("Python")


print("Question:")
print(question["question"])

print("\nDifficulty:")
print(question["difficulty"])

print("\nExpected Concepts:")
print(question["expected_concepts"])

print("\n=====================================\n")