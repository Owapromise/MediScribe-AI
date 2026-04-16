import streamlit as st
import os
import tempfile
import json
from stt_engine import STTEngine
from pii_redaction import PIIRedactor
from safety_layer import ClinicalSafetyLayer
from llm_engine import LLMEngine

#page config
st.set_page_config(page_title="MediScribeAI", page_icon="🩺", layout="wide")

st.title("⚕️ MediScribeAI Clinical Assistant")
st.markdown("Upload a doctor-patient conversation audio file, and MediScribeAI will transcribe, redact PII, generate a SOAP note, and check for clinical safety flags.")    

# initialize Engines
@st.cache_resource
def initialize_engines():
    return STTEngine(), PIIRedactor(), ClinicalSafetyLayer(), LLMEngine()
stt, redactor, safety_layer, llm = initialize_engines()

# UI for file upload
uploaded_file = st.file_uploader("Upload consultationaudio file (MP3, WAV, m4a)", type=["mp3", "wav", "m4a"])

if st.button("Generate Medical Notes", type="primary"):
    if uploaded_file is not None:
        st.warning("Please upload an audio file first. You can drag and drop the 'sample_visit.mp3' from your TestSuite folder!")
    else:
        with st.spinner("Processing audio and generating notes..."):
            # Save uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix = ".mp3") as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file_path = temp_file.name