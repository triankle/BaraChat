"""Chat view widget for displaying and sending messages."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QFileDialog
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QTextCharFormat, QTextCursor, QDesktopServices
from datetime import datetime
from pathlib import Path
from client.utils.logger import get_logger
import base64
import webbrowser


logger = get_logger(__name__)


class ChatView(QWidget):
    """Widget for displaying and sending chat messages."""
    
    def __init__(self):
        """Initialize chat view."""
        super().__init__()
        
        self.username = ""
        self.messages = []
        self.download_button = None
        self.current_file_url = None
        
        self._setup_ui()
        
        # Create download button (always visible at bottom)
        self._create_download_button()
    
    def _setup_ui(self):
        """Set up the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Message display area
        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)
        # Note: QTextEdit doesn't have setOpenExternalLinks, links will be clickable in HTML
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
        
        # Attach file button
        self.attach_button = QPushButton("📎")
        self.attach_button.clicked.connect(self._on_attach_clicked)
        self.attach_button.setToolTip("Attach file")
        self.attach_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
            }
        """)
        input_layout.addWidget(self.attach_button)
        
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
    
    def _create_download_button(self):
        """Create download button that shows last file URL."""
        # Get main layout
        layout = self.layout()
        
        # Create download area
        download_widget = QWidget()
        download_widget.setStyleSheet("background-color: #1e1e1e; padding: 5px;")
        download_layout = QVBoxLayout(download_widget)
        download_layout.setContentsMargins(10, 5, 10, 5)
        
        # Label
        label = QLabel("📥 Download Last File")
        label.setStyleSheet("color: #888; font-size: 11px; font-weight: bold;")
        download_layout.addWidget(label)
        
        # URL display and button row
        button_row = QHBoxLayout()
        
        self.download_url_label = QLabel("No file available")
        self.download_url_label.setStyleSheet("color: #888; font-size: 10px;")
        self.download_url_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        self.download_button = QPushButton("📥 Download")
        self.download_button.clicked.connect(self._download_file)
        self.download_button.setEnabled(False)
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #bbb;
            }
        """)
        
        button_row.addWidget(self.download_url_label, 3)
        button_row.addWidget(self.download_button, 1)
        
        download_layout.addLayout(button_row)
        
        # Add to main layout
        layout.addWidget(download_widget)
    
    def _download_file(self):
        """Download the current file."""
        if self.current_file_url:
            logger.info(f"Downloading file from: {self.current_file_url}")
            # Import and trigger download
            window = self.window()
            if hasattr(window, 'download_file'):
                window.download_file(self.current_file_url)
    
    def update_download_button(self, file_url: str):
        """Update download button with new file URL."""
        self.current_file_url = file_url
        display_url = file_url.split('/')[-1]  # Show just the filename
        self.download_url_label.setText(display_url)
        self.download_url_label.setStyleSheet("color: #28a745; font-size: 10px; font-weight: bold;")
        self.download_button.setEnabled(True)
    
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
    
    def _on_attach_clicked(self):
        """Handle attach file button click."""
        try:
            # Use native=False to avoid Windows dialog issues
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select a file to send",
                "",
                "All Files (*.*);;Images (*.png *.jpg *.jpeg *.gif *.bmp);;Documents (*.pdf *.doc *.docx *.txt)",
                options=QFileDialog.Option.DontUseNativeDialog
            )
            
            if file_path and file_path.strip():
                self._send_file(file_path)
        except Exception as e:
            logger.error(f"File dialog error: {e}")
            self.add_message("System", f"Error opening file dialog: {e}", 0)
    
    def _send_file(self, file_path: str):
        """Send a file."""
        file_path_obj = Path(file_path)
        filename = file_path_obj.name
        
        # Read file
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Check if it's an image
            is_image = file_path_obj.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
            
            # Show file in chat immediately
            self.add_message(self.username, f"[FILE] {filename}", 0)
            
            # Get parent window to send message
            window = self.window()
            if hasattr(window, 'send_file'):
                window.send_file(filename, file_data, is_image)
            
            logger.info(f"Attached file: {filename}")
        
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            self.add_message("System", f"Error: Could not read file - {e}", 0)
    
    def add_file_message(self, user: str, filename: str, file_url: str, is_image: bool, timestamp: float = 0):
        """Add a file message to the display."""
        if timestamp > 0:
            dt = datetime.fromtimestamp(timestamp)
            time_str = dt.strftime("%H:%M:%S")
        else:
            time_str = datetime.now().strftime("%H:%M:%S")
        
        color = "#4ec9b0" if user == self.username else "#9cdcfe"
        
        # Create a clickable download link
        download_link = f"file://download/{filename}"
        
        if is_image:
            # For images, show filename with download link
            message_html = f"""
            <div style="margin: 5px 0;">
                <span style="color: {color}; font-weight: bold;">{user}</span>
                <span style="color: #888; font-size: 10px;"> ({time_str})</span>
                <br>
                <span style="color: #888;">📷 {self._escape_html(filename)}</span>
                <br>
                <a href="{download_link}" style="color: #28a745; text-decoration: underline; cursor: pointer;">📥 Download</a>
            </div>
            """
        else:
            # For other files
            message_html = f"""
            <div style="margin: 5px 0;">
                <span style="color: {color}; font-weight: bold;">{user}</span>
                <span style="color: #888; font-size: 10px;"> ({time_str})</span>
                <br>
                <span style="color: #888;">📎 {self._escape_html(filename)}</span>
                <br>
                <a href="{download_link}" style="color: #28a745; text-decoration: underline; cursor: pointer;">📥 Download</a>
            </div>
            """
        
        # Add to display
        self.message_display.append(message_html)
        
        # Update last download button
        if self.download_button:
            self.update_download_button(file_url)
        
        # Store in messages list with file data for download
        self.messages.append({
            'user': user,
            'type': 'file',
            'filename': filename,
            'file_url': file_url,
            'is_image': is_image,
            'timestamp': timestamp
        })
        
        # Auto-scroll
        scrollbar = self.message_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear(self):
        """Clear all messages (for room switching)."""
        self.message_display.clear()
        self.messages.clear()
        logger.info("Chat view cleared")

