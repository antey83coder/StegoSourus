from cryptography.fernet import Fernet
from PIL import Image
import hashlib
import base64

def get_encryption_key(group_secret: bytes) -> bytes:
    digest = hashlib.sha256(group_secret).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt_payload(secret_text: str, group_secret: bytes) -> str:
    key = get_encryption_key(group_secret)
    cipher = Fernet(key)
    encrypted_bytes = cipher.encrypt(secret_text.encode('utf-8'))
    return encrypted_bytes.decode('utf-8')

def decrypt_payload(encrypted_b64: str, group_secret: bytes) -> str:
    key = get_encryption_key(group_secret)
    cipher = Fernet(key)
    decrypted_bytes = cipher.decrypt(encrypted_b64.encode('utf-8'))
    return decrypted_bytes.decode('utf-8')

def encode_image(image_path: str, encrypted_b64: str, output_path: str):
    image = Image.open(image_path).convert("RGB")
    payload = encrypted_b64 + "###END###"
    binary_data = ''.join(format(ord(c), '08b') for c in payload)
    
    pixels = image.load()
    width, height = image.size
    
    if len(binary_data) > width * height * 3:
        raise ValueError("Повідомлення завелике для цієї картинки!")
        
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
            
    image.save(output_path)

def decode_image(image_path: str) -> str:
    read_image = Image.open(image_path).convert("RGB")
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
            return msg[:-9]
            
    raise ValueError("Стоп-маркер не знайдено в зображенні!")