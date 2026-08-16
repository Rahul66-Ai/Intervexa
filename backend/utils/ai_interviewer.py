import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")


if not api_key:
    raise ValueError(
        "OPENAI_API_KEY is not set. "
        "Please add it to the .env file."
    )


client = OpenAI(api_key=api_key)


def ask_ai(prompt):
    """
    Send a prompt to the AI interviewer
    and return the response.
    """

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text