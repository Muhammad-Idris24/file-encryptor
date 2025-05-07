import pytest
from pathlib import Path
from encryptor.core.crypto import CryptoManager
import os

@pytest.fixture
def temp_key_file(tmp_path):
    key_file = tmp_path / "test.key"
    crypto = CryptoManager()
    crypto.save_key(key_file)
    return key_file

def test_key_generation():
    crypto1 = CryptoManager()
    crypto2 = CryptoManager()
    assert crypto1.key != crypto2.key, "Generated keys should be unique"

def test_encryption_decryption():
    crypto = CryptoManager()
    test_data = b"Test data for encryption"
    
    encrypted = crypto.encrypt_data(test_data)
    assert encrypted != test_data, "Encrypted data should differ from original"
    
    decrypted = crypto.decrypt_data(encrypted)
    assert decrypted == test_data, "Decrypted data should match original"

def test_invalid_decryption():
    crypto1 = CryptoManager()
    crypto2 = CryptoManager()
    test_data = b"Test data"
    
    encrypted = crypto1.encrypt_data(test_data)
    with pytest.raises(ValueError):
        crypto2.decrypt_data(encrypted)

def test_key_save_load(temp_key_file):
    original = CryptoManager.load_key(temp_key_file)
    loaded = CryptoManager.load_key(temp_key_file)

    assert original.key == loaded.key, "Loaded key should match saved key"

    # New check: Encrypt with one, decrypt with the other
    encrypted = original.encrypt_data(b"test")
    decrypted = loaded.decrypt_data(encrypted)
    assert decrypted == b"test", "Decrypted data should match original"


def test_key_file_not_found():
    with pytest.raises(FileNotFoundError):
        CryptoManager.load_key("nonexistent.key")