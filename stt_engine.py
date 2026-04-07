import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class STTEngine:
    def __init__(self):
        """
        Initializes the OpenAI client for the Whisper API.
        Ensure you have an OPENAI_API_KEY set in your .env file.
        """
        print("Initializing Speech-to-Text engine...")
        # The OpenAI client automatically looks for the OPENAI_API_KEY environment variable
        self.client = OpenAI()

    def transcribe_audio(self, file_path: str) -> str:
        """
        Takes a path to an audio file and returns the transcribed text using Whisper.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found at: {file_path}")

        print(f"Transcribing {file_path}...")
        
        with open(file_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text"
            )
        
        return transcription

# --- Quick Test ---
if __name__ == "__main__":
    # Note: To run this test, you'll need an actual audio file and your .env file setup.
    # stt = STTEngine()
    # text = stt.transcribe_audio("sample_visit.mp3")
    # print(text)
    print("STT module loaded. Ready to test when an audio file and .env are provided!")