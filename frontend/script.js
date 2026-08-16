// ============================================================
// INTERVEXA FRONTEND
// ============================================================

let sessionId = null;

let currentQuestion = null;

let isRecording = false;

let recognition = null;


// ============================================================
// DOM ELEMENTS
// ============================================================

const resumeInput =
    document.getElementById("resumeInput");

const fileName =
    document.getElementById("fileName");

const startButton =
    document.getElementById("startButton");

const loading =
    document.getElementById("loading");

const errorMessage =
    document.getElementById("errorMessage");


// ============================================================
// FILE SELECTION
// ============================================================

if (resumeInput) {

    resumeInput.addEventListener(
        "change",
        function () {

            if (!resumeInput.files.length) {

                fileName.textContent =
                    "No file selected";

                startButton.disabled = true;

                return;
            }


            const file =
                resumeInput.files[0];


            fileName.textContent =
                file.name;


            startButton.disabled = false;

        }
    );

}


// ============================================================
// ERROR FUNCTION
// ============================================================

function showError(message) {

    if (!errorMessage) {
        alert(message);
        return;
    }


    errorMessage.textContent =
        message;


    errorMessage.classList.remove(
        "hidden"
    );
}


// ============================================================
// HIDE ERROR
// ============================================================

function hideError() {

    if (!errorMessage) {
        return;
    }


    errorMessage.classList.add(
        "hidden"
    );

}


// ============================================================
// LOADING
// ============================================================

function setLoading(status) {

    if (!loading) {
        return;
    }


    if (status) {

        loading.classList.remove(
            "hidden"
        );

    } else {

        loading.classList.add(
            "hidden"
        );

    }

}


// ============================================================
// START INTERVIEW
// ============================================================

if (startButton) {

    startButton.addEventListener(
        "click",
        async function () {

            hideError();


            if (!resumeInput.files.length) {

                showError(
                    "Please select your resume first."
                );

                return;
            }


            const file =
                resumeInput.files[0];


            const formData =
                new FormData();


            formData.append(
                "resume",
                file
            );


            startButton.disabled = true;

            setLoading(true);


            try {

                const response =
                    await fetch(
                        "/api/start-interview",
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.message ||
                        "Unable to start interview."
                    );

                }


                // --------------------------------------------
                // SAVE SESSION
                // --------------------------------------------

                sessionId =
                    data.session_id;


                currentQuestion =
                    data.question;


                // --------------------------------------------
                // SHOW INTERVIEW PAGE
                // --------------------------------------------

                showInterviewScreen(
                    data
                );


                // --------------------------------------------
                // SPEAK FIRST QUESTION
                // --------------------------------------------

                speakQuestion(
                    currentQuestion.question
                );


            }

            catch (error) {

                console.error(
                    error
                );


                showError(
                    error.message
                );


                startButton.disabled =
                    false;

            }

            finally {

                setLoading(false);

            }

        }
    );

}


// ============================================================
// TEXT TO SPEECH
// ============================================================

function speakQuestion(text) {

    if (!text) {
        return;
    }


    // Stop previous speech

    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(
            text
        );


    speech.rate = 0.9;

    speech.pitch = 1;

    speech.volume = 1;


    window.speechSynthesis.speak(
        speech
    );

}


// ============================================================
// INTERVIEW SCREEN
// ============================================================

