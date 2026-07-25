from cryptography.fernet import Fernet
from PIL import Image
import hashlib
import base64

def get_encryption_key(group_secret: bytes) -> bytes:
    digest = hashlib.sha256(group_secret).digest()
    return base64.urlsafe_b64encode(digest)

def run_secure_stego_with_keys():
    print("=== АВТОНОМНИЙ СТЕГАНО-МОДУЛЬ З КЛЮЧОВОЮ СИСТЕМОЮ ===")
    
    GROUP_MASTER_SECRET = b"alpha_team_secret_2026"
    
    secret_text = "Координати цілі підтверджено. Починаємо роботу."
    print(f"1. Повідомлення: '{secret_text}'")
    
    encryption_key = get_encryption_key(GROUP_MASTER_SECRET)
    cipher = Fernet(encryption_key)
    
    encrypted_bytes = cipher.encrypt(secret_text.encode('utf-8'))
    encrypted_b64 = encrypted_bytes.decode('utf-8')
    
    input_img = "original.jpg"
    output_img = "secure_output_keyed.png"
    
    try:
        image = Image.open(input_img).convert("RGB")
    except FileNotFoundError:
        print(f"Помилка: Не знайдено файл '{input_img}'!")
        return
        
    payload = encrypted_b64 + "###END###"
    binary_data = ''.join(format(ord(c), '08b') for c in payload)
    
    pixels = image.load()
    width, height = image.size
    
    if len(binary_data) > width * height * 3:
        print("Помилка: Повідомлення завелике для цієї картинки!")
        return
        
    data_idx = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if data_idx < len(binary_data):
                r = (r & ~1) | int(binary_data[data_idx]); data_idx += 1
            if data_idx < len(binary_data):
                g = (g & ~1) | int(binary_data[data_idx]); data_idx += 1
            if data_idx < len(binary_data):
                b = (b & ~1) | int(binary_data[data_idx]); data_idx += 1
            pixels[x, y] = (r, g, b)
            if data_idx >= len(binary_data):
                break
        if data_idx >= len(binary_data):
            break
            
    image.save(output_img)
    print(f"2. Зашито у файл з ключовим захистом: '{output_img}'")
    
    read_image = Image.open(output_img).convert("RGB")
    read_pixels = read_image.load()
    rw, rh = read_image.size
    
    extracted_bits = ""
    for y in range(rh):
        for x in range(rw):
            r, g, b = read_pixels[x, y]
            extracted_bits += str(r & 1) + str(g & 1) + str(b & 1)
            
    all_bytes = [extracted_bits[i:i+8] for i in range(0, len(extracted_bits), 8)]
    chars = []
    for b in all_bytes:
        chars.append(chr(int(b, 2)))
        msg = "".join(chars)
        if msg.endswith("###END###"):
            extracted_b64 = msg[:-9]
            break
            
    decryption_key = get_encryption_key(GROUP_MASTER_SECRET)
    receiver_cipher = Fernet(decryption_key)
    
    decrypted_bytes = receiver_cipher.decrypt(extracted_b64.encode('utf-8'))
    final_text = decrypted_bytes.decode('utf-8')
    
    print(f"3. Успішно розшифровано за груповим ключем: '{final_text}'")
    print("=== КЛЮЧОВИЙ ЦИКЛ ЗАВЕРШЕНО УСПІШНО ===")

if __name__ == "__main__":
    run_secure_stego_with_keys()