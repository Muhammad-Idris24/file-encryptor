from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QFileDialog, QLineEdit, 
                            QProgressBar, QMessageBox, QGroupBox, QRadioButton)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pathlib import Path
import sys
from ..core.crypto import CryptoManager
from ..core.file_ops import FileOperations

class EncryptionThread(QThread):
    """Worker thread for encryption/decryption operations."""
    
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, operation, key, input_path, output_dir, recursive, parent=None):
        super().__init__(parent)
        self.operation = operation  # 'encrypt' or 'decrypt'
        self.key = key
        self.input_path = input_path
        self.output_dir = output_dir
        self.recursive = recursive
        self.crypto = CryptoManager(key)
    
    def run(self):
        try:
            if self.operation == 'encrypt':
                process_func = self.crypto.encrypt_data
                suffix = '.enc'
                extensions = None
            else:
                process_func = self.crypto.decrypt_data
                suffix = ''
                extensions = ['.enc']
            
            input_path = Path(self.input_path)
            processed_files = 0
            
            if input_path.is_file():
                output_path = FileOperations.create_output_path(
                    input_path, self.output_dir, suffix
                )
                FileOperations.process_file(input_path, output_path, process_func)
                processed_files = 1
            elif input_path.is_dir():
                for file_path in FileOperations.find_files(
                    input_path, self.recursive, extensions
                ):
                    output_path = FileOperations.create_output_path(
                        file_path, self.output_dir, suffix
                    )
                    FileOperations.process_file(file_path, output_path, process_func)
                    processed_files += 1
            
            self.finished.emit(True, f"Successfully processed {processed_files} files")
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")

class FileEncryptorGUI(QMainWindow):
    """Main application window for the GUI."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Encryptor")
        self.setGeometry(100, 100, 600, 400)
        self._init_ui()
        self.worker_thread = None
    
    def _init_ui(self):
        """Initialize the user interface."""
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        # Operation selection
        self.operation_group = QGroupBox("Operation")
        operation_layout = QHBoxLayout()
        self.encrypt_radio = QRadioButton("Encrypt")
        self.decrypt_radio = QRadioButton("Decrypt")
        self.encrypt_radio.setChecked(True)
        operation_layout.addWidget(self.encrypt_radio)
        operation_layout.addWidget(self.decrypt_radio)
        self.operation_group.setLayout(operation_layout)
        layout.addWidget(self.operation_group)
        
        # Key selection
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("Encryption Key:"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Path to key file or leave empty to generate new")
        key_layout.addWidget(self.key_input)
        browse_key_btn = QPushButton("Browse...")
        browse_key_btn.clicked.connect(self._browse_key_file)
        key_layout.addWidget(browse_key_btn)
        layout.addLayout(key_layout)
        
        # File selection
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Input File/Directory:"))
        self.file_input = QLineEdit()
        file_layout.addWidget(self.file_input)
        browse_file_btn = QPushButton("Browse...")
        browse_file_btn.clicked.connect(self._browse_input)
        file_layout.addWidget(browse_file_btn)
        layout.addLayout(file_layout)
        
        # Output directory
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Output Directory:"))
        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("Defaults to 'encrypted' or 'decrypted'")
        output_layout.addWidget(self.output_input)
        browse_output_btn = QPushButton("Browse...")
        browse_output_btn.clicked.connect(self._browse_output)
        output_layout.addWidget(browse_output_btn)
        layout.addLayout(output_layout)
        
        # Options
        self.recursive_check = QRadioButton("Process directories recursively")
        self.recursive_check.setChecked(True)
        layout.addWidget(self.recursive_check)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress)
        
        # Execute button
        execute_btn = QPushButton("Execute")
        execute_btn.clicked.connect(self._execute)
        layout.addWidget(execute_btn)
        
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
    
    def _browse_key_file(self):
        """Open file dialog to select key file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Key File", "", "Key Files (*.key);;All Files (*)"
        )
        if file_path:
            self.key_input.setText(file_path)
    
    def _browse_input(self):
        """Open file dialog to select input file/directory."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select File or Directory", "", "All Files (*)"
        )
        if path:
            self.file_input.setText(path)
    
    def _browse_output(self):
        """Open file dialog to select output directory."""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_input.setText(dir_path)
    
    def _execute(self):
        """Execute the selected operation."""
        if not self.file_input.text():
            QMessageBox.warning(self, "Error", "Please select an input file or directory")
            return
        
        if self.decrypt_radio.isChecked() and not self.key_input.text():
            QMessageBox.warning(self, "Error", "Decryption requires a key file")
            return
        
        # Set default output directory if not specified
        output_dir = self.output_input.text()
        if not output_dir:
            output_dir = "decrypted" if self.decrypt_radio.isChecked() else "encrypted"
            self.output_input.setText(output_dir)
        
        # Load or generate key
        key = None
        if self.key_input.text():
            try:
                key = Path(self.key_input.text()).read_bytes()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load key: {str(e)}")
                return
        elif self.encrypt_radio.isChecked():
            # Generate new key
            crypto = CryptoManager()
            key = crypto.key
            key_path = Path(output_dir) / "encryption.key"
            try:
                key_path.parent.mkdir(parents=True, exist_ok=True)
                key_path.write_bytes(key)
                QMessageBox.information(
                    self, "New Key Generated", 
                    f"A new encryption key has been generated and saved to:\n{key_path}\n\n"
                    "IMPORTANT: Keep this key safe as it's required for decryption."
                )
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save key: {str(e)}")
                return
        
        # Start worker thread
        operation = 'encrypt' if self.encrypt_radio.isChecked() else 'decrypt'
        self.worker_thread = EncryptionThread(
            operation, key, self.file_input.text(), output_dir, 
            self.recursive_check.isChecked()
        )
        self.worker_thread.finished.connect(self._on_operation_finished)
        self.worker_thread.start()
        
        # Disable UI during operation
        self._set_ui_enabled(False)
    
    def _on_operation_finished(self, success, message):
        """Handle completion of encryption/decryption operation."""
        self._set_ui_enabled(True)
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)
    
    def _set_ui_enabled(self, enabled):
        """Enable or disable UI elements."""
        self.operation_group.setEnabled(enabled)
        self.key_input.setEnabled(enabled)
        self.file_input.setEnabled(enabled)
        self.output_input.setEnabled(enabled)
        self.recursive_check.setEnabled(enabled)

def run_gui():
    """Run the GUI application."""
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = FileEncryptorGUI()
    window.show()
    sys.exit(app.exec_())