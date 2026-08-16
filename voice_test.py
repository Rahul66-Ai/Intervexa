import streamlit as st
import subprocess
import tempfile
import os


st.title("🔊 Intervexa Voice Test")

text = st.text_input(
    "Intervexa kya bole?"
)


if st.button("🔊 Speak"):

    if not text.strip():

        st.warning("Pehle kuch text likho.")

    else:

        # Create PowerShell command
        command = f'''
        Add-Type -AssemblyName System.Speech
        $speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
        $speaker.Speak({text!r})
        '''

        subprocess.Popen(
            [
                "powershell",
                "-Command",
                command
            ]
        )

        st.success("Intervexa is speaking! 🔊")