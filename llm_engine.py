import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMEngine:
    def __init__(self):
        print("Initializing LLM Engine (SOAP Note Generator)...")
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        # Run in mock mode if key is missing, empty, or is the dummy placeholder
        self.mock_mode = not bool(self.api_key) or self.api_key.startswith("sk-your-")
        if self.mock_mode:
            print("⚠️ No valid OPENAI_API_KEY found. LLM Engine running in MOCK mode.")
        else:
            self.client = OpenAI()

    def generate_soap_note(self, transcript: str) -> dict:
        """Takes an anonymized transcript and returns a structured SOAP note."""
        if not transcript:
            return {}

        if self.mock_mode:
            # Returning a hardcoded JSON response that matches our test audio script
            return {
                "Subjective": "Patient [PERSON] (DOB: [DATE_TIME]) presents with mild chest pain for the past few days and shortness of breath. Pain occurs mostly when walking up stairs at their apartment in [LOCATION].",
                "Objective": "Patient takes Lisinopril for blood pressure.",
                "Assessment": "Chest pain and shortness of breath, evaluating for cardiac etiology.",
                "Plan": ["Run EKG", "Consider adjusting Lisinopril or adding medication based on EKG results", "Pharmacy on file: CVS on 5th Avenue"]
            }

        system_prompt = """
        You are an expert medical scribe. 
        Analyze the provided doctor-patient transcript and generate a structured SOAP note.
        Respond ONLY with a valid JSON object containing exactly these four keys: 
        "Subjective", "Objective", "Assessment", and "Plan".
        Ensure the "Plan" value is a list of strings representing actionable items and medications.
        """
        
        try:
            print("Sending transcript to OpenAI...")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": transcript}
                ],
                response_format={ "type": "json_object" } # Forces strict JSON output
            )
            
            # Parse the JSON string returned by the LLM into a Python dictionary
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error generating SOAP note: {e}")
            return {}

# --- Quick Test ---
if __name__ == "__main__":
    llm = LLMEngine()
    print(json.dumps(llm.generate_soap_note("mock transcript text..."), indent=2))