function showInterviewScreen(data) {

    document.body.innerHTML = `

        <header class="navbar">

            <div class="nav-container">

                <a
                    href="/"
                    class="logo"
                >

                    <span class="logo-icon">
                        🎤
                    </span>

                    Intervexa

                </a>


                <div class="interview-header">

                    <span>
                        AI Technical Interview
                    </span>

                </div>

            </div>

        </header>


        <main class="interview-page">

            <div class="interview-container">


                <!-- ======================================
                     PROGRESS
                ======================================= -->

                <div class="interview-top">

                    <div>

                        <span class="small-label">
                            TECHNICAL INTERVIEW
                        </span>

                        <h1>
                            Question
                            <span id="questionNumber">
                                ${data.question_number}
                            </span>
                            / 5
                        </h1>

                    </div>


                    <div class="skill-box">

                        <span>
                            Detected Skills
                        </span>

                        <strong>
                            ${data.skills.join(", ")}
                        </strong>

                    </div>

                </div>


                <!-- ======================================
                     QUESTION CARD
                ======================================= -->

                <section class="question-card">

                    <div class="question-meta">

                        <span>
                            📚 ${data.question.topic}
                        </span>

                        <span>
                            ⚡ ${data.question.difficulty}
                        </span>

                    </div>


                    <h2 id="questionText">

                        ${data.question.question}

                    </h2>


                    <button
                        id="repeatQuestion"
                        class="secondary-button"
                    >
                        🔊 Hear Question Again
                    </button>

                </section>


                <!-- ======================================
                     ANSWER CARD
                ======================================= -->

                <section class="answer-card">

                    <div class="answer-heading">

                        <div>

                            <span class="small-label">
                                YOUR ANSWER
                            </span>

                            <h2>
                                Explain your answer
                            </h2>

                        </div>


                        <div
                            id="recordingStatus"
                            class="recording-status hidden"
                        >
                            🔴 Recording...
                        </div>

                    </div>


                    <textarea
                        id="answerInput"
                        class="answer-input"
                        placeholder="Type your answer here..."
                    ></textarea>


                    <div class="answer-actions">

                        <button
                            id="voiceButton"
                            class="voice-button"
                        >
                            🎙️ Start Speaking
                        </button>


                        <button
                            id="submitButton"
                            class="primary-button"
                        >
                            Submit Answer →
                        </button>

                    </div>


                    <p class="voice-help">

                        You can type your answer or
                        use your microphone.

                    </p>

                </section>


                <!-- ======================================
                     RESULT
                ======================================= -->

                <section
                    id="resultSection"
                    class="result-section hidden"
                >

                    <div
                        id="scoreBox"
                        class="score-box"
                    ></div>


                    <div class="feedback-box">

                        <span class="small-label">
                            AI FEEDBACK
                        </span>

                        <h3>
                            Feedback
                        </h3>

                        <p id="feedbackText"></p>

                    </div>


                    <div class="concept-grid">


                        <div class="concept-card">

                            <h3>
                                ✅ Matched Concepts
                            </h3>

                            <div
                                id="matchedConcepts"
                            ></div>

                        </div>


                        <div class="concept-card">

                            <h3>
                                ❌ Missing Concepts
                            </h3>

                            <div
                                id="missingConcepts"
                            ></div>

                        </div>


                    </div>


                    <button
                        id="nextButton"
                        class="primary-button next-button"
                    >
                        Next Question →
                    </button>

                </section>


            </div>

        </main>

    `;


    // ========================================================
    // EVENTS
    // ========================================================

    document
        .getElementById("repeatQuestion")
        .addEventListener(
            "click",
            function () {

                speakQuestion(
                    currentQuestion.question
                );

            }
        );


    document
        .getElementById("voiceButton")
        .addEventListener(
            "click",
            toggleVoice
        );


    document
        .getElementById("submitButton")
        .addEventListener(
            "click",
            submitAnswer
        );

}


// ============================================================
// VOICE RECOGNITION
// ============================================================

function setupRecognition() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        return null;

    }


    const recognizer =
        new SpeechRecognition();


    recognizer.continuous = false;

    recognizer.interimResults = false;

    recognizer.lang = "en-US";


    recognizer.onstart =
        function () {

            isRecording = true;

            updateRecordingUI(true);

        };


    recognizer.onresult =
        function (event) {

            const text =
                event.results[0][0].transcript;


            const answerInput =
                document.getElementById(
                    "answerInput"
                );


            if (answerInput) {

                answerInput.value =
                    text;

            }

        };


    recognizer.onerror =
        function (event) {

            console.error(
                "Speech recognition error:",
                event.error
            );


            updateRecordingUI(false);

        };


    recognizer.onend =
        function () {

            isRecording = false;

            updateRecordingUI(false);

        };


    return recognizer;

}


recognition =
    setupRecognition();


// ============================================================
// VOICE BUTTON
// ============================================================

function toggleVoice() {

    if (!recognition) {

        alert(
            "Voice recognition is not supported in this browser. Please use Chrome or Edge."
        );

        return;

    }


    if (isRecording) {

        recognition.stop();

        return;

    }


    recognition.start();

}


// ============================================================
// RECORDING UI
// ============================================================

function updateRecordingUI(recording) {

    const button =
        document.getElementById(
            "voiceButton"
        );


    const status =
        document.getElementById(
            "recordingStatus"
        );


    if (!button || !status) {
        return;
    }


    if (recording) {

        button.textContent =
            "⏹️ Stop Speaking";


        status.classList.remove(
            "hidden"
        );

    }

    else {

        button.textContent =
            "🎙️ Start Speaking";


        status.classList.add(
            "hidden"
        );

    }

}


// ============================================================
// SUBMIT ANSWER
// ============================================================

