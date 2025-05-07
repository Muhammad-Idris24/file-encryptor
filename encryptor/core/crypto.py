from cryptography.fernet import Fernet, InvalidToken
from typing import Union, Optional
import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoManager:
    """Handles encryption/decryption operations using Fernet symmetric encryption."""
    
    def __init__(self, key: Optional[bytes] = None):
        """
        Initialize with an optional key. If no key provided, generates a new one.
        
        Args:
            key: Optional encryption key bytes. If None, generates a new key.
        """
        self.key = key or Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
    
    def encrypt_data(self, data: bytes) -> bytes:
        """Encrypt raw bytes data."""
        return self.cipher_suite.encrypt(data)
    
    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Decrypt encrypted bytes data."""
        try:
            return self.cipher_suite.decrypt(encrypted_data)
        except InvalidToken as e:
            logger.error("Invalid token - possibly wrong key or corrupted data")
            raise ValueError("Decryption failed - invalid key or corrupted data") from e
    
    def save_key(self, key_file: Union[str, Path]):
        """Save the encryption key to a file."""
        key_file = Path(key_file)
        key_file.write_bytes(self.key)
        logger.info(f"Key saved to {key_file}")
    
    @classmethod
    def load_key(cls, key_file: Union[str, Path]):
        """Load encryption key from a file."""
        key_file = Path(key_file)
        if not key_file.exists():
            raise FileNotFoundError(f"Key file {key_file} not found")
        return cls(key_file.read_bytes())