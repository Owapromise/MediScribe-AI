import spacy
import requests

class ClinicalSafetyLayer:
    def __init__(self):
        print("Initializing Clinical Safety Layer (spaCy & RxNav)...")
        try:
            # We use the same spaCy model that Presidio uses
            self.nlp = spacy.load("en_core_web_lg")
        except OSError:
            print("Downloading spaCy model 'en_core_web_lg'...")
            spacy.cli.download("en_core_web_lg")
            self.nlp = spacy.load("en_core_web_lg")
            
        # Hardcoded high-risk keywords for clinical triage
        self.high_risk_keywords = [
            "chest pain", "shortness of breath", "difficulty breathing",
            "suicidal", "stroke", "bleeding", "dizziness", "fainting"
        ]

    def flag_symptoms(self, text: str) -> list:
        """Scans text for high-risk clinical symptoms."""
        if not text:
            return []
            
        # Ensure text is a string (LLMs can sometimes return lists of bullet points)
        if isinstance(text, list):
            text = " ".join(str(item) for item in text)
        elif not isinstance(text, str):
            text = str(text)

        text_lower = text.lower()
        flags = []
        for keyword in self.high_risk_keywords:
            if keyword in text_lower:
                flags.append(keyword)
        return flags

    def get_rxcui(self, drug_name: str) -> str:
        """Fetches the RxCUI (concept unique identifier) for a given drug name using NIH RxNav."""
        try:
            response = requests.get(f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name}")
            response.raise_for_status()
            data = response.json()
            if "idGroup" in data and "rxnormId" in data["idGroup"]:
                return data["idGroup"]["rxnormId"][0]
        except Exception as e:
            print(f"Error fetching RxCUI for {drug_name}: {e}")
        return None

    def check_drug_interactions(self, medications: list) -> list:
        """
        Checks for interactions between a list of medications.
        Note: The NIH RxNav Drug Interaction API was recently retired.
        This function now uses a mock clinical database for demonstration purposes.
        In a production app, you would integrate a paid API like Lexicomp or Epocrates.
        """
        if len(medications) < 2:
            return ["Need at least 2 medications to check for interactions."]
            
        interactions_found = []
        meds_lower = set([m.lower() for m in medications])
        
        # Mock clinical knowledge base
        if "lisinopril" in meds_lower and "potassium" in meds_lower:
            interactions_found.append("High Risk: Concurrent use of Lisinopril and Potassium may result in hyperkalemia (high blood potassium levels).")
            
        if not interactions_found:
            interactions_found.append("No known severe interactions found in mock database.")
            
        return interactions_found

# --- Quick Test ---
if __name__ == "__main__":
    safety = ClinicalSafetyLayer()
    
    # Test symptom flagging using text similar to our mock generated transcript
    mock_text = "I've been having some mild chest pain for the past few days, and a little shortness of breath."
    flags = safety.flag_symptoms(mock_text)
    print(f"\n[Symptom Flags Found]: {flags}")
    
    # Test drug interactions (Lisinopril + Potassium)
    # Adding Potassium because Lisinopril + Potassium is a known severe interaction (hyperkalemia)
    drug_name = ["Lisinopril", "Potassium"]
    print(f"\n[Checking Interactions for]: {drug_name}")
    interactions = safety.check_drug_interactions(drug_name)
    for interaction in interactions:
        print(f"- {interaction}")