async function submitAnswer() {

    const answerInput =
        document.getElementById(
            "answerInput"
        );


    const submitButton =
        document.getElementById(
            "submitButton"
        );


    const answer =
        answerInput.value.trim();


    if (!answer) {

        alert(
            "Please enter or speak your answer first."
        );

        return;

    }


    submitButton.disabled =
        true;


    submitButton.textContent =
        "Evaluating...";


    try {

        const response =
            await fetch(
                "/api/submit-answer",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        session_id:
                            sessionId,

                        answer:
                            answer

                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.message ||
                "Unable to submit answer."
            );

        }


        showResult(
            data
        );


    }

    catch (error) {

        console.error(
            error
        );


        alert(
            error.message
        );


        submitButton.disabled =
            false;


        submitButton.textContent =
            "Submit Answer →";

    }

}


// ============================================================
// SHOW RESULT
// ============================================================

function showResult(data) {

    const resultSection =
        document.getElementById(
            "resultSection"
        );


    const answerCard =
        document.querySelector(
            ".answer-card"
        );


    const scoreBox =
        document.getElementById(
            "scoreBox"
        );


    const feedbackText =
        document.getElementById(
            "feedbackText"
        );


    const matchedConcepts =
        document.getElementById(
            "matchedConcepts"
        );


    const missingConcepts =
        document.getElementById(
            "missingConcepts"
        );


    const nextButton =
        document.getElementById(
            "nextButton"
        );


    if (!resultSection) {
        return;
    }


    resultSection.classList.remove(
        "hidden"
    );


    if (answerCard) {

        answerCard.style.display =
            "none";

    }


    scoreBox.innerHTML = `

        <span>
            YOUR SCORE
        </span>

        <strong>
            ${data.score}
            <small>/10</small>
        </strong>

    `;


    feedbackText.textContent =
        data.feedback ||
        "No feedback available.";


    matchedConcepts.innerHTML =
        renderConcepts(
            data.matched_concepts
        );


    missingConcepts.innerHTML =
        renderConcepts(
            data.missing_concepts
        );


    // ========================================================
    // SPEAK FEEDBACK
    // ========================================================

    speakFeedback(
        data
    );


    // ========================================================
    // COMPLETED
    // ========================================================

    if (data.completed) {

        nextButton.textContent =
            "🏆 View Final Report";


        nextButton.onclick =
            function () {

                showFinalReport(
                    data
                );

            };

    }

    else {

        nextButton.textContent =
            "Next Question →";


        nextButton.onclick =
            function () {

                loadNextQuestion(
                    data
                );

            };

    }


    resultSection.scrollIntoView({
        behavior: "smooth"
    });

}


// ============================================================
// RENDER CONCEPTS
// ============================================================

function renderConcepts(concepts) {

    if (
        !concepts ||
        concepts.length === 0
    ) {

        return `
            <span class="empty-concept">
                None
            </span>
        `;

    }


    return concepts
        .map(
            concept => `
                <span class="concept-tag">
                    ${concept}
                </span>
            `
        )
        .join("");

}


// ============================================================
// SPEAK FEEDBACK
// ============================================================

function speakFeedback(data) {

    let message =
        `Your score is ${data.score} out of 10. `;


    if (data.feedback) {

        message +=
            data.feedback;

    }


    if (data.completed) {

        message +=
            " The interview is now complete.";

    }


    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(
            message
        );


    speech.rate =
        0.9;


    window.speechSynthesis.speak(
        speech
    );

}


// ============================================================
// LOAD NEXT QUESTION
// ============================================================

