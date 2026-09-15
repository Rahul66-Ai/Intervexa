import random

from .question_loader import load_questions
from .ai_question_generator import generate_ai_question


class InterviewSession:

    def __init__(self, skills):
        self.current_difficulty = "medium"

        self.skills = skills

        self.questions_asked = []

        self.answers = []

        self.scores = []

        self.current_question = None

        self.pending_concepts = []


    def get_question_key(self, question):
        """
        Create a unique identifier for a question.
        """

        return (
            question.get("topic", ""),
            question.get("id")
        )


    def normalize_difficulty(self, difficulty):
        """
        Convert difficulty into easy / medium / hard.
        """

        if not difficulty:
            return "medium"

        difficulty = str(difficulty).lower().strip()

        if difficulty in ["easy", "basic", "beginner"]:
            return "easy"

        if difficulty in ["hard", "difficult", "advanced"]:
            return "hard"

        return "medium"


    def calculate_next_difficulty(self):
        """
        Decide next question difficulty based
        on the student's previous score.
        """

        if not self.scores:
            return "medium"

        last_score = self.scores[-1]

        if last_score <= 4:
            return "easy"

        elif last_score <= 7:
            return "medium"

        else:
            return "hard"


    def get_previous_questions(self):
        """
        Return text of previously asked questions.
        """

        previous_questions = []

        for item in self.answers:

            question = item.get("question")

            if question:
                previous_questions.append(
                    question.get("question", "")
                )

        return previous_questions


    def get_ai_question(self):
        """
        Generate one question using Gemini AI.
        """

        previous_questions = self.get_previous_questions()

        question = generate_ai_question(
            skills=self.skills,
            difficulty=self.current_difficulty,
            previous_questions=previous_questions
        )

        return question


    def get_available_questions(self):
        """
        Get questions from old JSON question bank.

        This is kept as a fallback.
        """

        all_questions = []

        for skill in self.skills:

            questions = load_questions(skill)

            all_questions.extend(questions)

        return all_questions


    def get_questions_by_difficulty(
        self,
        questions,
        difficulty
    ):
        """
        Filter questions according to difficulty.
        """

        matching_questions = []

        for question in questions:

            question_difficulty = self.normalize_difficulty(
                question.get("difficulty")
            )

            if question_difficulty == difficulty:

                matching_questions.append(question)

        return matching_questions


    def get_next_question(self):
        """
        Generate the next interview question using AI.
        """

        self.current_difficulty = (
            self.calculate_next_difficulty()
        )

        try:

            question = self.get_ai_question()

            question_key = self.get_question_key(
                question
            )

            # Safety check against duplicate question IDs
            if question_key not in self.questions_asked:

                self.current_question = question

                self.questions_asked.append(
                    question_key
                )

                return question

        except Exception as error:

            print(
                "AI question generation failed:",
                error
            )


        # -----------------------------------------
        # FALLBACK TO OLD QUESTION BANK
        # -----------------------------------------

        available_questions = (
            self.get_available_questions()
        )

        remaining_questions = []

        for question in available_questions:

            question_key = self.get_question_key(
                question
            )

            if question_key not in self.questions_asked:

                remaining_questions.append(question)


        if not remaining_questions:

            return None


        matching_questions = (
            self.get_questions_by_difficulty(
                remaining_questions,
                self.current_difficulty
            )
        )


        if not matching_questions:

            matching_questions = remaining_questions


        # Random topic selection
        question = random.choice(
            matching_questions
        )


        self.current_question = question

        question_key = self.get_question_key(
            question
        )

        self.questions_asked.append(
            question_key
        )

        return question


    def submit_answer(
        self,
        answer,
        score,
        missing_concept=None
    ):
        """
        Store student's answer, score,
        and missing concepts.
        """

        self.answers.append({

            "question":
                self.current_question,

            "answer":
                answer,

            "score":
                score,

            "missing_concept":
                (missing_concept or [])
        })

        self.scores.append(score)

        self.pending_concepts = (
            missing_concept or []
        )


    def get_average_score(self):
        """
        Calculate average interview score.
        """

        if not self.scores:
            return 0

        return round(
            sum(self.scores) / len(self.scores),
            2
        )