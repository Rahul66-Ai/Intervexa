from pathlib import Path

from utils.resume_parser import extract_resume_text
from utils.skill import detect_skills
from utils.interview_engine import InterviewSession
from utils.answer_evaluator import evaluate_answer


TOTAL_QUESTIONS = 5


def start_interview(resume_path):

    print("\n==========================================")
    print("              INTERVEXA")
    print("==========================================")

    print("\nReading resume...")

    # ---------------------------------------
    # STEP 1: Extract resume text
    # ---------------------------------------

    resume_text = extract_resume_text(resume_path)

    if not resume_text.strip():

        print("\nCould not extract any text from the resume.")

        return


    print("Resume successfully read.")


    # ---------------------------------------
    # STEP 2: Detect skills
    # ---------------------------------------

    skills = detect_skills(resume_text)


    if not skills:

        print("\nNo supported skills were detected.")
        print("\nSupported skills are:")

        print("""
Python
C
C++
Java
HTML
CSS
JavaScript
Data Structures
Computer Fundamentals
        """)

        return


    # ---------------------------------------
    # STEP 3: Show detected skills
    # ---------------------------------------

    print("\n------------------------------------------")
    print("SKILLS DETECTED FROM YOUR RESUME")
    print("------------------------------------------")

    for skill in skills:

        print("✓", skill)


    # ---------------------------------------
    # STEP 4: Create interview session
    # ---------------------------------------

    session = InterviewSession(skills)


    print("\n------------------------------------------")
    print("INTERVIEW STARTING")
    print("------------------------------------------")


    # ---------------------------------------
    # STEP 5: Ask questions
    # ---------------------------------------

    for question_number in range(1, TOTAL_QUESTIONS + 1):

        question = session.get_next_question()


        if question is None:

            print("\nNo more questions available.")

            break


        print("\n==========================================")
        print(
            f"QUESTION {question_number}/{TOTAL_QUESTIONS}"
        )
        print("==========================================")


        print("\nTopic:")
        print(question["topic"])


        print("\nDifficulty:")
        print(question["difficulty"])


        print("\nQuestion:")
        print(question["question"])


        print("\n------------------------------------------")


        student_answer = input("Your Answer: ")


        # -----------------------------------
        # STEP 6: Evaluate answer
        # -----------------------------------

        result = evaluate_answer(
            question,
            student_answer
        )


        # Save answer and score
        session.submit_answer(
            student_answer,
            result["score"],
            result["missing_concepts"]
        )


        # -----------------------------------
        # STEP 7: Show evaluation
        # -----------------------------------

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


    # ---------------------------------------
    # STEP 8: Final Report
    # ---------------------------------------

    print("\n\n==========================================")
    print("          INTERVIEW COMPLETED")
    print("==========================================")


    print("\nQuestions Attempted:")

    print(len(session.answers))


    print("\nIndividual Scores:")


    for index, score in enumerate(
        session.scores,
        start=1
    ):

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


if __name__ == "__main__":

    resume_path = input(
        "\nEnter resume file path: "
    ).strip()


    if not Path(resume_path).exists():

        print("\nERROR: Resume file not found.")

    else:

        start_interview(resume_path)