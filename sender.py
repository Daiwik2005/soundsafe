import streamlit as st
import numpy as np
import soundfile as sf
import base64
import zlib
import tempfile
import os

def encode_to_tones(data):
    tones = []
    for byte in data:
        freq = 300 + (byte % 50) * 20  # Keep it in audible range
        tones.append(freq)
    return tones

def generate_audio_from_tones(tones, duration=0.15, samplerate=44100):
    audio = np.concatenate([
        np.sin(2 * np.pi * freq * np.linspace(0, duration, int(samplerate * duration)))
        for freq in tones
    ])
    return audio

st.title("🔊 SonicDrop - Transmit Text via Sound")

message = st.text_area("Enter your message")

if st.button("Send via Sound"):
    if message:
        compressed = zlib.compress(message.encode())
        encoded = base64.b64encode(compressed)
        tones = encode_to_tones(encoded)

        audio = generate_audio_from_tones(tones)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            sf.write(f.name, audio, 44100)
            st.audio(f.name)
            st.success("Sound sent! Let your laptop listen and decode.")
    else:
        st.warning("Please enter a message first.")
