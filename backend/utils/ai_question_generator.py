import json
import os
import uuid

from google import genai


def generate_ai_question(
    skills,
    difficulty="medium",
    previous_questions=None
):
    """
    Generate one interview question using Gemini AI.
    """

    previous_questions = previous_questions or []

    if not skills:
        raise ValueError("No skills were provided.")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set in .env"
        )

    client = genai.Client(api_key=api_key)

    previous_text = "\n".join(
        f"- {question}"
        for question in previous_questions
    )

    if not previous_text:
        previous_text = "None"

    prompt = f"""
You are an experienced technical interviewer.

Candidate skills detected from the resume:
{skills}

Generate ONE technical interview question.

Rules:
1. Select exactly ONE skill from the candidate's skill list.
2. Do NOT ask about any skill that is not in the list.
3. Difficulty must be exactly "{difficulty}".
4. Do NOT repeat any previous question.
5. The question must be suitable for a technical interview.
6. Test understanding and practical knowledge.
7. Return ONLY valid JSON.
8. Do not use markdown.
9. Do not add explanations outside the JSON.

Previous questions:
{previous_text}

Return exactly this structure:

{{
    "id": "unique_id",
    "topic": "selected skill",
    "question": "interview question",
    "difficulty": "{difficulty}",
    "expected_concepts": [
        "concept 1",
        "concept 2"
    ]
}}
"""

    # Generate question using Gemini Interactions API
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    response_text = interaction.output_text.strip()

    # Remove accidental markdown code fences
    if response_text.startswith("```"):
        response_text = response_text.replace(
            "```json", ""
        ).replace("```", "").strip()

    try:
        question_data = json.loads(response_text)

    except json.JSONDecodeError:
        raise ValueError(
            "Gemini returned invalid JSON:\n"
            + response_text
        )

    # Check required fields
    required_fields = [
        "id",
        "topic",
        "question",
        "difficulty",
        "expected_concepts"
    ]

    for field in required_fields:

        if field not in question_data:

            raise ValueError(
                f"Missing field from Gemini response: {field}"
            )

    # Generate ID if Gemini did not provide one
    if not question_data["id"]:

        question_data["id"] = str(uuid.uuid4())

    return question_data