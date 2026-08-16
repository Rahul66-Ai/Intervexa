from utils.ai_interviewer import ask_ai


prompt = """
You are an AI technical interviewer.

Ask me exactly ONE short interview question
about Python.

Do not provide the answer.

Only return the interview question.
"""


question = ask_ai(prompt)


print("\n================================")
print("       INTERVEXA AI TEST")
print("================================\n")

print(question)

print("\n================================")