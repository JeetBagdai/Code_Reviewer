import reflex as rx
from Code_Review.state import AppState
from Code_Review.pages.home import page_style, nav_link_style, primary_button_style


def analyser_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.el.div(
            left_panel(),
            right_panel(),
            style={
                "display": "grid",
                "grid_template_columns": "1fr 1fr",
                "gap": "0",
                "height": "calc(100vh - 64px)",
                "overflow": "hidden",
            }
        ),
        style=page_style(),
    )


def navbar() -> rx.Component:
    return rx.box(
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
                rx.link("Analyser", href="/analyser", style={**nav_link_style(), "color": "#a78bfa"}),
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
            "background": "rgba(15, 10, 30, 0.95)",
            "backdrop_filter": "blur(12px)",
            "height": "64px",
        }
    )


def left_panel() -> rx.Component:
    return rx.box(
        rx.box(
            rx.flex(
                rx.flex(
                    rx.box(style={"width": "12px", "height": "12px", "border_radius": "50%", "background": "#f87171"}),
                    rx.box(style={"width": "12px", "height": "12px", "border_radius": "50%", "background": "#fbbf24"}),
                    rx.box(style={"width": "12px", "height": "12px", "border_radius": "50%", "background": "#34d399"}),
                    gap="6px",
                    align_items="center",
                ),
                rx.el.span(
                    "input.py",
                    style={"color": "#64748b", "font_size": "0.8rem", "font_family": "monospace"}
                ),
                justify_content="space-between",
                align_items="center",
                padding="0.7rem 1rem",
                style={
                    "border_bottom": "1px solid rgba(139, 92, 246, 0.15)",
                    "background": "rgba(139, 92, 246, 0.04)",
                }
            ),
            rx.el.textarea(
                placeholder="# Paste your Python code here...\n\ndef example(x=[]):\n    try:\n        return x[0]\n    except:\n        pass",
                value=AppState.code_input,
                on_change=AppState.set_code,
                style={
                    "width": "100%",
                    "flex": "1",
                    "background": "transparent",
                    "border": "none",
                    "outline": "none",
                    "color": "#c4b5fd",
                    "font_family": "'Fira Code', 'Cascadia Code', monospace",
                    "font_size": "0.9rem",
                    "line_height": "1.7",
                    "padding": "1.2rem",
                    "resize": "none",
                    "height": "calc(100vh - 200px)",
                    "overflow_y": "auto",
                }
            ),
            rx.flex(
                rx.el.button(
                    "✕  Clear",
                    on_click=AppState.clear_code,
                    style={
                        "background": "transparent",
                        "border": "1px solid rgba(139, 92, 246, 0.3)",
                        "color": "#94a3b8",
                        "padding": "0.6rem 1.2rem",
                        "border_radius": "8px",
                        "cursor": "pointer",
                        "font_size": "0.85rem",
                        "transition": "all 0.2s",
                        "_hover": {"border_color": "#8b5cf6", "color": "#a78bfa"},
                    }
                ),
                rx.el.button(
                    rx.cond(AppState.is_loading, "Analysing...", "⚡  Analyse Code"),
                    on_click=AppState.analyse_code,
                    disabled=AppState.is_loading,
                    style={
                        **primary_button_style(),
                        "padding": "0.6rem 1.5rem",
                        "font_size": "0.9rem",
                        "opacity": rx.cond(AppState.is_loading, "0.7", "1"),
                    }
                ),
                gap="0.8rem",
                padding="1rem 1.2rem",
                justify_content="flex-end",
                style={"border_top": "1px solid rgba(139, 92, 246, 0.15)", "background": "rgba(139, 92, 246, 0.04)"},
            ),
            style={
                "display": "flex",
                "flex_direction": "column",
                "height": "100%",
                "border_right": "1px solid rgba(139, 92, 246, 0.2)",
            }
        ),
        style={"background": "#0d0920", "height": "100%", "overflow": "hidden"},
    )


def right_panel() -> rx.Component:
    return rx.box(
        rx.cond(
            AppState.has_review,
            results_view(),
            empty_state(),
        ),
        style={"background": "#100b21", "height": "100%", "overflow_y": "auto"},
    )


def empty_state() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.el.div(
                "◈",
                style={
                    "font_size": "4rem",
                    "color": "rgba(139, 92, 246, 0.2)",
                    "line_height": "1",
                }
            ),
            rx.el.p(
                "Paste code and click Analyse to begin.",
                style={"color": "#475569", "font_size": "0.95rem", "text_align": "center"}
            ),
            align_items="center",
            spacing="4",
        ),
        height="100%",
    )


