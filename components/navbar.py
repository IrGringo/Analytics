from nicegui import ui

def navbar():
    with ui.row().classes("gap-4"):
            
            ui.button(
                "Home",
                on_click=lambda: ui.navigate.to("/")
            )

            ui.button(
                "Finance",
                on_click=lambda: ui.navigate.to("/finance")
            )

            ui.button(
                "Seasonality",
                on_click=lambda: ui.navigate.to("/agriculture")
            )

            ui.button(
                "Customer",
                on_click=lambda: ui.navigate.to("/customer")
            )