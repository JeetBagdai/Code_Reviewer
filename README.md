# CodeSage — AI Code Reviewer

An AI-powered code review tool built with Reflex, Python AST, and Groq LLM.

## Setup

```bash
pip install reflex
cp .env.example .env
```

Add your Groq API key to `.env`:

```
GROQ_API_KEY=your_key_here
```

Then run:

```bash
python -m reflex run
```

## What it does

- Analyses code for bugs, style issues, and complexity using Python AST
- Sends findings to Groq (`llama-3.3-70b-versatile`) for AI-generated improvements
- Saves a history of all reviews with an interactive AI chat assistant
