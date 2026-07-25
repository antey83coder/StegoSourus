from stego_core import encrypt_payload, decrypt_payload, encode_image, decode_image

# Симуляція ролей та їх прав (як у базі даних бекенду)
ROLES_PERMISSIONS = {
    "Admin": {"can_encrypt": True, "can_decrypt": True},
    "Class 1": {"can_encrypt": True, "can_decrypt": True},
    "Class 2": {"can_encrypt": False, "can_decrypt": True},
    "Class 3": {"can_encrypt": False, "can_decrypt": False}
}

def execute_agent_action(role_name: str, action: str, secret_text: str, group_secret: bytes):
    print(f"\n--- Перевірка прав для ролі: [{role_name}] на дію: [{action}] ---")
    
    permissions = ROLES_PERMISSIONS.get(role_name, {})
    
    if action == "encrypt":
        if not permissions.get("can_encrypt", False):
            print(f"ДОСТУП ЗАБОРОНЕНО: Роль '{role_name}' не має прав на шифрування та приховування даних.")
            return None
        
        print("Права підтверджено. Шифруємо та ховаємо...")
        enc_b64 = encrypt_payload(secret_text, group_secret)
        encode_image("original.jpg", enc_b64, "secure_output_role.png")
        print("Успішно зашито у файл 'secure_output_role.png'")
        return "secure_output_role.png"
        
    elif action == "decrypt":
        if not permissions.get("can_decrypt", False):
            print(f"ДОСТУП ЗАБОРОНЕНО: Роль '{role_name}' не має прав на розшифрування.")
            return None
            
        print("Права підтверджено. Витягуємо та розшифровуємо...")
        extracted_b64 = decode_image("secure_output_role.png")
        final_text = decrypt_payload(extracted_b64, group_secret)
        print(f"Розшифровано: '{final_text}'")
        return final_text

if __name__ == "__main__":
    GROUP_SECRET = b"alpha_team_secret_2026"
    message = "Секретний звіт для командування."
    
    # Тест 1: Спроба агента з роллю Class 3 (яка не має прав на шифрування)
    execute_agent_action("Class 3", "encrypt", message, GROUP_SECRET)
    
    # Тест 2: Агент з роллю Class 1 успішно шифрує
    output_file = execute_agent_action("Class 1", "encrypt", message, GROUP_SECRET)
    
    if output_file:
        # Тест 3: Агент з роллю Class 2 (має право лише читати) успішно розшифровує
        execute_agent_action("Class 2", "decrypt", message, GROUP_SECRET)