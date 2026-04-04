from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

class PIIRedactor:
    def __init__(self):
        """
        Initializes the Presidio Analyzer and Anonymizer engines.
        Note: This requires a spaCy model to be installed. 
        If you haven't already, run: python -m spacy download en_core_web_lg
        """
        print("Initializing PII Redaction engines...")
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def redact(self, text: str) -> str:
        """
        Scans the input text for PII/PHI and replaces them with placeholders.
        """
        if not text:
            return ""

        # 1. Analyze the text to find PII entities
        # We can specify exactly which entities to look for to speed it up,
        # or leave it empty to use all supported entities.
        results = self.analyzer.analyze(
            text=text,
            language='en',
            entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "LOCATION", "DATE_TIME"]
        )

        # 2. Anonymize the detected entities
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )

        return anonymized_result.text

# --- Quick Test ---
if __name__ == "__main__":
    redactor = PIIRedactor()
    sample_transcript = "Patient John Doe, DOB 10/12/1980, came in complaining of chest pain. He can be reached at 555-123-4567 in New York."
    safe_text = redactor.redact(sample_transcript)
    print(f"\nOriginal: {sample_transcript}")
    print(f"Redacted: {safe_text}")