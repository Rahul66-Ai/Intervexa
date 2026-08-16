from utils.skill import detect_skills
from utils.interview_engine import InterviewSession


def create_interview_from_resume(resume_text):
    """
    Create an interview session automatically
    from resume text.
    """

    # Step 1: Detect skills from resume
    detected_skills = detect_skills(resume_text)

    # Step 2: Check whether any skill was detected
    if not detected_skills:
        return None, []

    # Step 3: Create interview session
    session = InterviewSession(detected_skills)

    return session, detected_skills