import reflex as rx

def navbar() -> rx.Component:
    return rx.flex(
        rx.link(
            rx.hstack(
                rx.icon(tag="code", size=24, color="#38bdf8", stroke_width=2.5),
                rx.heading("Code Reviewer", size="5", weight="bold", color="#e0f2fe", letter_spacing="-0.02em"),
                align_items="center",
                spacing="3",
            ),
            href="/",
            text_decoration="none",
        ),
        rx.hstack(
            rx.link("Home", href="/", color="#bae6fd", font_weight="500", _hover={"color": "#38bdf8", "text_decoration": "none"}),
            rx.link("Review Code", href="/posts", color="#bae6fd", font_weight="500", _hover={"color": "#38bdf8", "text_decoration": "none"}),
            rx.link("Assistant", href="/assistant", color="#bae6fd", font_weight="500", _hover={"color": "#38bdf8", "text_decoration": "none"}),
            rx.link("History", href="/history", color="#bae6fd", font_weight="500", _hover={"color": "#38bdf8", "text_decoration": "none"}),
            rx.link("About", href="/about", color="#bae6fd", font_weight="500", _hover={"color": "#38bdf8", "text_decoration": "none"}),
            spacing="5",
            display={"base": "none", "md": "flex"},
        ),
        rx.hstack(
            rx.link(
                rx.button(
                    "Try the Analyzer",
                    color_scheme="sky",
                    variant="solid",
                    size="2",
                    border_radius="10px",
                    font_weight="600",
                    box_shadow="0 4px 14px rgba(14, 165, 233, 0.4)",
                    _hover={"transform": "translateY(-1px)", "box_shadow": "0 6px 20px rgba(14, 165, 233, 0.5)"},
                ),
                href="/posts",
            ),
            spacing="3",
        ),
        width="100%",
        padding="1rem 1.4rem",
        justify_content="space-between",
        align_items="center",
        border_radius="16px",
        background="linear-gradient(135deg, rgba(8, 20, 48, 0.6) 0%, rgba(5, 14, 34, 0.75) 100%)",
        box_shadow="0 8px 32px rgba(1, 9, 28, 0.4), inset 0 0 0 1px rgba(56, 189, 248, 0.15)",
        backdrop_filter="blur(14px)",
        margin_bottom="2rem",
    )
