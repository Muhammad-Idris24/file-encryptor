from .cli.app import main as cli_main
from .gui.main_window import run_gui as gui_main

__version__ = "1.0.0"
__all__ = ['cli_main', 'gui_main']