function loadNextQuestion(data) {

    currentQuestion =
        data.question;


    const questionText =
        document.getElementById(
            "questionText"
        );


    const questionNumber =
        document.getElementById(
            "questionNumber"
        );


    const answerCard =
        document.querySelector(
            ".answer-card"
        );


    const resultSection =
        document.getElementById(
            "resultSection"
        );


    const answerInput =
        document.getElementById(
            "answerInput"
        );


    const submitButton =
        document.getElementById(
            "submitButton"
        );


    questionText.textContent =
        currentQuestion.question;


    questionNumber.textContent =
        data.question_number;


    answerInput.value =
        "";


    submitButton.disabled =
        false;


    submitButton.textContent =
        "Submit Answer →";


    resultSection.classList.add(
        "hidden"
    );


    answerCard.style.display =
        "block";


    speakQuestion(
        currentQuestion.question
    );


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


// ============================================================
// FINAL REPORT
// ============================================================

function showFinalReport(data) {

    document.body.innerHTML = `

        <header class="navbar">

            <div class="nav-container">

                <a
                    href="/"
                    class="logo"
                >
                    <span class="logo-icon">
                        🎤
                    </span>

                    Intervexa
                </a>

                <span class="interview-header">
                    Interview Report
                </span>

            </div>

        </header>


        <main class="final-page">

            <div class="final-container">


                <!-- =========================================
                     HEADER
                ========================================== -->

                <div class="final-heading">

                    <span class="small-label">
                        INTERVIEW COMPLETED
                    </span>

                    <h1>
                        Your Interview Report
                    </h1>

                    <p>
                        Here is your overall interview
                        performance.
                    </p>

                </div>


                <!-- =========================================
                     SCORE CARD
                ========================================== -->

                <section class="final-score-card">

                    <div class="final-trophy">
                        🏆
                    </div>

                    <div class="final-score-content">

                        <span>
                            OVERALL SCORE
                        </span>

                        <strong>
                            ${data.average_score}
                            <small>/10</small>
                        </strong>

                        <p>
                            ${
                                getScoreMessage(
                                    data.average_score
                                )
                            }
                        </p>

                    </div>

                </section>


                <!-- =========================================
                     PERFORMANCE
                ========================================== -->

                <section class="performance-card">

                    <div class="section-heading">

                        <span class="small-label">
                            PERFORMANCE
                        </span>

                        <h2>
                            Interview Summary
                        </h2>

                    </div>


                    <div class="performance-grid">


                        <div class="performance-item">

                            <span class="performance-icon">
                                🎯
                            </span>

                            <div>

                                <strong>
                                    ${
                                        data.average_score
                                    }/10
                                </strong>

                                <span>
                                    Average Score
                                </span>

                            </div>

                        </div>


                        <div class="performance-item">

                            <span class="performance-icon">
                                ❓
                            </span>

                            <div>

                                <strong>
                                    5
                                </strong>

                                <span>
                                    Questions
                                </span>

                            </div>

                        </div>


                        <div class="performance-item">

                            <span class="performance-icon">
                                🤖
                            </span>

                            <div>

                                <strong>
                                    AI
                                </strong>

                                <span>
                                    Evaluation
                                </span>

                            </div>

                        </div>


                    </div>

                </section>


                <!-- =========================================
                     MESSAGE
                ========================================== -->

                <section class="final-message-card">

                    <div class="message-icon">
                        💡
                    </div>

                    <div>

                        <span class="small-label">
                            AI INTERVIEWER
                        </span>

                        <h2>
                            Interview Complete
                        </h2>

                        <p>
                            ${
                                data.message ||
                                "You have successfully completed your technical interview."
                            }
                        </p>

                    </div>

                </section>


                <!-- =========================================
                     ACTIONS
                ========================================== -->

                <div class="final-actions">

                    <button
                        class="primary-button"
                        id="newInterviewButton"
                    >
                        🔄 Start New Interview
                    </button>


                    <button
                        class="secondary-button"
                        id="homeButton"
                    >
                        🏠 Back to Home
                    </button>

                </div>


                <p class="final-footer">
                    Powered by Intervexa AI
                </p>


            </div>

        </main>

    `;


    // ========================================================
    // SPEAK FINAL REPORT
    // ========================================================

    const finalSpeech = `

        Interview completed.

        Your average score is
        ${data.average_score}
        out of 10.

        ${
            getScoreMessage(
                data.average_score
            )
        }

    `;


    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(
            finalSpeech
        );


    speech.rate = 0.9;

    speech.pitch = 1;

    speech.volume = 1;


    window.speechSynthesis.speak(
        speech
    );


    // ========================================================
    // NEW INTERVIEW
    // ========================================================

    document
        .getElementById(
            "newInterviewButton"
        )
        .addEventListener(
            "click",
            function () {

                window.location.href = "/";

            }
        );


    // ========================================================
    // HOME
    // ========================================================

    document
        .getElementById(
            "homeButton"
        )
        .addEventListener(
            "click",
            function () {

                window.location.href = "/";

            }
        );

}


// ============================================================
// SCORE MESSAGE
// ============================================================

function getScoreMessage(score) {

    const numericScore =
        Number(score);


    if (numericScore >= 8) {

        return (
            "Excellent performance! " +
            "You demonstrated strong technical knowledge."
        );

    }


    if (numericScore >= 6) {

        return (
            "Good performance! " +
            "Your fundamentals are developing well."
        );

    }


    if (numericScore >= 4) {

        return (
            "Fair performance. " +
            "Review the important concepts and try again."
        );

    }


    return (
        "Keep practicing. " +
        "Strengthen your fundamentals and try the interview again."
    );

}