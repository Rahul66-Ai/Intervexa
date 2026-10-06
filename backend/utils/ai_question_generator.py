import json
import os
import uuid

from google import genai


def generate_ai_question(
    skills,
    difficulty="medium",
    previous_questions=None,
    previous_topics=None,
    follow_up_concepts=None,
    previous_topic=None
):
    """
    Generate one technical interview question using Gemini AI.

    If follow_up_concepts are provided, generate a focused
    follow-up question related to the previous topic.
    Otherwise, generate a normal mixed-topic question.
    """

    previous_questions = previous_questions or []
    previous_topics = previous_topics or []
    follow_up_concepts = follow_up_concepts or []


    # ============================================================
    # VALIDATE SKILLS
    # ============================================================

    if not skills:

        raise ValueError(
            "No skills were provided."
        )


    # ============================================================
    # API KEY
    # ============================================================

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "GEMINI_API_KEY is not set in .env"
        )


    # ============================================================
    # GEMINI CLIENT
    # ============================================================

    client = genai.Client(
        api_key=api_key
    )


    # ============================================================
    # PREVIOUS QUESTIONS
    # ============================================================

    previous_questions_text = "\n".join(
        f"- {question}"
        for question in previous_questions
    )

    if not previous_questions_text:

        previous_questions_text = "None"


    # ============================================================
    # PREVIOUS TOPICS
    # ============================================================

    previous_topics_text = "\n".join(
        f"- {topic}"
        for topic in previous_topics
    )

    if not previous_topics_text:

        previous_topics_text = "None"


    # ============================================================
    # FOLLOW-UP CONCEPTS
    # ============================================================

    follow_up_concepts_text = "\n".join(
        f"- {concept}"
        for concept in follow_up_concepts
    )

    if not follow_up_concepts_text:

        follow_up_concepts_text = "None"


    # ============================================================
    # QUESTION MODE
    # ============================================================

    if follow_up_concepts and previous_topic:

        question_mode = f"""
FOLLOW-UP MODE

The candidate's previous answer was incomplete.

Previous topic:
{previous_topic}

Missing concepts:
{follow_up_concepts_text}

Generate a focused follow-up question about ONE
of these missing concepts.

The follow-up MUST remain related to the previous topic.

Do not introduce an unrelated topic.
Do not ask the exact previous question again.
"""

    else:

        question_mode = """
NORMAL INTERVIEW MODE

Generate a new question from the candidate's skills.

Prefer a skill/topic that has not been asked recently.
Avoid repeating the same topic consecutively when
other skills are available.
"""


    # ============================================================
    # AI PROMPT
    # ============================================================

    prompt = f"""
You are an experienced technical interviewer.

Candidate skills detected from the resume:
{skills}

{question_mode}

General rules:

1. Select exactly ONE skill/topic.

2. The selected topic must be present in the
candidate's skill list.

3. Difficulty must be exactly "{difficulty}".

4. Do NOT repeat any previous question.

5. The question must be suitable for a real
technical interview.

6. Test understanding and practical knowledge.

7. Do not ask multiple questions in one question.

8. Keep the question clear and concise.

9. Return ONLY valid JSON.

10. Do not use markdown.

11. Do not add explanations outside the JSON.

Previous questions:
{previous_questions_text}

Topics already asked:
{previous_topics_text}

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


    # ============================================================
    # GENERATE QUESTION
    # ============================================================

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )


    response_text = (
        interaction.output_text
        .strip()
    )


    # ============================================================
    # REMOVE MARKDOWN CODE FENCES
    # ============================================================

    if response_text.startswith("```"):

        response_text = (
            response_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )


    # ============================================================
    # PARSE JSON
    # ============================================================

    try:

        question_data = json.loads(
            response_text
        )

    except json.JSONDecodeError:

        raise ValueError(
            "Gemini returned invalid JSON:\n"
            + response_text
        )


    # ============================================================
    # REQUIRED FIELDS
    # ============================================================

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


    # ============================================================
    # VALIDATE QUESTION
    # ============================================================

    if not question_data["question"]:

        raise ValueError(
            "Gemini returned an empty question."
        )


    if not question_data["topic"]:

        raise ValueError(
            "Gemini returned an empty topic."
        )


    # ============================================================
    # GENERATE ID IF NEEDED
    # ============================================================

    if not question_data["id"]:

        question_data["id"] = str(
            uuid.uuid4()
        )


    # ============================================================
    # RETURN QUESTION
    # ============================================================

    return question_data