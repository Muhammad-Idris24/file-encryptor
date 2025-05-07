```markdown
# API Reference

Developer documentation for the File Encryptor package.

## Core Modules

### `encryptor.core.crypto`

```python
class CryptoManager:
    """Handles encryption/decryption operations."""
    
    def __init__(self, key: Optional[bytes] = None):
        """Initialize with optional key."""
    
    def encrypt_data(self, data: bytes) -> bytes:
        """Encrypt raw bytes data."""
    
    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Decrypt encrypted bytes data."""
    
    def save_key(self, key_file: Union[str, Path]):
        """Save the encryption key to a file."""
    
    @classmethod
    def load_key(cls, key_file: Union[str, Path]):
        """Load encryption key from a file."""