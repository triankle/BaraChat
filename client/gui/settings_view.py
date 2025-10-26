"""Settings view for user configuration."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox
from PySide6.QtCore import Signal


class SettingsView(QWidget):
    """Settings and login view."""
    
    # Signal emitted when user logs in
    on_login = Signal(str, str)  # username, server_url
    
    def __init__(self):
        """Initialize settings view."""
        super().__init__()
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI layout."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Connection settings group
        connection_group = QGroupBox("Server Connection")
        connection_layout = QVBoxLayout()
        
        server_layout = QHBoxLayout()
        server_layout.addWidget(QLabel("Server URL:"))
        self.server_url_input = QLineEdit("http://127.0.0.1:8765")
        server_layout.addWidget(self.server_url_input)
        connection_layout.addLayout(server_layout)
        
        connection_group.setLayout(connection_layout)
        layout.addWidget(connection_group)
        
        # User settings group
        user_group = QGroupBox("User Settings")
        user_layout = QVBoxLayout()
        
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit("User123")
        username_layout.addWidget(self.username_input)
        user_layout.addLayout(username_layout)
        
        user_group.setLayout(user_layout)
        layout.addWidget(user_group)
        
        # Connect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004578;
            }
        """)
        self.connect_button.clicked.connect(self._on_connect_clicked)
        layout.addWidget(self.connect_button)
        
        # Add stretch to push everything up
        layout.addStretch()
    
    def _on_connect_clicked(self):
        """Handle connect button click."""
        username = self.username_input.text().strip()
        server_url = self.server_url_input.text().strip()
        
        if username and server_url:
            # Emit signal to trigger login
            self.on_login.emit(username, server_url)
        else:
            print("Please enter username and server URL")

