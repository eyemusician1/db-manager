"""
Clean statistic card with pastel dark theme
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class StatCard(QFrame):
    """Modern stat card with pastel accents"""
    
    ICON_MAP = {
        "database": "▣",
        "backup": "⧉",
        "storage": "▦",
        "time": "◷"
    }
    
    PASTEL_COLORS = {
        "database": "#8b7ab8",  # Pastel purple
        "backup": "#7ea8c7",    # Deeper blue
        "storage": "#c9a86a",   # Muted gold
        "time": "#b88ba8"       # Dusty rose
    }
    
    def __init__(self, title: str, value: str, icon_type: str, parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.icon_type = icon_type
        self.color = self.PASTEL_COLORS.get(icon_type, "#8b7ab8")
        self._init_ui(title, value, icon_type)
        self._add_shadow()
        self._apply_default_style()
    
    def _init_ui(self, title: str, value: str, icon_type: str):
        """Initialize stat card UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)
        
        # Icon with pastel background
        self.icon_container = QFrame()
        self.icon_container.setObjectName("iconContainer")
        self.icon_container.setFixedSize(56, 56)
        
        icon_layout = QVBoxLayout(self.icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignCenter)
        
        self.icon_label = QLabel(self.ICON_MAP.get(icon_type, "◆"))
        icon_layout.addWidget(self.icon_label)
        
        # Value label
        self.value_label = QLabel(value)
        self.value_label.setObjectName("cardValue")
        
        # Title label
        self.title_label = QLabel(title)
        self.title_label.setObjectName("cardTitle")
        
        layout.addWidget(self.icon_container, 0, Qt.AlignLeft)
        layout.addWidget(self.value_label)
        layout.addWidget(self.title_label)
        layout.addStretch()
    
    def _apply_default_style(self):
        """Apply default non-hover styles"""
        # Card background - using a semi-transparent style
        self.setStyleSheet(f"""
            #statCard {{
                background-color: #252238;
                border: 1px solid #3a3550;
                border-radius: 16px;
            }}
        """)
        
        # Icon container
        self.icon_container.setStyleSheet(f"""
            #iconContainer {{
                background-color: {self.color}33;
                border-radius: 14px;
                border: 1px solid {self.color}55;
            }}
        """)
        
        # Icon label
        self.icon_label.setStyleSheet(f"""
            font-size: 28px;
            color: {self.color};
            font-weight: 600;
            background: transparent;
            border: none;
        """)
        
        # Value label
        self.value_label.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: -0.5px;
        """)
        
        # Title label
        self.title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #b8a5d8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        """)
    
    def _add_shadow(self):
        """Add subtle shadow effect"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)
    
    def enterEvent(self, event):
        """Animate on mouse enter"""
        # Update card background with border
        self.setStyleSheet(f"""
            #statCard {{
                background-color: #2d2a3e;
                border: 2px solid {self.color};
                border-radius: 16px;
            }}
        """)
        
        # Enhance shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(32)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(shadow)
        
        # Brighten icon background
        self.icon_container.setStyleSheet(f"""
            #iconContainer {{
                background-color: {self.color};
                border-radius: 14px;
                border: 1px solid {self.color};
            }}
        """)
        
        # Update icon color to dark for contrast
        self.icon_label.setStyleSheet("""
            font-size: 28px;
            color: #1a1625;
            font-weight: 700;
            background: transparent;
            border: none;
        """)
        
        # Update value color to accent
        self.value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 700;
            color: {self.color};
            letter-spacing: -0.5px;
        """)
        
        # Title stays the same
        self.title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #b8a5d8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        """)
        
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Animate on mouse leave"""
        # Reset to default styles
        self._apply_default_style()
        
        # Reset shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)
        
        super().leaveEvent(event)
