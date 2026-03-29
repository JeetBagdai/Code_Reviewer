import reflex as rx

from Code_Review.pages.home import home_page
from Code_Review.pages.analyser import analyser_page
from Code_Review.pages.history import history_page
from Code_Review.state import AppState

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap",
    ],
    style={
        "*": {
            "box_sizing": "border-box",
            "margin": "0",
            "padding": "0",
        },
        "body": {
            "font_family": "'Inter', 'Segoe UI', sans-serif",
            "background": "#0f0a1e",
        },
        "::scrollbar": {"width": "6px"},
        "::scrollbar-track": {"background": "rgba(139, 92, 246, 0.05)"},
        "::scrollbar-thumb": {
            "background": "rgba(139, 92, 246, 0.3)",
            "border_radius": "3px",
        },
    }
)

app.add_page(home_page, route="/")
app.add_page(analyser_page, route="/analyser")
app.add_page(history_page, route="/history")
