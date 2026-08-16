import random

from .question_loader import load_questions


class InterviewSession:

    def __init__(self, skills):
        """
        Create a new interview session.
        """
        self.current_difficulty = "medium"

        self.pending_concept = []

        self.skills = skills

        self.questions_asked = []

        self.answers = []

        self.scores = []

        self.current_question = None

        self.pending_concepts = []


    def get_available_questions(self):
        """
        Get questions from all detected skills.
        """

        all_questions = []

        for skill in self.skills:

            questions = load_questions(skill)

            all_questions.extend(questions)

        return all_questions


    def get_question_key(self, question):
        """
        Create a unique identifier for a question.

        Topic + question ID are used together.
        """

        return (
            question.get("topic", ""),
            question.get("id")
        )


    def normalize_difficulty(self, difficulty):
        """
        Convert different difficulty formats
        into easy / medium / hard.
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

        # First question
        if not self.scores:

            return "medium"


        last_score = self.scores[-1]


        # Weak performance
        if last_score <= 4:

            return "easy"


        # Average performance
        elif last_score <= 7:

            return "medium"


        # Strong performance
        else:

            return "hard"

    def find_concept_followup(self, questions):
        """ 
        Find an unanswered question related to
        a concept that the student previously missed.
         """

        if not self.pending_concept:
            return None

        for concept in self.pending_concepts:
            concept = concept.lower().strip()

            for question in questions:
                question_key = self.get_question_key(question)

                if question_key in self.questions_asked:

                    continue 
                question_text = question.get("question", "").lower()
                expected_concept = [str(item).lower().strip()
                    for item in question.get("expected_concepts",[])
                ]

                if concept in expected_concept:
                    return question 
                if concept in question_text:
                    return question
                return None



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
        Select the next question adaptively.
        """

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


        # No questions left
        if not remaining_questions:

            return None

        followup_question = self.find_concept_followup(remaining_questions)
        if followup_question:
            self.current_question = followup_question
            question_key = self.get_question_key(followup_question)
            self.questions_asked.append(question_key)
            self.pending_concept =[]
            return followup_question


        # -----------------------------------------
        # Decide next difficulty
        # -----------------------------------------

        self.current_difficulty = (
            self.calculate_next_difficulty()
        )


        # -----------------------------------------
        # Find questions of required difficulty
        # -----------------------------------------

        matching_questions = (
            self.get_questions_by_difficulty(
                remaining_questions,
                self.current_difficulty
            )
        )


        # -----------------------------------------
        # If required difficulty doesn't exist,
        # use any remaining question
        # -----------------------------------------

        if not matching_questions:

            matching_questions = remaining_questions


        # -----------------------------------------
        # Prefer same topic as previous question
        # -----------------------------------------

        same_topic_questions = []


        if self.current_question:

            current_topic = (
                self.current_question.get("topic")
            )


            for question in matching_questions:

                if question.get("topic") == current_topic:

                    same_topic_questions.append(question)


        # -----------------------------------------
        # Select question
        # -----------------------------------------

        if same_topic_questions:

            question = random.choice(
                same_topic_questions
            )

        else:

            question = random.choice(
                matching_questions
            )


        # -----------------------------------------
        # Save current question
        # -----------------------------------------

        self.current_question = question


        question_key = self.get_question_key(
            question
        )


        self.questions_asked.append(
            question_key
        )


        return question


    def submit_answer(self, answer, score, missing_concept=None):
        """
        store student's answer,score and missing concept.
        """
        self.answers.append({
            "question":
            self.current_question,
            "answer":answer,
            "score":score,
            "missing_concept":(missing_concept or [])
        })
        self.scores.append(score)
        # save missing concept for follow-up
        self.pending_concept = (
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