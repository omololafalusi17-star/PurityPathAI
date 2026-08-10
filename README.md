# 🌿 PurityPathAI

**Your Worth. Your Choice. Your Path.**

PurityPathAI is an AI-powered youth education assistant MVP built with Python and Streamlit.

## Features

- 🏠 Home dashboard
- 📚 Age-aware Learning Center
- 🎮 Interactive Choose Your Path scenarios
- 💬 AI-powered educational assistant
- 🛡️ Basic safety triage layer
- ✨ AI content generator for educators
- 👩‍🏫 Mentor resources
- 🔐 Privacy-conscious design

## Important

This is an MVP, not a production-ready safeguarding system. The keyword safety layer is only a first-pass prototype and can miss context or produce false positives. Before public launch, add robust moderation, professional safeguarding review, local escalation pathways, privacy/legal review, and testing with qualified child-safety professionals.

## Setup

### 1. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the API key

Copy `.env.example` to `.env` and add your API key:

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.5
```

Never commit `.env` to GitHub.

### 4. Run the app

```bash
streamlit run app.py
```

## Project structure

```text
PurityPathAI/
├── app.py
├── prompts.py
├── safety.py
├── learning_content.py
├── scenarios.py
├── mentor_resources.py
├── ai_content_generator.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Suggested next steps for production

1. Add authentication and role-based access.
2. Add a database with strict data minimization.
3. Add professional moderation and safeguarding workflows.
4. Add formal privacy and child-safety review.
5. Add local emergency/support resources by country.
6. Add automated tests and adversarial safety testing.
7. Add analytics that use aggregated, non-identifying data.
8. Conduct usability testing with qualified educators and safeguarding experts.
