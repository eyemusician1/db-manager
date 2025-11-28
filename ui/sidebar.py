"""
Enhanced Sidebar with collapse/expand functionality - FIXED
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QButtonGroup
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QIcon, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer


class NavButton(QPushButton):
    """Custom navigation button with icon and text"""
    
    def __init__(self, text: str, icon_svg: str, parent=None):
        super().__init__(text, parent)
        self.icon_svg = icon_svg
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(48)


class Sidebar(QWidget):
    """Enhanced sidebar with collapse/expand animation"""
    
    page_changed = Signal(int, str)
    
    # SVG Icons - Outlined style for collapsed state
    ICONS = {
        "dashboard": "▦",
        "database": "◎",
        "backup": "⊞",
        "users": "⚈",
        "settings": "⚙"
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.is_collapsed = False
        self.expanded_width = 280
        self.collapsed_width = 80
        self.setFixedWidth(self.expanded_width)
        self._init_ui()
        self._setup_animation()
    
    def _init_ui(self):
        """Initialize sidebar UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header with toggle button
        header = self._create_header()
        layout.addWidget(header)
        
        layout.addSpacing(24)
        
        # Navigation buttons
        nav_container = QWidget()
        self.nav_layout = QVBoxLayout(nav_container)
        self.nav_layout.setContentsMargins(16, 0, 16, 0)
        self.nav_layout.setSpacing(8)
        
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        
        nav_items = [
            ("Dashboard", "dashboard", 0),
            ("Databases", "database", 1),
            ("Backups", "backup", 2),
            ("Users", "users", 3),
            ("Settings", "settings", 4)
        ]
        
        self.nav_buttons = []
        for text, icon_key, index in nav_items:
            btn = self._create_nav_button(text, self.ICONS[icon_key], index)
            self.nav_layout.addWidget(btn)
            self.button_group.addButton(btn, index)
            self.nav_buttons.append(btn)
        
        self.button_group.button(0).setChecked(True)
        
        layout.addWidget(nav_container)
        layout.addStretch()
        
        # Footer
        self.footer = self._create_footer()
        layout.addWidget(self.footer)
    
    def _create_header(self):
        """Create sidebar header with toggle button"""
        header = QFrame()
        header.setObjectName("sidebarHeader")
        header.setFixedHeight(80)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)
        
        # Title container
        self.title_container = QWidget()
        title_layout = QVBoxLayout(self.title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(2)
        title_layout.setAlignment(Qt.AlignCenter)
        
        self.title = QLabel("BackMeUp")
        self.title.setObjectName("appTitle")
        
        self.subtitle = QLabel("Database Management")
        self.subtitle.setStyleSheet("""
            color: #b8a5d8;
            font-size: 12px;
            font-weight: 500;
        """)
        
        title_layout.addWidget(self.title)
        title_layout.addWidget(self.subtitle)
        
        header_layout.addWidget(self.title_container)
        header_layout.addStretch()
        
        # Toggle button
        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.setObjectName("toggleButton")
        self.toggle_btn.setFixedSize(40, 40)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        
        header_layout.addWidget(self.toggle_btn)
        
        return header
    
    def _create_nav_button(self, text: str, icon_svg: str, index: int):
        """Create navigation button"""
        btn = QPushButton(f"{icon_svg}  {text}")
        btn.setObjectName("navButton")
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(48)
        btn.setProperty("fullText", f"{icon_svg}  {text}")
        btn.setProperty("iconText", icon_svg)  # Changed from "icon" to "iconText" to avoid confusion
        btn.clicked.connect(lambda: self.page_changed.emit(index, text))
        
        return btn
    
    def _create_footer(self):
        """Create sidebar footer"""
        footer = QFrame()
        footer.setObjectName("sidebarFooter")
        
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(24, 16, 24, 24)
        
        
        self.info_label = QLabel("Developed by Sire")
        self.info_label.setStyleSheet("""
            color: #b8a5d8;
            font-size: 11px;
            line-height: 1.6;
        """)
        self.info_label.setAlignment(Qt.AlignCenter)
        
        footer_layout.addSpacing(16)
        footer_layout.addWidget(self.info_label)
        
        return footer
    
    def _setup_animation(self):
        """Setup width animation"""
        self.animation = QPropertyAnimation(self, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        
        self.min_animation = QPropertyAnimation(self, b"minimumWidth")
        self.min_animation.setDuration(300)
        self.min_animation.setEasingCurve(QEasingCurve.InOutCubic)
    
    def toggle_sidebar(self):
        """Toggle sidebar collapse/expand"""
        if self.is_collapsed:
            self.expand_sidebar()
        else:
            self.collapse_sidebar()
    
    def collapse_sidebar(self):
        """Collapse sidebar"""
        self.is_collapsed = True
        
        # Animate width
        self.animation.setStartValue(self.expanded_width)
        self.animation.setEndValue(self.collapsed_width)
        self.animation.start()
        
        self.min_animation.setStartValue(self.expanded_width)
        self.min_animation.setEndValue(self.collapsed_width)
        self.min_animation.start()
        
        # Hide text elements
        self.title.hide()
        self.subtitle.hide()
        self.title_container.hide()
        self.info_label.hide()
        
        # Change button text to show only icons
        for btn in self.nav_buttons:
            icon_text = btn.property("iconText")  # Changed from "icon"
            btn.setText(icon_text)
            # Set property to trigger collapsed state in stylesheet
            btn.setProperty("collapsed", True)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        
        # Change toggle button - center it
        self.toggle_btn.setText("☰")
        
        # Adjust layout margins for centered icons
        self.nav_layout.setContentsMargins(8, 0, 8, 0)
    
    def expand_sidebar(self):
        """Expand sidebar"""
        self.is_collapsed = False
        
        # Animate width
        self.animation.setStartValue(self.collapsed_width)
        self.animation.setEndValue(self.expanded_width)
        self.animation.start()
        
        self.min_animation.setStartValue(self.collapsed_width)
        self.min_animation.setEndValue(self.expanded_width)
        self.min_animation.start()
        
        # Show text elements
        self.title.show()
        self.subtitle.show()
        self.title_container.show()
        self.info_label.show()
        
        # Restore button text with icons
        for btn in self.nav_buttons:
            full_text = btn.property("fullText")
            btn.setText(full_text)
            # Remove collapsed property
            btn.setProperty("collapsed", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        
        # Change toggle button
        self.toggle_btn.setText("☰")
        
        # Restore layout margins
        self.nav_layout.setContentsMargins(16, 0, 16, 0)