import os
import hashlib
import base64

SECRET_KEY = b'ThereIsNoSecretHere'

def _derive_stream_key(iv: bytes) -> bytes:
    """Génère une clé pseudo-aléatoire à partir de l'IV et la clé secrète"""
    return hashlib.sha256(SECRET_KEY + iv).digest()

def encrypt_message(message: str) -> str:
    iv = os.urandom(16)  
    key_stream = _derive_stream_key(iv)
    
    encrypted_bytes = bytes(
        ord(char) ^ key_stream[i % len(key_stream)] for i, char in enumerate(message)
    )
    
    combined = iv + encrypted_bytes
    return base64.b64encode(combined).decode('utf-8')

def decrypt_message(cipher_b64: str) -> str:
    combined = base64.b64decode(cipher_b64)
    iv = combined[:16]
    encrypted_bytes = combined[16:]
    
    key_stream = _derive_stream_key(iv)

    decrypted = ''.join(
        chr(byte ^ key_stream[i % len(key_stream)]) for i, byte in enumerate(encrypted_bytes)
    )
    return decrypted
