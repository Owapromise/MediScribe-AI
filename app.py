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
