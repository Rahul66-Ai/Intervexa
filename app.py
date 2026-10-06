import streamlit as st
from pathlib import Path
import tempfile
import speech_recognition as sr
import subprocess

from streamlit_mic_recorder import mic_recorder

from backend.utils.resume_parser import extract_resume_text
from backend.utils.skill import detect_skills, detect_ai_skills
from backend.utils.interview_engine import InterviewSession
from backend.utils.answer_evaluator import evaluate_answer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Intervexa",
    page_icon="🎤",
    layout="centered"
)


# ============================================================
# VOICE FUNCTION
# ============================================================

def speak_text(text):
    """
    Speak text using Windows built-in Speech Synthesizer.
    """

    if not text:
        return

    safe_text = str(text).replace(
        "'",
        "''"
    )

    command = (
        "Add-Type -AssemblyName System.Speech; "
        "$speaker = New-Object "
        "System.Speech.Synthesis.SpeechSynthesizer; "
        f"$speaker.Speak('{safe_text}')"
    )

    subprocess.Popen(
        [
            "powershell",
            "-Command",
            command
        ]
    )


# ============================================================
# SESSION STATE
# ============================================================

if "session" not in st.session_state:
    st.session_state.session = None


if "skills" not in st.session_state:
    st.session_state.skills = []


if "question" not in st.session_state:
    st.session_state.question = None


if "interview_started" not in st.session_state:
    st.session_state.interview_started = False


if "question_number" not in st.session_state:
    st.session_state.question_number = 0


if "completed" not in st.session_state:
    st.session_state.completed = False


if "pending_voice" not in st.session_state:
    st.session_state.pending_voice = None


# ============================================================
# SPEAK PENDING VOICE ONCE
# ============================================================

if st.session_state.pending_voice:

    text_to_speak = (
        st.session_state.pending_voice
    )

    st.session_state.pending_voice = None

    speak_text(
        text_to_speak
    )


# ============================================================
# TITLE
# ============================================================

st.title("🎤 Intervexa")

st.subheader(
    "AI Technical Interviewer"
)

st.write(
    "Upload your resume and Intervexa will "
    "conduct a technical interview based on "
    "your detected skills."
)


# ============================================================
# RESUME UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf", "docx"]
)


# ============================================================
# START INTERVIEW
# ============================================================

if (
    uploaded_file
    and not st.session_state.interview_started
):

    if st.button(
        "🚀 Start Interview"
    ):

        with st.spinner(
            "Reading your resume..."
        ):

            # ------------------------------------------------
            # CREATE TEMPORARY FILE
            # ------------------------------------------------

            suffix = Path(
                uploaded_file.name
            ).suffix

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getbuffer()
                )

                temp_path = temp_file.name


            # ------------------------------------------------
            # EXTRACT RESUME TEXT
            # ------------------------------------------------

            resume_text = extract_resume_text(
                temp_path
            )


            # ------------------------------------------------
            # AI SKILL DETECTION
            # ------------------------------------------------

            try:

                skills = detect_ai_skills(
                    resume_text
                )

            except Exception as e:

                st.warning(
                    "AI skill detection failed. "
                    "Using basic skill detection instead."
                )

                print(
                    "AI skill detection error:",
                    e
                )

                skills = detect_skills(
                    resume_text
                )


        # ----------------------------------------------------
        # NO SKILLS FOUND
        # ----------------------------------------------------

        if not skills:

            st.error(
                "No technical skills "
                "were detected in your resume."
            )


        # ----------------------------------------------------
        # SKILLS FOUND
        # ----------------------------------------------------

        else:

            st.session_state.skills = skills


            # ------------------------------------------------
            # CREATE INTERVIEW SESSION
            # ------------------------------------------------

            st.session_state.session = (
                InterviewSession(
                    skills
                )
            )


            # ------------------------------------------------
            # GET FIRST QUESTION
            # ------------------------------------------------

            first_question = (
                st.session_state.session
                .get_next_question()
            )


            if first_question:

                st.session_state.question = (
                    first_question
                )

                st.session_state.question_number = 1

                st.session_state.interview_started = True

                st.session_state.completed = False


                # ------------------------------------------------
                # QUEUE FIRST QUESTION FOR VOICE
                # ------------------------------------------------

                st.session_state.pending_voice = (
                    first_question["question"]
                )

                st.rerun()

            else:

                st.error(
                    "Could not generate the first interview question."
                )


