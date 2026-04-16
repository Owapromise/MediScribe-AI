import os
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

    return redacted_transcript 


if __name__ == "__main__":
    audio_file = os.path.join("TestSuite","sample_visit.mp3") 
    transcript_file = os.path.join("TestSuite","mock_encounter_script.txt")

    run_mediscribe_pipeline(audio_file, transcript_file)