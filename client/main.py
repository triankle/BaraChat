"""Main entry point for the client application."""

import sys
from pathlib import Path

# Add project root to path so imports work
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from client.gui.app_window import AppWindow



def main():
    """Run the BaraChat client application."""
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = AppWindow()
    window.show()
    
    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

