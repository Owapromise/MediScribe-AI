import os
import json
from stt_engine import STTEngine
from pii_redaction import PIIRedactor
from safety_layer import ClinicalSafetyLayer
from llm_engine import LLMEngine

def run_mediscribe_pipeline(audio_path: str, transcript_path: str=None):
    print("\n--- Starting MediScribeAI Pipeline ---")

    # 1. Initialize all modules
    print("\n[1] Initializing Modules...")
    stt= STTEngine()
    redactor = PIIRedactor()
    safety_layer = ClinicalSafetyLayer()
    llm = LLMEngine()

    # 2. Transcribe speech to text (Mock transcipt if no API key)
    print("\n[2] processing Audio / Transcrip...")
    raw_transcript = ""

    api_key = os.getenv("OPENAI_API_KEY")
    if (not api_key or api_key.startswith("sk-your-")) and transcript_path:
        print("Mock mode: Loading pre-generated transcript instead of calling whisper API.")
        with open(transcript_path, "r") as f:
            raw_transcript = f.read()
    else:
        raw_transcript = stt.transcribe_audio(audio_path)

    print("\n---Raw Transcript---")
    print(raw_transcript.strip())

    # 3. PII Redaction
    print("\n[3] Redacting PII/PHI...")
    redacted_transcript = redactor.redact(raw_transcript)
    
    print("\n--- Redacted Transcript ---")
    print(redacted_transcript.strip())

    # 4. LLM SOAP Note Generation
    print("\n[4] Generating SOAP Note...")
    soap_note = llm.generate_soap_note(redacted_transcript)
    
    print("\n--- Generated SOAP Note ---")
    print(json.dumps(soap_note, indent=2))

    # 5. Clinical Safety & Triage
    print("\n[5] Running Clinical Safety Checks...")
    
    # Analyze the Subjective section for red flags
    subjective_text = soap_note.get("Subjective", "")
    flags = safety_layer.flag_symptoms(subjective_text)
    
    print("\n--- Triage Alerts ---")
    if flags:
        print(f"⚠️ HIGH RISK SYMPTOMS DETECTED: {', '.join(flags).title()}")
    else:
        print("✅ No high-risk symptoms detected.")
        
    print("\n--- Drug Interaction Check ---")
    # Simulating NLP medication extraction for demonstration purposes
    extracted_meds = ["Lisinopril", "Potassium"] 
    interactions = safety_layer.check_drug_interactions(extracted_meds)
    for interaction in interactions:
        print(f"- {interaction}")

    print("\n=== Pipeline Complete ===")
    return soap_note 


if __name__ == "__main__":
    audio_file = os.path.join("TestSuite","sample_visit.mp3") 
    transcript_file = os.path.join("TestSuite","mock_encounter_script.txt")

    run_mediscribe_pipeline(audio_file, transcript_file)