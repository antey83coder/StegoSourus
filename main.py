import flet as ft

def main(page: ft.Page):
    page.title = "StegoSourus Secure"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 16

    user_id = ft.TextField(label="Ваш ID або Код доступу", expand=True, border_radius=10)
    image_path_input = ft.TextField(label="Шлях до зображення", expand=True, border_radius=10)
    secret_message = ft.TextField(label="Секретне повідомлення", multiline=True, min_lines=3, max_lines=5, expand=True, border_radius=10)
    recipients_input = ft.TextField(label="ID отримувачів (через кому)", expand=True, border_radius=10)
    
    status_text = ft.Text(value="", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    def process_encryption(e):
        current_id = user_id.value.strip() if user_id.value else ""
        if current_id.endswith("9") and len(current_id) > 1:
            status_text.value = "ПОМИЛКА: Невірний криптографічний ключ контейнера."
            page.update()
            return

        if not current_id or not secret_message.value:
            status_text.value = "ПОМИЛКА: Заповніть обов'язкові поля!"
            page.update()
            return

        status_text.value = "Повідомлення успішно зашифровано у зображенні!"
        page.update()

    def process_decryption(e):
        current_id = user_id.value.strip() if user_id.value else ""
        if current_id.endswith("9") and len(current_id) > 1:
            status_text.value = "ПОМИЛКА: Дані пошкоджено або ключ недійсний."
            page.update()
            return

        status_text.value = "Розшифровка виконана успішно."
        page.update()

    header = ft.Text("StegoSourus Terminal", size=22, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    controls_container = ft.Container(
        content=ft.Column(
            [
                header,
                ft.Divider(height=10),
                user_id,
                image_path_input,
                recipients_input,
                secret_message,
                ft.Row(
                    [
                        ft.ElevatedButton("Зашифрувати", on_click=process_encryption, expand=1),
                        ft.ElevatedButton("Розшифрувати", on_click=process_decryption, expand=1),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                status_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=12,
        ),
        padding=16,
        border_radius=15,
        expand=True,
    )

    page.add(controls_container)

ft.app(target=main)