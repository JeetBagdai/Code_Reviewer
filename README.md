# CodeSage — AI-Driven Code Reviewer

An AI-powered code review tool built with **Reflex**, **Python AST**, and the **Groq LLM API**.

Paste any code snippet and get instant feedback on bugs, style issues, time/space complexity, and AI-generated improvements. Every review is saved to a history, and you can chat with an AI assistant about any past analysis.

## Features

- **AST-Based Static Analysis** — Parses Python code with the built-in `ast` module to detect mutable default arguments, bare `except` clauses, missing docstrings, unused imports, and overly long functions.
- **Groq LLM Review** — Sends code and AST findings to `llama-3.3-70b-versatile` via the Groq REST API for a structured review with improvement suggestions.
- **Complexity Estimation** — Estimates time and space complexity from loop nesting and recursion patterns.
- **Session History** — Every analysis is stored in the session and browsable from the History page.
- **AI Chat Assistant** — Ask follow-up questions about any past review directly in the app.

## Tech Stack

| Layer | Technology |
|---|---|
| Web Framework | [Reflex](https://reflex.dev) (Python → React) |
| Static Analysis | Python `ast` module |
| AI Model | Groq API — `llama-3.3-70b-versatile` |
| HTTP Client | Python `urllib` (no extra dependencies) |
| Styling | CSS-in-Python via Reflex |

## Setup

```bash
git clone https://github.com/JeetBagdai/Code_Reviewer.git
cd Code_Reviewer

pip install reflex

cp .env.example .env
```

Edit `.env` and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

Then run the app:

```bash
python -m reflex run
```

Open `http://localhost:3000` in your browser.

## Project Structure

```
Code_Review/
├── Code_Review/
│   ├── Code_Review.py      # App entry point and routing
│   ├── state.py            # Reflex state and event handlers
│   ├── ast_analyzer.py     # Python AST static analysis engine
│   ├── groq_client.py      # Groq REST API client
│   └── pages/
│       ├── home.py         # Landing page
│       ├── analyser.py     # Code editor + review panel
│       └── history.py      # Analysis history + AI chat
├── rxconfig.py             # Reflex configuration
├── .env                    # API key (not committed)
└── requirements.txt        # Python dependencies
```

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from [console.groq.com](https://console.groq.com) |
