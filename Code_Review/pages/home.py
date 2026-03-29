import reflex as rx
from Code_Review.state import AppState


def home_page() -> rx.Component:
    return rx.box(
        rx.box(
            rx.flex(
                rx.box(
                    rx.el.span("⬡", style={"font_size": "1.5rem", "color": "#a78bfa"}),
                    rx.el.span(
                        "CodeSage",
                        style={"font_weight": "700", "font_size": "1.1rem", "color": "#e2e8f0", "margin_left": "8px"}
                    ),
                    display="flex",
                    align_items="center",
                ),
                rx.flex(
                    rx.link("Home", href="/", style=nav_link_style()),
                    rx.link("Analyser", href="/analyser", style=nav_link_style()),
                    rx.link("History", href="/history", style=nav_link_style()),
                    gap="2rem",
                    align_items="center",
                ),
                justify_content="space-between",
                align_items="center",
                padding="1rem 2.5rem",
            ),
            style={
                "border_bottom": "1px solid rgba(139, 92, 246, 0.2)",
                "background": "rgba(15, 10, 30, 0.9)",
                "backdrop_filter": "blur(12px)",
                "position": "sticky",
                "top": "0",
                "z_index": "100",
            }
        ),
        rx.center(
            rx.vstack(
                rx.box(
                    rx.el.div(
                        style={
                            "width": "80px",
                            "height": "80px",
                            "border_radius": "50%",
                            "background": "linear-gradient(135deg, #8b5cf6, #ec4899)",
                            "display": "flex",
                            "align_items": "center",
                            "justify_content": "center",
                            "font_size": "2.5rem",
                            "margin": "0 auto 2rem auto",
                            "box_shadow": "0 0 40px rgba(139, 92, 246, 0.5)",
                        },
                    ),
                ),
                rx.el.h1(
                    "AI-Powered",
                    rx.el.span(
                        " Code Reviewer",
                        style={"background": "linear-gradient(90deg, #8b5cf6, #ec4899)", "WebkitBackgroundClip": "text", "WebkitTextFillColor": "transparent"}
                    ),
                    style={
                        "font_size": "clamp(2.5rem, 5vw, 4rem)",
                        "font_weight": "800",
                        "line_height": "1.1",
                        "color": "#f1f5f9",
                        "text_align": "center",
                    }
                ),
                rx.el.p(
                    "Paste your code. Get instant bugs, style feedback, complexity analysis, and AI-powered improvements.",
                    style={
                        "color": "#94a3b8",
                        "font_size": "1.15rem",
                        "text_align": "center",
                        "max_width": "550px",
                        "line_height": "1.7",
                        "margin_top": "1rem",
                    }
                ),
                rx.flex(
                    rx.link(
                        rx.el.button(
                            "Start Analysing  →",
                            style=primary_button_style(),
                        ),
                        href="/analyser",
                    ),
                    rx.link(
                        rx.el.button(
                            "View History",
                            style=ghost_button_style(),
                        ),
                        href="/history",
                    ),
                    gap="1.2rem",
                    flex_wrap="wrap",
                    justify_content="center",
                    margin_top="2.5rem",
                ),
                rx.flex(
                    feature_card("🪲", "Bug Detection", "Finds syntax errors, logical flaws, and risky patterns via AST."),
                    feature_card("🎨", "Style Review", "PEP8 compliance, naming, docstrings, and code structure."),
                    feature_card("⚡", "Complexity", "Time & space complexity estimated automatically."),
                    feature_card("🤖", "AI Suggestions", "Groq LLM rewrites problem areas with better code."),
                    gap="1.5rem",
                    flex_wrap="wrap",
                    justify_content="center",
                    margin_top="4rem",
                    max_width="900px",
                ),
                align_items="center",
                spacing="0",
            ),
            padding="5rem 2rem",
            min_height="calc(100vh - 64px)",
        ),
        style=page_style(),
    )


def feature_card(icon: str, title: str, desc: str) -> rx.Component:
    return rx.box(
        rx.el.div(icon, style={"font_size": "1.8rem", "margin_bottom": "0.7rem"}),
        rx.el.h3(title, style={"color": "#e2e8f0", "font_weight": "600", "font_size": "1rem", "margin_bottom": "0.4rem"}),
        rx.el.p(desc, style={"color": "#64748b", "font_size": "0.875rem", "line_height": "1.6"}),
        style={
            "background": "rgba(139, 92, 246, 0.06)",
            "border": "1px solid rgba(139, 92, 246, 0.2)",
            "border_radius": "16px",
            "padding": "1.5rem",
            "width": "200px",
            "text_align": "center",
            "transition": "all 0.3s ease",
            "_hover": {
                "border_color": "rgba(139, 92, 246, 0.5)",
                "background": "rgba(139, 92, 246, 0.12)",
                "transform": "translateY(-4px)",
                "box_shadow": "0 8px 32px rgba(139, 92, 246, 0.2)",
            }
        }
    )


def page_style() -> dict:
    return {
        "background": "#0f0a1e",
        "min_height": "100vh",
        "font_family": "'Inter', 'Segoe UI', sans-serif",
        "color": "#e2e8f0",
    }


def nav_link_style() -> dict:
    return {
        "color": "#94a3b8",
        "text_decoration": "none",
        "font_size": "0.9rem",
        "font_weight": "500",
        "transition": "color 0.2s",
        "_hover": {"color": "#a78bfa"},
    }


def primary_button_style() -> dict:
    return {
        "background": "linear-gradient(135deg, #8b5cf6, #ec4899)",
        "color": "white",
        "border": "none",
        "padding": "0.85rem 2rem",
        "border_radius": "12px",
        "font_size": "1rem",
        "font_weight": "600",
        "cursor": "pointer",
        "transition": "all 0.3s ease",
        "box_shadow": "0 4px 20px rgba(139, 92, 246, 0.4)",
        "_hover": {
            "transform": "translateY(-2px)",
            "box_shadow": "0 8px 30px rgba(139, 92, 246, 0.6)",
        }
    }


def ghost_button_style() -> dict:
    return {
        "background": "transparent",
        "color": "#a78bfa",
        "border": "1px solid rgba(139, 92, 246, 0.4)",
        "padding": "0.85rem 2rem",
        "border_radius": "12px",
        "font_size": "1rem",
        "font_weight": "600",
        "cursor": "pointer",
        "transition": "all 0.3s ease",
        "_hover": {
            "background": "rgba(139, 92, 246, 0.1)",
            "border_color": "#8b5cf6",
        }
    }
