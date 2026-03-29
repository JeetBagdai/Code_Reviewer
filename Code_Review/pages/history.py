import reflex as rx
from Code_Review.state import AppState
from Code_Review.pages.home import page_style, nav_link_style


def history_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.el.div(
            history_panel(),
            chat_panel(),
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
                rx.link("Analyser", href="/analyser", style=nav_link_style()),
                rx.link("History", href="/history", style={**nav_link_style(), "color": "#a78bfa"}),
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


def history_panel() -> rx.Component:
    return rx.box(
        rx.box(
            rx.flex(
                rx.el.h2(
                    "ANALYSIS HISTORY",
                    style={"color": "#a78bfa", "font_size": "0.75rem", "font_weight": "700", "letter_spacing": "0.15em"}
                ),
                rx.el.button(
                    "Clear All",
                    on_click=AppState.clear_history,
                    style={
                        "background": "transparent",
                        "border": "1px solid rgba(248, 113, 113, 0.3)",
                        "color": "#f87171",
                        "padding": "0.3rem 0.8rem",
                        "border_radius": "6px",
                        "cursor": "pointer",
                        "font_size": "0.8rem",
                        "transition": "all 0.2s",
                        "_hover": {"background": "rgba(248, 113, 113, 0.1)", "border_color": "#f87171"},
                    }
                ),
                justify_content="space-between",
                align_items="center",
                padding="1rem 1.5rem",
                style={"border_bottom": "1px solid rgba(139, 92, 246, 0.15)"},
            ),
            rx.cond(
                AppState.history,
                rx.box(
                    rx.foreach(
                        AppState.history,
                        history_card,
                    ),
                    style={"overflow_y": "auto", "height": "calc(100vh - 130px)", "padding": "0.75rem"},
                ),
                rx.center(
                    rx.vstack(
                        rx.el.div("📋", style={"font_size": "2.5rem"}),
                        rx.el.p(
                            "No analysis history yet.",
                            style={"color": "#475569", "font_size": "0.9rem"}
                        ),
                        align_items="center",
                        spacing="3",
                    ),
                    height="calc(100vh - 130px)",
                ),
            ),
            style={"height": "100%", "display": "flex", "flex_direction": "column"},
        ),
        style={
            "background": "#0d0920",
            "border_right": "1px solid rgba(139, 92, 246, 0.2)",
            "height": "100%",
            "overflow": "hidden",
        }
    )


def history_card(item: dict) -> rx.Component:
    return rx.box(
        rx.flex(
            rx.el.span(
                item["timestamp"],
                style={"color": "#64748b", "font_size": "0.75rem"}
            ),
            rx.box(
                rx.el.span(item["score"], style={"font_weight": "700", "font_size": "0.85rem"}),
                rx.el.span("/100", style={"color": "#64748b", "font_size": "0.7rem"}),
                style={
                    "background": "rgba(139, 92, 246, 0.15)",
                    "border": "1px solid rgba(139, 92, 246, 0.3)",
                    "color": "#c4b5fd",
                    "padding": "0.2rem 0.6rem",
                    "border_radius": "20px",
                    "display": "flex",
                    "align_items": "center",
                    "gap": "2px",
                }
            ),
            justify_content="space-between",
            align_items="center",
            margin_bottom="0.5rem",
        ),
        rx.el.p(
            item["snippet"],
            style={
                "color": "#94a3b8",
                "font_size": "0.78rem",
                "font_family": "monospace",
                "white_space": "nowrap",
                "overflow": "hidden",
                "text_overflow": "ellipsis",
                "margin_bottom": "0.6rem",
            }
        ),
        rx.flex(
            rx.el.span(
                item["language"],
                style={
                    "background": "#6d28d933",
                    "color": "#e2e8f0",
                    "font_size": "0.7rem",
                    "padding": "0.2rem 0.5rem",
                    "border_radius": "4px",
                    "font_family": "monospace",
                }
            ),
            rx.el.span(
                item["complexity"],
                style={
                    "background": "#1e40af33",
                    "color": "#e2e8f0",
                    "font_size": "0.7rem",
                    "padding": "0.2rem 0.5rem",
                    "border_radius": "4px",
                    "font_family": "monospace",
                }
            ),
            gap="0.5rem",
        ),
        style={
            "background": "rgba(139, 92, 246, 0.06)",
            "border": "1px solid rgba(139, 92, 246, 0.15)",
            "border_radius": "12px",
            "padding": "1rem",
            "margin_bottom": "0.75rem",
            "cursor": "pointer",
            "transition": "all 0.2s",
            "_hover": {
                "background": "rgba(139, 92, 246, 0.12)",
                "border_color": "rgba(139, 92, 246, 0.4)",
                "transform": "translateX(4px)",
            }
        }
    )


def chat_panel() -> rx.Component:
    return rx.box(
        rx.box(
            rx.flex(
                rx.el.div("🤖", style={"font_size": "1.1rem"}),
                rx.el.h2(
                    "AI Code Assistant",
                    style={"color": "#e2e8f0", "font_size": "0.95rem", "font_weight": "600"}
                ),
                align_items="center",
                gap="0.5rem",
                padding="1rem 1.5rem",
                style={"border_bottom": "1px solid rgba(139, 92, 246, 0.15)"},
            ),
            rx.box(
                rx.cond(
                    AppState.chat_messages,
                    rx.vstack(
                        rx.foreach(
                            AppState.chat_messages,
                            chat_bubble,
                        ),
                        align_items="stretch",
                        spacing="3",
                        padding="1rem",
                    ),
                    rx.center(
                        rx.vstack(
                            rx.el.div("💬", style={"font_size": "2rem"}),
                            rx.el.p(
                                "Select a history item and ask questions about the code.",
                                style={"color": "#475569", "font_size": "0.85rem", "text_align": "center", "max_width": "240px"}
                            ),
                            align_items="center",
                            spacing="3",
                        ),
                        height="100%",
                    ),
                ),
                style={
                    "flex": "1",
                    "overflow_y": "auto",
                    "height": "calc(100vh - 190px)",
                }
            ),
            rx.box(
                rx.flex(
                    rx.el.input(
                        placeholder="Ask about the code...",
                        value=AppState.chat_input,
                        on_change=AppState.set_chat_input,
                        on_key_down=AppState.handle_chat_key,
                        style={
                            "flex": "1",
                            "background": "rgba(139, 92, 246, 0.06)",
                            "border": "1px solid rgba(139, 92, 246, 0.2)",
                            "border_radius": "10px",
                            "padding": "0.7rem 1rem",
                            "color": "#e2e8f0",
                            "font_size": "0.875rem",
                            "outline": "none",
                            "_placeholder": {"color": "#475569"},
                            "_focus": {"border_color": "#8b5cf6"},
                        }
                    ),
                    rx.el.button(
                        rx.cond(AppState.is_chat_loading, "...", "→"),
                        on_click=AppState.send_chat_message,
                        disabled=AppState.is_chat_loading,
                        style={
                            "background": "linear-gradient(135deg, #8b5cf6, #ec4899)",
                            "border": "none",
                            "color": "white",
                            "width": "40px",
                            "height": "40px",
                            "border_radius": "10px",
                            "cursor": "pointer",
                            "font_size": "1.1rem",
                            "font_weight": "bold",
                            "transition": "all 0.2s",
                            "_hover": {"opacity": "0.85", "transform": "scale(1.05)"},
                            "flex_shrink": "0",
                        }
                    ),
                    gap="0.5rem",
                    align_items="center",
                ),
                padding="0.75rem 1rem",
                style={"border_top": "1px solid rgba(139, 92, 246, 0.15)", "background": "rgba(139, 92, 246, 0.03)"},
            ),
            style={
                "display": "flex",
                "flex_direction": "column",
                "height": "100%",
            }
        ),
        style={"background": "#100b21", "height": "100%", "overflow": "hidden"}
    )


def chat_bubble(msg: dict) -> rx.Component:
    return rx.box(
        rx.el.div(
            msg["content"],
            style={
                "font_size": "0.875rem",
                "line_height": "1.6",
                "white_space": "pre-wrap",
                "word_break": "break-word",
            }
        ),
        style={
            "background": rx.cond(
                msg["role"] == "user",
                "linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(236, 72, 153, 0.2))",
                "rgba(139, 92, 246, 0.07)"
            ),
            "border": rx.cond(
                msg["role"] == "user",
                "1px solid rgba(139, 92, 246, 0.3)",
                "1px solid rgba(139, 92, 246, 0.12)"
            ),
            "border_radius": "12px",
            "padding": "0.75rem 1rem",
            "margin_left": rx.cond(msg["role"] == "user", "2rem", "0"),
            "margin_right": rx.cond(msg["role"] == "user", "0", "2rem"),
            "color": rx.cond(msg["role"] == "user", "#ddd6fe", "#94a3b8"),
        }
    )
