from pathlib import Path
from typing import Union, List, Generator
import shutil
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)

class FileOperations:
    """Handles file system operations for encryption/decryption."""
    
    @staticmethod
    def process_file(input_path: Union[str, Path], output_path: Union[str, Path], 
                    process_func, chunk_size: int = 64 * 1024) -> None:
        """
        Process a file in chunks using the provided function.
        
        Args:
            input_path: Path to input file
            output_path: Path to output file
            process_func: Function to process data chunks
            chunk_size: Size of chunks to read/process (bytes)
        """
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        # Create parent directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get file size for progress bar
        total_size = input_path.stat().st_size
        
        with (
            open(input_path, 'rb') as infile,
            open(output_path, 'wb') as outfile,
            tqdm(total=total_size, unit='B', unit_scale=True, 
                 desc=f"Processing {input_path.name}") as pbar
        ):
            while True:
                chunk = infile.read(chunk_size)
                if not chunk:
                    break
                processed_chunk = process_func(chunk)
                outfile.write(processed_chunk)
                pbar.update(len(chunk))
    
    @staticmethod
    def find_files(directory: Union[str, Path], recursive: bool = False, 
                   extensions: List[str] = None) -> Generator[Path, None, None]:
        """
        Find files in a directory, optionally recursively and with specific extensions.
        
        Args:
            directory: Directory to search
            recursive: Whether to search recursively
            extensions: List of file extensions to include (None for all)
            
        Yields:
            Path objects for matching files
        """
        directory = Path(directory)
        if not directory.is_dir():
            raise ValueError(f"{directory} is not a valid directory")
        
        pattern = "**/*" if recursive else "*"
        
        for file_path in directory.glob(pattern):
            if file_path.is_file():
                if extensions is None or file_path.suffix.lower() in extensions:
                    yield file_path
    
    @staticmethod
    def create_output_path(input_path: Union[str, Path], output_dir: Union[str, Path], 
                          suffix: str = "", new_extension: str = None) -> Path:
        """
        Create an output path based on input path and parameters.
        
        Args:
            input_path: Original file path
            output_dir: Directory for output
            suffix: Suffix to add to filename
            new_extension: New file extension (None to keep original)
            
        Returns:
            Path object for output file
        """
        input_path = Path(input_path)
        output_dir = Path(output_dir)
        
        # Create new filename
        new_name = input_path.stem + suffix
        if new_extension:
            new_name += new_extension
        else:
            new_name += input_path.suffix
            
        return output_dir / new_name