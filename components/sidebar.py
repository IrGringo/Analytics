from nicegui import ui


def sidebar():
    with ui.left_drawer(top_corner=True).classes("bg-grey-2"):

        ui.label("Navigation").classes("text-h6")

        ui.button(
            "🏠 Home",
            on_click=lambda: ui.navigate.to("/")
        )

        ui.button(
            "🌾 Agriculture",
            on_click=lambda: ui.navigate.to("/agriculture")
        )

        ui.button(
            "🛍️ Customer",
            on_click=lambda: ui.navigate.to("/customer")
        )