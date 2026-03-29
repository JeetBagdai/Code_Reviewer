import reflex as rx
import datetime
from Code_Review.ast_analyzer import analyze
from Code_Review.groq_client import get_code_review, get_chat_response


class AppState(rx.State):
    code_input: str = ""
    is_loading: bool = False
    is_chat_loading: bool = False

    review_bugs: list[str] = []
    review_quality: list[str] = []
    review_time_complexity: str = ""
    review_space_complexity: str = ""
    review_improvements: str = ""
    review_summary: str = ""
    has_review: bool = False

    history: list[dict] = []
    chat_messages: list[dict] = []
    chat_input: str = ""
    selected_history_index: int = -1

    def clear_code(self):
        self.code_input = ""
        self.has_review = False
        self.review_bugs = []
        self.review_quality = []
        self.review_time_complexity = ""
        self.review_space_complexity = ""
        self.review_improvements = ""
        self.review_summary = ""

    def set_code(self, value: str):
        self.code_input = value

    def set_chat_input(self, value: str):
        self.chat_input = value

    def select_history_item(self, index: int):
        self.selected_history_index = index
        self.chat_messages = []

    def clear_history(self):
        self.history = []
        self.chat_messages = []
        self.selected_history_index = -1

    @rx.event(background=True)
    async def analyse_code(self):
        async with self:
            if not self.code_input.strip():
                return
            self.is_loading = True
            self.has_review = False
            self.review_bugs = []
            self.review_quality = []
            self.review_improvements = ""
            self.review_summary = ""

        code_snapshot = self.code_input

        async with self:
            ast_findings = await rx.run_in_thread(
                lambda: analyze(code_snapshot)
            )

        async with self:
            ai_review = await rx.run_in_thread(
                lambda: get_code_review(code_snapshot, ast_findings)
            )

        async with self:
            merged_bugs = list(set(
                ast_findings.get("bugs", []) + ai_review.get("bugs", [])
            ))
            merged_quality = list(set(
                ast_findings.get("quality_issues", []) + ai_review.get("quality_issues", [])
            ))
            complexity = ai_review.get("complexity", ast_findings.get("complexity", {"time": "O(?)", "space": "O(?)"}))
            improvements = ai_review.get("improvements", "")
            summary = ai_review.get("summary", "")
            score = ast_findings.get("score", 80)
            language = ast_findings.get("language", "Unknown")
            snippet = ast_findings.get("snippet", code_snapshot[:120])

            self.review_bugs = merged_bugs
            self.review_quality = merged_quality
            self.review_time_complexity = complexity.get("time", "O(?)")
            self.review_space_complexity = complexity.get("space", "O(?)")
            self.review_improvements = improvements
            self.review_summary = summary
            self.has_review = True
            self.is_loading = False

            self.history.insert(0, {
                "timestamp": datetime.datetime.now().strftime("%b %d, %Y %H:%M"),
                "snippet": snippet,
                "score": score,
                "language": language,
                "complexity": complexity.get("time", "O(?)"),
                "code": code_snapshot,
                "bugs": merged_bugs,
                "quality": merged_quality,
                "improvements": improvements,
                "summary": summary,
            })

    @rx.event(background=True)
    async def send_chat_message(self):
        async with self:
            if not self.chat_input.strip():
                return
            msg = self.chat_input
            self.chat_messages.append({"role": "user", "content": msg})
            self.chat_input = ""
            self.is_chat_loading = True

        async with self:
            context = ""
            idx = self.selected_history_index
            history_snapshot = list(self.history)
            if 0 <= idx < len(history_snapshot):
                item = history_snapshot[idx]
                context = (
                    f"Code:\n{item.get('code', '')}\n\n"
                    f"Bugs: {item.get('bugs', [])}\n"
                    f"Quality issues: {item.get('quality', [])}\n"
                    f"Improvements: {item.get('improvements', '')}"
                )
            messages_snapshot = list(self.chat_messages)

        async with self:
            response = await rx.run_in_thread(
                lambda: get_chat_response(context, messages_snapshot)
            )

        async with self:
            self.chat_messages.append({"role": "assistant", "content": response})
            self.is_chat_loading = False

    @rx.event
    def handle_chat_key(self, key: str):
        if key == "Enter":
            return AppState.send_chat_message()
