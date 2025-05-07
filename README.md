# File Encryptor

A secure file encryption/decryption tool with both CLI and GUI interfaces.

## Features

- Encrypt/decrypt individual files or entire directories
- Secure Fernet symmetric encryption
- Progress visualization with tqdm
- Optional PyQt5 GUI
- Recursive directory processing
- Key management

## Installation

```bash
# Install from PyPI (when published)
pip install file-encryptor

# For GUI support
pip install file-encryptor[gui]

# Install from source
git clone https://github.com/yourusername/file-encryptor.git
cd file-encryptor
pip install .