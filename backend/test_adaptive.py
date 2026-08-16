from utils.interview_engine import InterviewSession


print("\n==========================================")
print("       INTERVEXA ADAPTIVE TEST")
print("==========================================\n")


# Test skills
skills = ["C"]


# Create interview session
session = InterviewSession(skills)


# ------------------------------------------
# QUESTION 1
# ------------------------------------------

question = session.get_next_question()


print("Question 1")
print("------------------------------------------")

print("Difficulty:", question["difficulty"])

print("Question:", question["question"])


# ------------------------------------------
# Simulate weak answer
# ------------------------------------------

print("\nSimulating score: 3/10")

session.submit_answer(
    "wrong answer",
    3
)


# ------------------------------------------
# QUESTION 2
# ------------------------------------------

question = session.get_next_question()


print("\nQuestion 2")
print("------------------------------------------")

print("Difficulty:", question["difficulty"])

print("Question:", question["question"])


# ------------------------------------------
# Simulate strong answer
# ------------------------------------------

print("\nSimulating score: 9/10")

session.submit_answer(
    "excellent answer",
    9
)


# ------------------------------------------
# QUESTION 3
# ------------------------------------------

question = session.get_next_question()


print("\nQuestion 3")
print("------------------------------------------")

print("Difficulty:", question["difficulty"])

print("Question:", question["question"])


# ------------------------------------------
# FINAL
# ------------------------------------------

print("\n==========================================")
print("          ADAPTIVE TEST COMPLETE")
print("==========================================")