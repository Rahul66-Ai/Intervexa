import re


SKILLS = {
    "Python": [
        "python",
        "python programming"
    ],

    "C": [
        "c programming",
        "c language"
    ],

    "C++": [
        "c++",
        "cpp",
        "c plus plus"
    ],

    "Java": [
        "java",
        "java programming"
    ],

    "HTML": [
        "html",
        "html5"
    ],

    "CSS": [
        "css",
        "css3"
    ],

    "JavaScript": [
        "javascript",
        "js"
    ],

    "Data Structures": [
        "data structures",
        "data structure",
        "dsa"
    ],

    "Computer Fundamentals": [
        "computer fundamentals",
        "computer basics",
        "computer science fundamentals"
    ]
}


def detect_skills(resume_text):
    """
    Detect predefined skills from resume text.
    """

    text = resume_text.lower()

    detected_skills = []

    for skill, keywords in SKILLS.items():

        for keyword in keywords:

            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, text):
                detected_skills.append(skill)
                break

    return detected_skills