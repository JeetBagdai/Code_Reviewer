import json
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
MODEL = "llama-3.3-70b-versatile"


def _call_groq(messages: list[dict]) -> str:
    try:
        chat = ChatGroq(
            temperature=0.3,
            max_tokens=2048,
            groq_api_key=GROQ_API_KEY,
            model_name=MODEL,
            max_retries=2,
        )

        lc_messages = []
        for m in messages:
            if m.get("role") == "system":
                lc_messages.append(SystemMessage(content=m["content"]))
            elif m.get("role") == "user":
                lc_messages.append(HumanMessage(content=m["content"]))
            elif m.get("role") == "assistant":
                lc_messages.append(AIMessage(content=m["content"]))

        response = chat.invoke(lc_messages)
        return response.content
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
        if raw.startswith("API error") or raw.startswith("Request failed"):
            raise ValueError(raw)
            
        start = raw.find("{")
        end = raw.rfind("}") + 1
        parsed = json.loads(raw[start:end])
        
        if "error" in parsed:
            raise ValueError(f"API returned error: {parsed['error']}")
            
        return parsed
    except Exception as e:
        error_msg = str(e) if str(e) else raw
        return {
            "bugs": ast_findings.get("bugs", []),
            "quality_issues": ast_findings.get("quality_issues", []),
            "complexity": ast_findings.get("complexity", {"time": "O(?)", "space": "O(?)"}),
            "improvements": error_msg,
            "summary": "Review fallback due to API error.",
        }


def get_chat_response(history_context: str, messages: list[dict]) -> str:
    system_prompt = (
        "You are an expert AI code assistant. The user is reviewing previously analyzed code. "
        f"Here is the context from the analysis:\n{history_context}\n\n"
        "Answer questions about the code, explain issues, and suggest fixes concisely."
    )

    chat_messages = [{"role": "system", "content": system_prompt}] + messages
    return _call_groq(chat_messages)
