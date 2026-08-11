import flet as ft
from cryptography.fernet import Fernet
import os

def main(page: ft.Page):
    page.title = "StegoSourus Secure"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.padding = ft.padding.all(16)

    # Локальний стан користувача та бази ID
    user_id = ft.TextField(label="Ваш ID або Код доступу", width=300, border_radius=10)
    image_path_input = ft.TextField(label="Шлях до зображення (наприклад, original.jpg)", width=300, border_radius=10)
    secret_message = ft.TextField(label="Секретне повідомлення", multiline=True, min_lines=3, max_lines=5, width=300, border_radius=10)
    recipients_input = ft.TextField(label="ID отримувачів (через кому)", width=300, border_radius=10)
    
    status_text = ft.Text(value="", color=ft.colors.RED_400, weight=ft.FontWeight.BOLD)

    def process_encryption(e):
        # Перевірка на «код полону» (наприклад, якщо ID закінчується на дев'ятку замість нуля — симулюємо компрометацію)
        current_id = user_id.value.strip()
        if current_id.endswith("9") and len(current_id) > 1:
            status_text.value = "ПОМИЛКА: Невірний криптографічний ключ контейнера."
            status_text.color = ft.colors.RED_400
            # Тут спрацьовує прихований тривожний сигнал
            print("УВАГА: Зафіксовано ввід коду примусу/полону для абонента!")
            page.update()
            return

        if not current_id or not secret_message.value:
            status_text.value = "ПОМИЛКА: Заповніть обов'язкові поля!"
            status_text.color = ft.colors.RED_400
            page.update()
            return

        # Імітація процесу стеганографічного приховування
        status_text.value = "Повідомлення успішно зашифровано у зображенні!"
        status_text.color = ft.colors.GREEN_400
        page.update()

    def process_decryption(e):
        current_id = user_id.value.strip()
        if current_id.endswith("9") and len(current_id) > 1:
            status_text.value = "ПОМИЛКА: Дані пошкоджено або ключ недійсний."
            status_text.color = ft.colors.RED_400
            print("УВАГА: Полон при розшифровці!")
            page.update()
            return

        status_text.value = "Розшифровка виконана успішно."
        status_text.color = ft.colors.GREEN_400
        page.update()

    # Адаптивний інтерфейс з відносними відступами
    header = ft.Text("StegoSourus Terminal", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    controls_container = ft.Container(
        content=ft.Column(
            [
                header,
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                user_id,
                image_path_input,
                recipients_input,
                secret_message,
                ft.Row(
                    [
                        ft.ElevatedButton("Зашифрувати", on_click=process_encryption, bgcolor=ft.colors.INDIGO_700, color=ft.colors.WHITE),
                        ft.ElevatedButton("Розшифрувати", on_click=process_decryption, bgcolor=ft.colors.TEAL_700, color=ft.colors.WHITE),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    width=300,
                ),
                status_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        padding=20,
        border_radius=15,
        bgcolor=ft.colors.SURFACE_VARIANT,
        alignment=ft.alignment.center,
    )

    page.add(controls_container)

ft.app(target=main)