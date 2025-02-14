# TeeCustomizer Ordering Assistant

This project implements a chatbot interface for a LangGraph-based agent that guides users through a customized t-shirt ordering process.

## Setup Instructions (Windows)

0. **Create .env file and enter your OpeanAI API key into it**

```
OPENAI_API_KEY=SOME_VALUE
```

1. **Create a Virtual Environment**

   Open Command Prompt (or PowerShell) and run:

```
   python -m venv .venv
```

2. **Activate the Virtual Environment**

Command Prompt:

```
    .venv\Scripts\activate
```

3. **Install Dependencies**

Ensure that you have a requirements.txt file in the project root, then run:

```
pip install -r requirements.txt
```

4. **Run the Application**

Start the application by executing:

```
py app/main.py
```