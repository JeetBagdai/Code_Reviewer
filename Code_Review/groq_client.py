import urllib.request
import urllib.error
import json
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


def _call_groq(messages: list[dict]) -> str:
    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 2048,
    }).encode("utf-8")

    req = urllib.request.Request(
        GROQ_API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "CodeSage-Reviewer/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return f"API error {e.code}: {body}"
    except Exception as e:
        return f"Request failed: {str(e)}"


def get_code_review(code: str, ast_findings: dict) -> dict:
    bugs_str = "\n".join(ast_findings.get("bugs", [])) or "None detected"
    quality_str = "\n".join(ast_findings.get("quality_issues", [])) or "None detected"

    system_prompt = (
        "You are an expert code reviewer. Analyze the given code and the AST findings, "
        "then respond ONLY with a valid JSON object in this exact structure:\n"
        '{"bugs": [...], "quality_issues": [...], '
        '"complexity": {"time": "O(?)", "space": "O(?)"}, '
        '"improvements": "improved code as a string", '
        '"summary": "one-sentence summary"}'
        "\nDo not include any text before or after the JSON."
    )

    user_msg = (
        f"Code to review:\n```python\n{code}\n```\n\n"
        f"AST-detected bugs:\n{bugs_str}\n\n"
        f"AST-detected quality issues:\n{quality_str}"
    )

    raw = _call_groq([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg},
    ])

    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except Exception:
        return {
            "bugs": ast_findings.get("bugs", []),
            "quality_issues": ast_findings.get("quality_issues", []),
            "complexity": ast_findings.get("complexity", {"time": "O(?)", "space": "O(?)"}),
            "improvements": raw,
            "summary": "Review complete.",
        }


def get_chat_response(history_context: str, messages: list[dict]) -> str:
    system_prompt = (
        "You are an expert AI code assistant. The user is reviewing previously analyzed code. "
        f"Here is the context from the analysis:\n{history_context}\n\n"
        "Answer questions about the code, explain issues, and suggest fixes concisely."
    )

    chat_messages = [{"role": "system", "content": system_prompt}] + messages
    return _call_groq(chat_messages)
