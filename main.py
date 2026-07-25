import flet as ft
from stego_core import encrypt_payload, decrypt_payload, encode_image, decode_image
import os

# Ролі та їх права (без Class 3)
ROLES_PERMISSIONS = {
    "Admin": {"can_encrypt": True, "can_decrypt": True},
    "Class 1": {"can_encrypt": True, "can_decrypt": True},
    "Class 2": {"can_encrypt": False, "can_decrypt": True}
}

GROUP_SECRET = b"alpha_team_secret_2026"

def main(page: ft.Page):
    page.title = "StegoSourus - Secure Terminal"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 500
    page.window_height = 700
    page.padding = 20

    # Елементи інтерфейсу
    role_dropdown = ft.Dropdown(
        label="Виберіть роль агента",
        options=[
            ft.dropdown.Option("Admin"),
            ft.dropdown.Option("Class 1"),
            ft.dropdown.Option("Class 2"),
        ],
        value="Class 1",
        width=400
    )

    message_input = ft.TextField(
        label="Секретне повідомлення",
        multiline=True,
        min_lines=2,
        max_lines=4,
        width=400
    )

    image_path_input = ft.TextField(
        label="Шлях до зображення (наприклад, original.jpg)",
        value="original.jpg",
        width=400
    )

    status_output = ft.Text(value="Статус: Готово до роботи", color="blue", weight=ft.FontWeight.BOLD)
    result_output = ft.Text(value="", selectable=True, width=400)

    def on_encrypt_click(e):
        role = role_dropdown.value
        msg = message_input.value
        img_path = image_path_input.value

        perms = ROLES_PERMISSIONS.get(role, {})
        if not perms.get("can_encrypt", False):
            status_output.value = f"ПОМИЛКА: Роль '{role}' не має прав на шифрування!"
            status_output.color = "red"
            result_output.value = ""
            page.update()
            return

        if not msg:
            status_output.value = "ПОМИЛКА: Введіть текст повідомлення!"
            status_output.color = "red"
            page.update()
            return

        if not os.path.exists(img_path):
            status_output.value = f"ПОМИЛКА: Файл '{img_path}' не знайдено!"
            status_output.color = "red"
            page.update()
            return

        try:
            enc_b64 = encrypt_payload(msg, GROUP_SECRET)
            output_img = "secure_output_gui.png"
            encode_image(img_path, enc_b64, output_img)
            
            status_output.value = f"Успішно зашито у файл: {output_img}"
            status_output.color = "green"
            result_output.value = f"Зашифрований payload: {enc_b64[:40]}..."
        except Exception as ex:
            status_output.value = f"Помилка виконання: {str(ex)}"
            status_output.color = "red"
        
        page.update()

    def on_decrypt_click(e):
        role = role_dropdown.value
        output_img = "secure_output_gui.png"

        perms = ROLES_PERMISSIONS.get(role, {})
        if not perms.get("can_decrypt", False):
            status_output.value = f"ПОМИЛКА: Роль '{role}' не має прав на дешифрування!"
            status_output.color = "red"
            result_output.value = ""
            page.update()
            return

        if not os.path.exists(output_img):
            status_output.value = f"ПОМИЛКА: Файл '{output_img}' відсутній для читання!"
            status_output.color = "red"
            page.update()
            return

        try:
            extracted_b64 = decode_image(output_img)
            final_text = decrypt_payload(extracted_b64, GROUP_SECRET)
            
            status_output.value = "Успішно витягнуто та розшифровано!"
            status_output.color = "green"
            result_output.value = f"Розшифрований текст: {final_text}"
        except Exception as ex:
            status_output.value = f"Помилка розшифрування: {str(ex)}"
            status_output.color = "red"

        page.update()

    encrypt_btn = ft.ElevatedButton("Зашифрувати і сховати", on_click=on_encrypt_click, color="white", bgcolor="indigo")
    decrypt_btn = ft.ElevatedButton("Витягнути і розшифрувати", on_click=on_decrypt_click, color="white", bgcolor="teal")

    page.add(
        ft.Text("StegoSourus Terminal", size=22, weight=ft.FontWeight.BOLD),
        role_dropdown,
        image_path_input,
        message_input,
        ft.Row([encrypt_btn, decrypt_btn], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        status_output,
        result_output
    )

if __name__ == "__main__":
    ft.app(target=main)