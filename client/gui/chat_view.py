"""Chat view widget for displaying and sending messages."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt
from datetime import datetime
from client.utils.logger import get_logger


logger = get_logger(__name__)


class ChatView(QWidget):
    """Widget for displaying and sending chat messages."""
    
    def __init__(self):
        """Initialize chat view."""
        super().__init__()
        
        self.username = ""
        self.messages = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Message display area
        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)
        self.message_display.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.message_display)
        
        # Input area
        input_layout = QHBoxLayout()
        
        # Username label
        self.username_label = QLabel("You: ")
        self.username_label.setStyleSheet("color: #888; font-weight: bold;")
        input_layout.addWidget(self.username_label)
        
        # Message input
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.returnPressed.connect(self._on_send_clicked)
        self.message_input.setStyleSheet("""
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
        """)
        input_layout.addWidget(self.message_input)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self._on_send_clicked)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004578;
            }
        """)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
    
    def set_username(self, username: str):
        """Set the current username."""
        self.username = username
        self.username_label.setText(f"{username}: ")
        logger.info(f"Username set: {username}")
    
    def add_message(self, user: str, text: str, timestamp: float = 0):
        """
        Add a message to the display.
        
        Args:
            user: Username
            text: Message text
            timestamp: Message timestamp
        """
        # Format timestamp
        if timestamp > 0:
            dt = datetime.fromtimestamp(timestamp)
            time_str = dt.strftime("%H:%M:%S")
        else:
            time_str = datetime.now().strftime("%H:%M:%S")
        
        # Determine color based on user
        color = "#4ec9b0" if user == self.username else "#9cdcfe"
        
        # Format message
        message_html = f"""
        <div style="margin: 5px 0;">
            <span style="color: {color}; font-weight: bold;">{user}</span>
            <span style="color: #888; font-size: 10px;"> ({time_str})</span>
            <br>
            <span style="color: #ffffff;">{self._escape_html(text)}</span>
        </div>
        """
        
        # Add to display
        self.message_display.append(message_html)
        
        # Store in messages list
        self.messages.append({
            'user': user,
            'text': text,
            'timestamp': timestamp
        })
        
        # Auto-scroll to bottom
        scrollbar = self.message_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#x27;"))
    
    def _on_send_clicked(self):
        """Handle send button click or Enter key."""
        text = self.message_input.text().strip()
        
        if text:
            # Get parent window and send message
            window = self.window()
            if hasattr(window, 'send_message'):
                window.send_message(text)
            
            self.message_input.clear()
            logger.info(f"Sent: {text}")
    
    def clear(self):
        """Clear all messages (for room switching)."""
        self.message_display.clear()
        self.messages.clear()
        logger.info("Chat view cleared")

