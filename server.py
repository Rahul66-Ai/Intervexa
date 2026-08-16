from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
import tempfile

from backend.utils.resume_parser import extract_resume_text
from backend.utils.skill import detect_skills
from backend.utils.interview_engine import InterviewSession
from backend.utils.answer_evaluator import evaluate_answer


# ============================================================
# APP CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path=""
)

CORS(app)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "success",
        "message": "Intervexa backend is running"
    })


# ============================================================
# START INTERVIEW
# ============================================================

@app.route("/api/start-interview", methods=["POST"])
def start_interview():

    try:

        # ----------------------------------------------------
        # CHECK FILE
        # ----------------------------------------------------

        if "resume" not in request.files:

            return jsonify({
                "status": "error",
                "message": "Resume file is required."
            }), 400


        uploaded_file = request.files["resume"]


        if uploaded_file.filename == "":

            return jsonify({
                "status": "error",
                "message": "Please select a resume."
            }), 400


        # ----------------------------------------------------
        # SAVE TEMPORARY RESUME
        # ----------------------------------------------------

        suffix = Path(
            uploaded_file.filename
        ).suffix


        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            uploaded_file.save(
                temp_file.name
            )

            temp_path = temp_file.name


        # ----------------------------------------------------
        # EXTRACT RESUME TEXT
        # ----------------------------------------------------

        resume_text = extract_resume_text(
            temp_path
        )


        # ----------------------------------------------------
        # DETECT SKILLS
        # ----------------------------------------------------

        skills = detect_skills(
            resume_text
        )


        if not skills:

            return jsonify({
                "status": "error",
                "message": (
                    "No supported technical "
                    "skills were detected."
                )
            }), 400


        # ----------------------------------------------------
        # CREATE INTERVIEW SESSION
        # ----------------------------------------------------

        session = InterviewSession(
            skills
        )


        # ----------------------------------------------------
        # GET FIRST QUESTION
        # ----------------------------------------------------

        question = session.get_next_question()


        if question is None:

            return jsonify({
                "status": "error",
                "message": (
                    "No interview questions "
                    "are available."
                )
            }), 500


        # ----------------------------------------------------
        # STORE SESSION
        # ----------------------------------------------------

        # Simple in-memory session storage.
        # This is enough for our minor project.

        session_id = str(
            id(session)
        )


        sessions[session_id] = {
            "session": session,
            "skills": skills,
            "question_number": 1
        }


        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "status": "success",

            "session_id": session_id,

            "skills": skills,

            "question_number": 1,

            "question": {
                "id": question.get("id"),
                "question": question.get("question"),
                "difficulty": question.get("difficulty"),
                "topic": question.get("topic")
            }

        })


    except Exception as e:

        print(
            "START INTERVIEW ERROR:",
            e
        )

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ============================================================
# SUBMIT ANSWER
# ============================================================

@app.route("/api/submit-answer", methods=["POST"])
def submit_answer():

    try:

        data = request.get_json()


        if not data:

            return jsonify({
                "status": "error",
                "message": "Invalid request."
            }), 400


        session_id = data.get(
            "session_id"
        )


        answer = data.get(
            "answer",
            ""
        )


        if not session_id:

            return jsonify({
                "status": "error",
                "message": "Session ID is required."
            }), 400


        if not answer.strip():

            return jsonify({
                "status": "error",
                "message": "Answer cannot be empty."
            }), 400


        # ----------------------------------------------------
        # FIND SESSION
        # ----------------------------------------------------

        session_data = sessions.get(
            session_id
        )


        if not session_data:

            return jsonify({
                "status": "error",
                "message": "Interview session not found."
            }), 404


        session = session_data["session"]


        # ----------------------------------------------------
        # CURRENT QUESTION
        # ----------------------------------------------------

        current_question = (
            session.current_question
        )


        if current_question is None:

            return jsonify({
                "status": "error",
                "message": "No active question."
            }), 400


        # ----------------------------------------------------
        # EVALUATE ANSWER
        # ----------------------------------------------------

        result = evaluate_answer(
            current_question,
            answer
        )


        # ----------------------------------------------------
        # SAVE ANSWER
        # ----------------------------------------------------

        session.submit_answer(
            answer,
            result["score"],
            result["missing_concepts"]
        )


        # ----------------------------------------------------
        # QUESTION NUMBER
        # ----------------------------------------------------

        question_number = (
            session_data["question_number"]
        )


        TOTAL_QUESTIONS = 5


        # ----------------------------------------------------
        # CHECK COMPLETION
        # ----------------------------------------------------

        if question_number >= TOTAL_QUESTIONS:

            return jsonify({

                "status": "success",

                "completed": True,

                "score": result["score"],

                "feedback": result["feedback"],

                "matched_concepts":
                    result["matched_concepts"],

                "missing_concepts":
                    result["missing_concepts"],

                "average_score":
                    session.get_average_score(),

                "message":
                    "Interview completed successfully."

            })


        # ----------------------------------------------------
        # NEXT QUESTION
        # ----------------------------------------------------

        next_question = (
            session.get_next_question()
        )


        session_data["question_number"] += 1


        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "status": "success",

            "completed": False,

            "score": result["score"],

            "feedback": result["feedback"],

            "matched_concepts":
                result["matched_concepts"],

            "missing_concepts":
                result["missing_concepts"],

            "question_number":
                session_data["question_number"],

            "question": {

                "id":
                    next_question.get("id"),

                "question":
                    next_question.get("question"),

                "difficulty":
                    next_question.get("difficulty"),

                "topic":
                    next_question.get("topic")

            }

        })


    except Exception as e:

        print(
            "SUBMIT ANSWER ERROR:",
            e
        )

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ============================================================
# IN-MEMORY SESSION STORAGE
# ============================================================

sessions = {}


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print()
    print(
        "========================================"
    )

    print(
        "       INTERVEXA BACKEND SERVER"
    )

    print(
        "========================================"
    )

    print(
        "Server running at:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print(
        "========================================"
    )

    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )