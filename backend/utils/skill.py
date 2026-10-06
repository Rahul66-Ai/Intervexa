import re
import os
import json

from google import genai


# ============================================================
# PREDEFINED SKILLS
# ============================================================

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


# ============================================================
# PREDEFINED SKILL DETECTION
# ============================================================

def detect_skills(resume_text):
    """
    Detect predefined skills from resume text.
    """

    text = resume_text.lower()

    detected_skills = []

    for skill, keywords in SKILLS.items():

        for keyword in keywords:

            pattern = (
                r"\b"
                + re.escape(keyword)
                + r"\b"
            )

            if re.search(pattern, text):

                detected_skills.append(
                    skill
                )

                break

    return detected_skills


# ============================================================
# AI SKILL DETECTION
# ============================================================

def detect_ai_skills(resume_text):
    """
    Detect technical skills from resume using Gemini AI.
    """

    if not resume_text:
        return []

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "GEMINI_API_KEY is not set in .env"
        )

    client = genai.Client(
        api_key=api_key
    )

    prompt = f"""
You are a technical resume skill analyzer.

Analyze the following resume text and identify
the technical skills mentioned in it.

Resume:
{resume_text}

Rules:

1. Return only technical skills.
2. Include programming languages, frameworks,
   libraries, databases, tools, cloud technologies,
   AI/ML technologies, and technical concepts.
3. Do not include soft skills.
4. Do not invent skills that are not present.
5. Avoid duplicate skills.
6. Return ONLY valid JSON.
7. Do not use markdown.
8. Keep skill names short and clear.

Return exactly this format:

{{
    "skills": [
        "Python",
        "SQL",
        "React",
        "Machine Learning"
    ]
}}
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    response_text = (
        interaction.output_text
        .strip()
    )

    # --------------------------------------------------------
    # Remove accidental markdown code fences
    # --------------------------------------------------------

    if response_text.startswith("```"):

        response_text = (
            response_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    # --------------------------------------------------------
    # Parse JSON
    # --------------------------------------------------------

    try:

        result = json.loads(
            response_text
        )

    except json.JSONDecodeError:

        raise ValueError(
            "Gemini returned invalid JSON:\n"
            + response_text
        )

    # --------------------------------------------------------
    # Validate skills
    # --------------------------------------------------------

    skills = result.get(
        "skills",
        []
    )

    if not isinstance(
        skills,
        list
    ):

        raise ValueError(
            "Gemini returned invalid skills format."
        )

    # --------------------------------------------------------
    # Remove empty / duplicate values
    # --------------------------------------------------------

    cleaned_skills = []

    for skill in skills:

        if not isinstance(
            skill,
            str
        ):
            continue

        skill = skill.strip()

        if not skill:
            continue

        if skill not in cleaned_skills:

            cleaned_skills.append(
                skill
            )

    return cleaned_skills