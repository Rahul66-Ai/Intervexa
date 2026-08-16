from utils.resume_interview import create_interview_from_resume


resume_text = """
I am a Computer Science student.

Technical Skills:
Python
C++
JavaScript
Data Structures

I have developed web applications using HTML and CSS.
"""


session, skills = create_interview_from_resume(resume_text)


print("\n======================================")
print("       INTERVEXA RESUME TEST")
print("======================================\n")


print("Detected Skills:")

for skill in skills:
    print("-", skill)


if session is None:

    print("\nNo skills detected.")
    print("Interview cannot start.")

else:

    print("\nInterview successfully created!")

    print("\nFirst Question:")

    question = session.get_next_question()

    if question:

        print(question["question"])
        print("Topic:", question["topic"])
        print("Difficulty:", question["difficulty"])


print("\n======================================")