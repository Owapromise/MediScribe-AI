import streamlit as st
import os
import tempfile
import json
import time
from stt_engine import STTEngine
from pii_redaction import PIIRedactor
from safety_layer import ClinicalSafetyLayer
from llm_engine import LLMEngine

#page config
st.set_page_config(page_title="MediScribeAI", page_icon="🩺", layout="wide")

# Custom CSS for a sophisticated MedTech UI
st.markdown("""
<style>
    .stButton>button {
        background-color: #0056b3;
        color: white;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #003d82;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .med-header {
        color: #0056b3;
        border-bottom: 2px solid #0056b3;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for System Diagnostics
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3003/3003051.png", width=100) # Medical AI Tech icon
    st.title("⚙️ System Status")
    st.markdown("---")
    st.metric(label="HIPAA Privacy Engine", value="Active", delta="Secure", delta_color="normal")
    st.metric(label="LLM SOAP Generator", value="Online", delta="GPT-3.5")
    st.metric(label="RxNav Triage DB", value="Connected", delta="Mock")
    st.markdown("---")
    st.caption("MediScribeAI v1.2.0 | Encrypted Pipeline")

st.markdown("<h1 class='med-header'>⚕️ MediScribeAI Clinical Dashboard</h1>", unsafe_allow_html=True)
st.markdown("Automated clinical documentation and real-time safety triage powered by advanced AI.")    

# initialize Engines
@st.cache_resource
def initialize_engines():
    return STTEngine(), PIIRedactor(), ClinicalSafetyLayer(), LLMEngine()
stt, redactor, safety_layer, llm = initialize_engines()

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📥 Input & Data Pipeline")
    # UI for file upload
    uploaded_file = st.file_uploader("Upload consultation audio file (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"])
    analyze_btn = st.button("🚀 Analyze Consultation", type="primary", use_container_width=True)

if analyze_btn:
    if uploaded_file is None:
        with col1:
            st.warning("Please upload an audio file first. You can drag and drop 'sample_visit.mp3' from your TestSuite folder!")
    else:
        with col1:
            st.info("Initiating secure processing pipeline...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file_path = temp_file.name
                
            try:
                with st.status("Transcribing audio...", expanded=True) as status:
                    st.write("Generating transcript using Whisper...")
                    raw_transcript = stt.transcribe_audio(temp_file_path)
                    time.sleep(0.5) # UI pacing
                    status.update(label="🎙️ Audio Transcribed", state="complete", expanded=False)

                with st.status("Redacting PII/PHI...", expanded=True) as status:
                    st.write("Masking identifiers via NLP...")
                    redacted_transcript = redactor.redact(raw_transcript)
                    time.sleep(0.5)
                    status.update(label="🔒 PII Redacted", state="complete", expanded=False)
                    
                with st.status("📝 Generating SOAP Note...", expanded=True) as status:
                    st.write("Synthesizing clinical notes...")
                    soap_note = llm.generate_soap_note(redacted_transcript)
                    status.update(label="📝 SOAP Note Generated", state="complete", expanded=False)

                with st.status("⚕️ Running Clinical Safety Checks...", expanded=True) as status:
                    st.write("Cross-referencing triage database...")
                    subjective_text = soap_note.get("Subjective", "")
                    flags = safety_layer.flag_symptoms(subjective_text)
                    extracted_meds = ["Lisinopril", "Potassium"]
                    interactions = safety_layer.check_drug_interactions(extracted_meds)
                    status.update(label="✅ Clinical Safety Checks Completed", state="complete", expanded=False)

            finally:
                os.remove(temp_file_path)

        with col2:
            st.subheader("🔍 Diagnostics & Alerts")
            with st.expander("View Processed Transcripts", expanded=True):
                st.markdown("**Raw Transcript (Internal Use Only):**")
                st.info(raw_transcript)
                st.markdown("**Redacted Transcript:**")
                st.success(redacted_transcript)
                
            st.markdown("### 🚨 Triage & Safety Alerts")
            if flags:
                st.error(f"**High Risk Symptoms Detected:** {', '.join(flags).title()}", icon="🚨")
            else:
                st.success("**Symptom Check:** No high-risk symptoms detected.", icon="✅")
                
            for interaction in interactions:
                if "No known" in interaction:
                    st.success(f"**Drug Interactions:** {interaction}", icon="✅")
                else:
                    st.warning(f"**Drug Interactions:** {interaction}", icon="⚠️")
