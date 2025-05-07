# 🧰 Command-Line Interface (CLI) Usage

The CLI allows you to encrypt and decrypt files directly from the terminal.

## 🔑 Generate a Key

```bash
file-encryptor generate-key -o mykey.key

## 🔑 Encrypt a file

```bash
file-encryptor encrypt myfile.txt -o encrypted/ -k mykey.key

## 🔑 Encrypt a directory recursively

```bash
file-encryptor encrypt mydir/ -r -o encrypted/ -k mykey.key

## 🔑 Decrypt a file

```bash
file-encryptor decrypt myfile.txt.enc -o decrypted/ -k mykey.key


## Installation

```bash
pip install file-encryptor