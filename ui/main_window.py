"""
Main application window
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, 
    QFrame, QStackedWidget, QLabel, QStatusBar, QPushButton
)
from PySide6.QtCore import Qt
from config.constants import APP_NAME, APP_VERSION, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, STATUS_CONNECTED
from ui.sidebar import Sidebar
from ui.pages.dashboard_page import DashboardPage
from ui.pages.databases import DatabasesPage
from ui.pages.backups_page import BackupsPage
from ui.pages.users_page import UsersPage
from ui.pages.settings_page import SettingsPage
from resources.styles.dark_theme import MODERN_GRAY_THEME


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.resize(1320, 840)
        
        self.setStyleSheet(MODERN_GRAY_THEME)
        self._init_ui()
        
    def _init_ui(self):
        """Initialize user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self.switch_page)
        main_layout.addWidget(self.sidebar)
        
        # Content area
        content_container = QWidget()
        content_container.setObjectName("contentArea")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Top bar
        top_bar = self._create_top_bar()
        content_layout.addWidget(top_bar)
        
        # Stacked widget for pages
        self.stack = QStackedWidget()
        self.stack.addWidget(DashboardPage())
        self.stack.addWidget(DatabasesPage())
        self.stack.addWidget(BackupsPage())
        self.stack.addWidget(UsersPage())
        self.stack.addWidget(SettingsPage())
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.stack)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setObjectName("mainScrollArea")
        content_layout.addWidget(scroll)
        
        main_layout.addWidget(content_container, 1)
        
        # Remove status bar
        self.setStatusBar(None)
    
    def _create_top_bar(self):
        """Create top bar with breadcrumbs"""
        top_bar = QFrame()
        top_bar.setObjectName("topBar")
        top_bar.setFixedHeight(64)
        
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(32, 0, 32, 0)
        
        self.breadcrumb = QLabel("Home / Dashboard")
        self.breadcrumb.setObjectName("breadcrumb")
        layout.addWidget(self.breadcrumb)
        
        layout.addStretch()
        
        return top_bar
    
    def switch_page(self, index: int, page_name: str):
        """Switch to selected page"""
        self.stack.setCurrentIndex(index)
        self.breadcrumb.setText(f"Home / {page_name}")