import argparse
from pathlib import Path
import sys
import os
from typing import Optional
from ..core.crypto import CryptoManager
from ..core.file_ops import FileOperations
import logging
from getpass import getpass

logger = logging.getLogger(__name__)

class FileEncryptorCLI:
    """Command-line interface for file encryption/decryption."""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser with all commands and options."""
        parser = argparse.ArgumentParser(
            description="File Encryption/Decryption Tool",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest='command', required=True)
        
        # Encrypt command
        encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt files')
        encrypt_parser.add_argument('paths', nargs='+', help='Files or directories to encrypt')
        encrypt_parser.add_argument('-o', '--output', help='Output directory', default='encrypted')
        encrypt_parser.add_argument('-k', '--key', help='Encryption key file')
        encrypt_parser.add_argument('-r', '--recursive', action='store_true', 
                                  help='Process directories recursively')
        encrypt_parser.add_argument('--ext', help='File extensions to process (comma-separated)')
        
        # Decrypt command
        decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt files')
        decrypt_parser.add_argument('paths', nargs='+', help='Files or directories to decrypt')
        decrypt_parser.add_argument('-o', '--output', help='Output directory', default='decrypted')
        decrypt_parser.add_argument('-k', '--key', help='Encryption key file (required)')
        decrypt_parser.add_argument('-r', '--recursive', action='store_true', 
                                  help='Process directories recursively')
        decrypt_parser.add_argument('--ext', help='File extensions to process (comma-separated)')
        
        # Key generation command
        key_parser = subparsers.add_parser('generate-key', help='Generate a new encryption key')
        key_parser.add_argument('-o', '--output', help='Output key file', default='encryption.key')
        
        return parser
    
    def run(self):
        """Parse arguments and execute appropriate command."""
        args = self.parser.parse_args()
        
        try:
            if args.command == 'generate-key':
                self._generate_key(args)
            elif args.command == 'encrypt':
                self._encrypt(args)
            elif args.command == 'decrypt':
                self._decrypt(args)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            sys.exit(1)
    
    def _generate_key(self, args):
        """Handle key generation command."""
        crypto = CryptoManager()
        crypto.save_key(args.output)
        print(f"New encryption key generated and saved to {args.output}")
        print("IMPORTANT: Keep this key secure and don't lose it!")
    
    def _encrypt(self, args):
        """Handle encryption command."""
        # Load or create key
        if args.key:
            crypto = CryptoManager.load_key(args.key)
        else:
            crypto = CryptoManager()
            key_path = Path(args.output) / 'encryption.key'
            crypto.save_key(key_path)
            print(f"New key generated and saved to {key_path}")
        
        # Process files
        extensions = args.ext.split(',') if args.ext else None
        processed_files = 0
        
        for path in args.paths:
            path = Path(path)
            if path.is_file():
                self._process_single_file(path, args.output, crypto.encrypt_data, '.enc')
                processed_files += 1
            elif path.is_dir():
                processed_files += self._process_directory(
                    path, args.output, crypto.encrypt_data, '.enc', 
                    args.recursive, extensions
                )
        
        print(f"\nEncryption complete. {processed_files} files processed.")
        if not args.key:
            print(f"IMPORTANT: Your encryption key is at {key_path}")
    
    def _decrypt(self, args):
        """Handle decryption command."""
        if not args.key:
            raise ValueError("Decryption requires a key file. Use -k/--key option.")
        
        crypto = CryptoManager.load_key(args.key)
        extensions = ['.enc'] if not args.ext else args.ext.split(',')
        processed_files = 0
        
        for path in args.paths:
            path = Path(path)
            if path.is_file():
                self._process_single_file(path, args.output, crypto.decrypt_data, '')
                processed_files += 1
            elif path.is_dir():
                processed_files += self._process_directory(
                    path, args.output, crypto.decrypt_data, '', 
                    args.recursive, extensions
                )
        
        print(f"\nDecryption complete. {processed_files} files processed.")
    
    def _process_single_file(self, input_path: Path, output_dir: str, 
                           process_func, suffix: str) -> None:
        """Process a single file with the given function."""
        output_path = FileOperations.create_output_path(
            input_path, output_dir, suffix
        )
        print(f"Processing {input_path} -> {output_path}")
        FileOperations.process_file(input_path, output_path, process_func)
    
    def _process_directory(self, directory: Path, output_dir: str, 
                         process_func, suffix: str, 
                         recursive: bool, extensions: list) -> int:
        """Process all files in a directory matching criteria."""
        processed_count = 0
        output_dir = Path(output_dir) / directory.name
        
        for file_path in FileOperations.find_files(
            directory, recursive, extensions
        ):
            output_path = FileOperations.create_output_path(
                file_path, output_dir, suffix
            )
            print(f"Processing {file_path} -> {output_path}")
            FileOperations.process_file(file_path, output_path, process_func)
            processed_count += 1
        
        return processed_count

def main():
    """Entry point for command-line interface."""
    cli = FileEncryptorCLI()
    cli.run()

if __name__ == '__main__':
    main()