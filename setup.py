from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="file_encryptor",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A secure file encryption/decryption tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/file-encryptor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "cryptography>=3.4",
        "tqdm>=4.0",
    ],
    extras_require={
        "gui": ["PyQt5>=5.15"],
    },
    entry_points={
        "console_scripts": [
            "file-encryptor=encryptor.cli.app:main",
            "file-encryptor-gui=encryptor.gui.main_window:run_gui [gui]",
        ],
    },
)