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
    if uploaded_file is None:
        st.warning("Please upload an audio file first. You can drag and drop the 'sample_visit.mp3' from your TestSuite folder!")
    else:
        with st.spinner("Processing audio and generating notes..."):
            # Save uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix = ".mp3") as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file_path = temp_file.name
                
            try:
                # 1. speach to text
                with st.status("Transcribing audio...") as status:
                    raw_transcript = stt.transcribe_audio(temp_file_path)
                    st.markdown("**Raw Transcript:**")
                    st.info(raw_transcript)
                    status.update(label="🎙️ Audio Transcribed", state="complete", expanded=False)

                # 2. PII Redaction
                with st.status("Redacting PII/PHI...") as status:
                    redacted_transcript = redactor.redact(raw_transcript)
                    st.markdown("**Redacted Transcript:**")
                    st.success(redacted_transcript)
                    status.update(label="🔒 PII Redacted", state="complete", expanded=False)

                # 3. LLM SOAP Note
                with st.status("📝 Generating SOAP Note...") as status:
                    soap_note = llm.generate_soap_note(redacted_transcript)
                    st.json(soap_note)
                    status.update(label="📝 SOAP Note Generated", state="complete", expanded=False)

                # 4. Clinical Safety Checks
                with st.status("⚕️ Running Clinical Safety Checks...") as status:
                    subjective_text = soap_note.get("Subjective", "")
                    flags = safety_layer.flag_symptoms(subjective_text)
                    if flags:
                        st.error(f"⚠️ HIGH RISK SYMPTOMS DETECTED: {', '.join(flags).title()}")
                    else:
                        st.success("✅ No high-risk symptoms detected.")
                    

                    #simulating NLP medication extraction for demonstration purposes
                    st.markdown("**Drug Interaction Check:**")
                    extracted_meds = ["Lisinopril", "Potassium"]
                    interactions = safety_layer.check_drug_interactions(extracted_meds)
                    for interaction in interactions:
                        st.warning(interaction)
                    status.update(label="✅ Clinical Safety Checks Completed", state="complete", expanded=False)

            finally:
                os.remove(temp_file_path)
                    

