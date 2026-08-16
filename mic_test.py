import streamlit as st
import speech_recognition as sr

from streamlit_mic_recorder import mic_recorder


st.title("🎙️ Intervexa - Voice to Text Test")

st.write("Microphone button dabao aur clearly bolo.")


audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹️ Stop Recording",
    just_once=False,
    use_container_width=True,
    format="wav"
)


if audio:

    st.success("Recording received! ✅")

    # Play recorded audio
    st.audio(
        audio["bytes"],
        format="audio/wav"
    )


    # Create SpeechRecognition object
    recognizer = sr.Recognizer()


    try:

        # Save browser audio temporarily
        with open("temp_audio.wav", "wb") as file:

            file.write(audio["bytes"])


        # Read the recorded audio
        with sr.AudioFile("temp_audio.wav") as source:

            recorded_audio = recognizer.record(source)


        # Convert speech to text
        text = recognizer.recognize_google(
            recorded_audio
        )


        st.subheader("📝 Your Speech")

        st.write(text)


    except sr.UnknownValueError:

        st.warning(
            "Sorry, I could not understand the audio."
        )


    except sr.RequestError:

        st.error(
            "Speech recognition service is unavailable."
        )


    except Exception as e:

        st.error(
            f"Error: {e}"
        )