def results_view() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.el.div(
                rx.el.span("🤖 ", style={"font_size": "1.1rem"}),
                rx.el.span(
                    "AI TECHNICAL REVIEW",
                    style={"color": "#a78bfa", "font_size": "0.75rem", "font_weight": "700", "letter_spacing": "0.15em"}
                ),
                style={"display": "flex", "align_items": "center", "gap": "6px"},
            ),
            rx.el.h2(
                "Code Review",
                style={"color": "#f1f5f9", "font_size": "1.4rem", "font_weight": "700"}
            ),
            rx.el.div(
                AppState.review_summary,
                style={"color": "#94a3b8", "font_size": "0.875rem", "font_style": "italic", "line_height": "1.6"}
            ),
            section_divider(),
            section_heading("🪲", "Bugs Detected"),
            rx.cond(
                AppState.review_bugs,
                rx.vstack(
                    rx.foreach(
                        AppState.review_bugs,
                        lambda bug: rx.box(
                            rx.el.span("▸ ", style={"color": "#f87171"}),
                            rx.el.span(bug, style={"color": "#fca5a5"}),
                            style={"font_size": "0.875rem", "line_height": "1.6", "padding": "0.3rem 0"}
                        )
                    ),
                    align_items="flex-start",
                    spacing="1",
                ),
                rx.el.p("No bugs detected.", style={"color": "#34d399", "font_size": "0.875rem"}),
            ),
            section_divider(),
            section_heading("📊", "Complexity"),
            rx.flex(
                complexity_badge("Time", AppState.review_time_complexity),
                complexity_badge("Space", AppState.review_space_complexity),
                gap="1rem",
            ),
            section_divider(),
            section_heading("🎨", "Code Quality Issues"),
            rx.cond(
                AppState.review_quality,
                rx.vstack(
                    rx.foreach(
                        AppState.review_quality,
                        lambda issue: rx.box(
                            rx.el.span("• ", style={"color": "#fbbf24"}),
                            rx.el.span(issue, style={"color": "#fde68a"}),
                            style={"font_size": "0.875rem", "line_height": "1.6", "padding": "0.3rem 0"}
                        )
                    ),
                    align_items="flex-start",
                    spacing="1",
                ),
                rx.el.p("No quality issues found.", style={"color": "#34d399", "font_size": "0.875rem"}),
            ),
            section_divider(),
            section_heading("✨", "Improvements"),
            rx.box(
                rx.el.pre(
                    AppState.review_improvements,
                    style={
                        "white_space": "pre-wrap",
                        "word_break": "break-word",
                        "color": "#c4b5fd",
                        "font_family": "'Fira Code', monospace",
                        "font_size": "0.82rem",
                        "line_height": "1.7",
                        "margin": "0",
                    }
                ),
                style={
                    "background": "rgba(139, 92, 246, 0.06)",
                    "border": "1px solid rgba(139, 92, 246, 0.2)",
                    "border_radius": "12px",
                    "padding": "1rem",
                    "overflow_x": "auto",
                    "width": "100%",
                }
            ),
            align_items="flex-start",
            spacing="4",
            width="100%",
        ),
        padding="2rem",
    )


def section_heading(icon: str, title: str) -> rx.Component:
    return rx.flex(
        rx.el.span(icon, style={"font_size": "1rem"}),
        rx.el.span(
            title,
            style={"color": "#cbd5e1", "font_weight": "600", "font_size": "0.9rem", "letter_spacing": "0.05em"}
        ),
        align_items="center",
        gap="8px",
    )


def section_divider() -> rx.Component:
    return rx.el.hr(style={"border_color": "rgba(139, 92, 246, 0.15)", "margin": "0.5rem 0", "width": "100%"})


def complexity_badge(label: str, value) -> rx.Component:
    return rx.box(
        rx.el.span(label, style={"color": "#64748b", "font_size": "0.75rem", "display": "block", "margin_bottom": "4px"}),
        rx.el.span(value, style={"color": "#a78bfa", "font_weight": "700", "font_size": "1.1rem", "font_family": "monospace"}),
        style={
            "background": "rgba(139, 92, 246, 0.08)",
            "border": "1px solid rgba(139, 92, 246, 0.25)",
            "border_radius": "10px",
            "padding": "0.6rem 1.2rem",
        }
    )
