import pytest
from pathlib import Path
from encryptor.core.file_ops import FileOperations
import shutil
import os

@pytest.fixture
def test_dir(tmp_path):
    # Create test directory structure
    (tmp_path / "file1.txt").write_text("Test file 1")
    (tmp_path / "file2.txt").write_text("Test file 2")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "file3.txt").write_text("Test file 3")
    (tmp_path / "file4.dat").write_bytes(b"\x00\x01\x02\x03")
    return tmp_path

def test_process_file(tmp_path, test_dir):
    input_file = test_dir / "file1.txt"
    output_file = tmp_path / "processed.txt"
    
    def uppercase(chunk):
        return chunk.decode().upper().encode()
    
    FileOperations.process_file(input_file, output_file, uppercase)
    
    assert output_file.exists()
    assert output_file.read_text() == "TEST FILE 1"

def test_find_files_non_recursive(test_dir):
    files = list(FileOperations.find_files(test_dir))
    assert len(files) == 3  # file1.txt, file2.txt, file4.dat
    assert all(f.name in ["file1.txt", "file2.txt", "file4.dat"] for f in files)

def test_find_files_recursive(test_dir):
    files = list(FileOperations.find_files(test_dir, recursive=True))
    assert len(files) == 4  # Includes subdir/file3.txt
    assert any(f.name == "file3.txt" for f in files)

def test_find_files_with_extensions(test_dir):
    files = list(FileOperations.find_files(test_dir, extensions=[".txt"]))
    assert len(files) == 2
    assert all(f.suffix == ".txt" for f in files)

def test_create_output_path(test_dir):
    input_path = test_dir / "subdir" / "file3.txt"
    output_path = FileOperations.create_output_path(
        input_path, "output", "_backup", ".enc"
    )
    assert output_path.as_posix() == "output/file3_backup.enc"
