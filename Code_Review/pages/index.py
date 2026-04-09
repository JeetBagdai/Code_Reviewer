import reflex as rx
from Code_Review.components.navbar import navbar
from Code_Review.components.hero import hero
from Code_Review.components.footer import footer

def index() -> rx.Component:
    return rx.box(
        rx.container(
            rx.vstack(
                navbar(),
                hero(),
                footer(),
                spacing="5",
                align="center",
            ),
            max_width="1160px",
            width="100%",
            padding_y="1.6rem",
            padding_x={"base": "1rem", "md": "1.3rem"},
        ),
        width="100%",
        display="flex",
        justify_content="center",
    )
