# AI & Clinical Decision Support: Medical Scribe & Triage Tool

![MediScribeAI Screenshot](./mediscribe_app_screenshot.png)

An AI-powered backend designed to reduce clinician burnout by automating medical documentation while ensuring patient safety and data privacy. This tool processes raw doctor-patient audio transcripts, generates structured SOAP notes, and acts as a preliminary clinical triage layer by flagging high-risk symptoms and potential drug-drug interactions.

## 🚀 Key Features

1. **Speech-to-Text (STT)**: Converts raw consultation audio into text using OpenAI's Whisper model.
2. **PII Redaction & Anonymization**: A crucial pre-processing step that scrubs Protected Health Information (PHI) from transcripts to maintain HIPAA compliance before transmitting data to external LLMs.
3. **Automated SOAP Note Generation**: Leverages advanced Large Language Models (OpenAI/Anthropic) to structure conversations into standard Subjective, Objective, Assessment, and Plan (SOAP) formats.
4. **Clinical Safety Layer**: 
    - Analyzes the subjective data for high-risk symptoms (e.g., chest pain, shortness of breath).
    - Extracts medication plans and cross-references them against clinical knowledge bases (e.g., NIH RxNav API) to flag potential drug-drug interactions.

## 🛠 Tech Stack

- **Language**: Python 3.10+
- **Speech-to-Text**: [Whisper](https://github.com/openai/whisper)
- **PII Redaction**: [Microsoft Presidio](https://microsoft.github.io/presidio/) (Targeted for upcoming integration)
- **LLM Engine**: OpenAI API / Anthropic API
- **Safety / Triage**: spaCy (NLP keyword extraction) & NIH RxNav API

## ⚙️ Architecture Pipeline

```text
[Audio Input] 
    │
    ▼
[ Whisper STT ] ──► (Raw Transcript)
    │
    ▼
[ PII Redaction ] ──► (Anonymized Transcript)
    │
    ▼
[ LLM Engine ] ──► (Structured SOAP Note JSON)
    │
    ▼
[ Safety Layer ] ──► (Drug Interactions & Triage Alerts)
    │
    ▼
[ Final Output: Safe SOAP Note + Clinical Alerts ]
