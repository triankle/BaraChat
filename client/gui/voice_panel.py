"""Voice chat panel (stub for future implementation)."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class VoicePanel(QWidget):
    """Voice chat panel - stub implementation."""
    
    def __init__(self):
        """Initialize voice panel."""
        super().__init__()
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI layout."""
        layout = QVBoxLayout(self)
        
        info_label = QLabel("Voice chat functionality coming soon...")
        info_label.setAlignment(4)  # Qt::AlignmentFlag.AlignCenter
        info_label.setStyleSheet("color: #888; font-size: 14px;")
        layout.addWidget(info_label)
        
        # Placeholder button
        mute_button = QPushButton("Mute (Coming Soon)")
        mute_button.setEnabled(False)
        layout.addWidget(mute_button)
        
        layout.addStretch()