# ============================================================
# SHOW DETECTED SKILLS
# ============================================================

if st.session_state.interview_started:

    st.success(
        "Resume processed successfully! ✅"
    )


    st.write(
        "### Skills detected from your resume:"
    )


    for skill in st.session_state.skills:

        st.write(
            f"✓ {skill}"
        )


# ============================================================
# INTERVIEW SCREEN
# ============================================================

if (
    st.session_state.interview_started
    and st.session_state.question is not None
    and not st.session_state.completed
):

    question = (
        st.session_state.question
    )


    st.divider()


    # ========================================================
    # QUESTION NUMBER
    # ========================================================

    st.write(
        f"### Question "
        f"{st.session_state.question_number}"
    )


    # ========================================================
    # FOLLOW-UP INDICATOR
    # ========================================================

    if (
        st.session_state.session
        and st.session_state.session.follow_up_pending
    ):

        st.warning(
            "🔄 Follow-up Question"
        )


    # ========================================================
    # TOPIC
    # ========================================================

    st.write(
        f"**Topic:** "
        f"{question['topic']}"
    )


    # ========================================================
    # DIFFICULTY
    # ========================================================

    st.write(
        f"**Difficulty:** "
        f"{question['difficulty']}"
    )


    # ========================================================
    # QUESTION
    # ========================================================

    st.info(
        question["question"]
    )


    # ========================================================
    # MANUAL REPEAT BUTTON
    # ========================================================

    if st.button(
        "🔊 Hear Question Again"
    ):

        speak_text(
            question["question"]
        )


    # ========================================================
    # END INTERVIEW BUTTON
    # ========================================================

    if st.button(
        "🛑 End Interview"
    ):

        st.session_state.completed = True

        st.session_state.pending_voice = (
            "The interview has been ended. "
            "Here is your final result."
        )

        st.rerun()


    # ========================================================
    # VOICE ANSWER
    # ========================================================

    st.write(
        "### 🎙️ Speak Your Answer"
    )


    audio = mic_recorder(
        start_prompt="🎤 Start Speaking",
        stop_prompt="⏹️ Stop Recording",
        just_once=False,
        use_container_width=True,
        format="wav"
    )


    # ========================================================
    # TEXT ANSWER
    # ========================================================

    answer = st.text_area(
        "Your Answer",
        height=150,
        placeholder="Type your answer here..."
    )


    # ========================================================
    # SPEECH TO TEXT
    # ========================================================

    if audio:

        recognizer = (
            sr.Recognizer()
        )


        try:

            # ------------------------------------------------
            # SAVE AUDIO
            # ------------------------------------------------

            with open(
                "temp_audio.wav",
                "wb"
            ) as file:

                file.write(
                    audio["bytes"]
                )


            # ------------------------------------------------
            # READ AUDIO
            # ------------------------------------------------

            with sr.AudioFile(
                "temp_audio.wav"
            ) as source:

                recorded_audio = (
                    recognizer.record(
                        source
                    )
                )


            # ------------------------------------------------
            # GOOGLE SPEECH RECOGNITION
            # ------------------------------------------------

            voice_text = (
                recognizer.recognize_google(
                    recorded_audio
                )
            )


            # ------------------------------------------------
            # SHOW CONVERTED TEXT
            # ------------------------------------------------

            st.success(
                "Voice converted to text! ✅"
            )


            st.write(
                f"**You said:** "
                f"{voice_text}"
            )


            # ------------------------------------------------
            # USE VOICE TEXT AS ANSWER
            # ------------------------------------------------

            answer = voice_text


        except sr.UnknownValueError:

            st.warning(
                "I could not understand your voice."
            )


        except sr.RequestError:

            st.error(
                "Speech recognition service "
                "is unavailable."
            )


        except Exception as e:

            st.error(
                f"Voice processing error: {e}"
            )


    # ========================================================
    # SUBMIT ANSWER
    # ========================================================

    if st.button(
        "Submit Answer"
    ):

        # ----------------------------------------------------
        # CHECK EMPTY ANSWER
        # ----------------------------------------------------

        if not answer.strip():

            st.warning(
                "Please enter an answer first."
            )


        else:

            # ------------------------------------------------
            # EVALUATE ANSWER
            # ------------------------------------------------

            result = evaluate_answer(
                question,
                answer
            )


            # ------------------------------------------------
            # SAVE ANSWER + SCORE
            # ------------------------------------------------

            st.session_state.session.submit_answer(
                answer,
                result["score"],
                result["missing_concepts"]
            )


            # =================================================
            # SCORE
            # =================================================

            st.success(
                f"Score: "
                f"{result['score']}/10"
            )


            # =================================================
            # FEEDBACK
            # =================================================

            st.write(
                "### Feedback"
            )


            st.write(
                result["feedback"]
            )


            # =================================================
            # MATCHED CONCEPTS
            # =================================================

            st.write(
                "### Concepts Covered"
            )


            if result["matched_concepts"]:

                for concept in (
                    result["matched_concepts"]
                ):

                    st.write(
                        f"✅ {concept}"
                    )

            else:

                st.write(
                    "None"
                )


            # =================================================
            # MISSING CONCEPTS
            # =================================================

            st.write(
                "### Missing Concepts"
            )


            if result["missing_concepts"]:

                for concept in (
                    result["missing_concepts"]
                ):

                    st.write(
                        f"❌ {concept}"
                    )

            else:

                st.write(
                    "None"
                )


            # =================================================
            # PREPARE VOICE FEEDBACK
            # =================================================

            score = result["score"]


            if score >= 8:

                voice_feedback = (
                    f"Good answer. "
                    f"Your score is "
                    f"{score} out of 10."
                )


            elif score >= 5:

                voice_feedback = (
                    f"Fair answer. "
                    f"Your score is "
                    f"{score} out of 10. "
                    f"Try to explain the "
                    f"concepts more clearly."
                )


            else:

                voice_feedback = (
                    f"Your score is "
                    f"{score} out of 10. "
                    f"Please review the "
                    f"important concepts."
                )


            # =================================================
            # CHECK WHETHER FOLLOW-UP WAS CREATED
            # =================================================

            follow_up_was_requested = (
                st.session_state.session.follow_up_pending
            )


            # =================================================
            # GET NEXT AI QUESTION
            # =================================================

            next_question = (
                st.session_state.session
                .get_next_question()
            )


            # ------------------------------------------------
            # SAFETY CHECK
            # ------------------------------------------------

            if not next_question:

                st.warning(
                    "No more interview questions "
                    "could be generated."
                )

                st.session_state.completed = True

                st.session_state.pending_voice = (
                    voice_feedback
                    + " "
                    + "The interview has ended."
                )

                st.rerun()


            else:

                st.session_state.question = (
                    next_question
                )


                st.session_state.question_number += 1


                # =================================================
                # ONE COMBINED VOICE
                # =================================================

                next_question_text = (
                    next_question["question"]
                )


                if follow_up_was_requested:

                    combined_voice = (
                        voice_feedback
                        + " "
                        + "Let's clarify that concept "
                        + "with a follow-up question. "
                        + next_question_text
                    )

                else:

                    combined_voice = (
                        voice_feedback
                        + " "
                        + "Now, next question. "
                        + next_question_text
                    )


                # ------------------------------------------------
                # QUEUE ONLY ONE VOICE
                # ------------------------------------------------

                st.session_state.pending_voice = (
                    combined_voice
                )


                # ------------------------------------------------
                # RERUN
                # ------------------------------------------------

                st.rerun()


# ============================================================
# FINAL REPORT
# ============================================================

if st.session_state.completed:

    st.divider()


    st.header(
        "🎯 Interview Completed"
    )


    # ------------------------------------------------
    # SESSION
    # ------------------------------------------------

    session = (
        st.session_state.session
    )


    # ------------------------------------------------
    # AVERAGE SCORE
    # ------------------------------------------------

    if session and session.scores:

        st.metric(
            "Average Score",
            f"{session.get_average_score()}/10"
        )


    # ------------------------------------------------
    # QUESTION SCORES
    # ------------------------------------------------

    if session and session.scores:

        st.write(
            "### Question Scores"
        )


        for index, score in enumerate(
            session.scores,
            start=1
        ):

            st.write(
                f"Question {index}: "
                f"{score}/10"
            )


    # ------------------------------------------------
    # COMPLETION MESSAGE
    # ------------------------------------------------

    st.success(
        "Thank you for using Intervexa! 🎤"
    )


    # ------------------------------------------------
    # NEW INTERVIEW
    # ------------------------------------------------

    if st.button(
        "🔄 Start New Interview"
    ):

        st.session_state.clear()

        st.rerun()