import os
from gtts import gTTS

# Create tests directory if it doesn't exist
os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)

# The mock doctor-patient encounter script
# Carefully designed to include PII (Name, DOB, Location, Phone) and Clinical Flags (Chest Pain, Lisinopril)
encounter = [
    {"speaker": "doctor", "text": "Good morning. I'm Dr. Smith. What brings you in today?"},
    {"speaker": "patient", "text": "Hi Dr. Smith. I'm John Doe. My date of birth is October 12th, 1980. I've been having some mild chest pain for the past few days, and a little shortness of breath."},
    {"speaker": "doctor", "text": "I see. When exactly does the chest pain start? Is it constant or does it come and go?"},
    {"speaker": "patient", "text": "It mostly happens when I walk up the stairs at my apartment in New York. I also take Lisinopril for my blood pressure, if that helps."},
    {"speaker": "doctor", "text": "That is helpful to know. We will run an EKG to be safe, and I might adjust your Lisinopril or add another medication depending on the results. Do you have a pharmacy on file?"},
    {"speaker": "patient", "text": "Yes, the CVS on 5th Avenue. You can reach me at 555-123-4567 if you need anything."}
]

audio_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_visit.mp3")
transcript_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock_encounter_script.txt")

print("Generating mock audio file using gTTS (Google Text-to-Speech)...")

# 1. Write the text script for our reference
with open(transcript_file_path, "w") as t_file:
    for line in encounter:
        t_file.write(f"{line['speaker'].capitalize()}: {line['text']}\n")

# 2. Generate and combine the audio
# We use tld='com' (US accent) for the doctor, and tld='co.uk' (UK accent) for the patient to fake two distinct voices.
with open(audio_file_path, "wb") as f:
    for line in encounter:
        print(f"Synthesizing {line['speaker'].capitalize()}...")
        tld = "com" if line["speaker"] == "doctor" else "co.uk"
        
        # Generate the speech stream and append it directly to the mp3 file
        tts = gTTS(text=line["text"], lang="en", tld=tld)
        tts.write_to_fp(f)

print(f"\nSuccess! Audio file saved to: {audio_file_path}")
print(f"Transcript text saved to: {transcript_file_path}")