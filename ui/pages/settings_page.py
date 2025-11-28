"""
Application settings page with modern card-based design
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QLineEdit, QPushButton, QCheckBox, QComboBox, 
    QGridLayout, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor


class SettingsPage(QWidget):
    """Settings page with modern design"""
    
    # Signals for actions
    test_connection_requested = Signal(dict)
    save_settings_requested = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize settings page UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(40)
        
        # Page header
        header_frame = self._create_page_header()
        layout.addWidget(header_frame)
        
        # Connection settings
        conn_frame = self._create_connection_settings()
        layout.addWidget(conn_frame)
        
        # Backup settings
        backup_frame = self._create_backup_settings()
        layout.addWidget(backup_frame)
        
        # Theme settings
        theme_frame = self._create_theme_settings()
        layout.addWidget(theme_frame)
        
        # Save button
        btn_save = QPushButton("↓ Save All Settings")
        btn_save.setObjectName("primaryButton")
        btn_save.setMinimumHeight(50)
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.clicked.connect(self._handle_save_settings)
        layout.addWidget(btn_save)
        
        layout.addStretch()
    
    def _create_page_header(self):
        """Create clean page header matching other pages"""
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)
        
        title = QLabel("Settings")
        title.setStyleSheet("""
            font-size: 36px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: -1.2px;
        """)
        
        subtitle = QLabel("Configure application preferences and database connections")
        subtitle.setStyleSheet("""
            color: #b8a5d8;
            font-size: 16px;
            font-weight: 500;
        """)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        return header_frame
    
    def _create_connection_settings(self):
        """Create connection settings section"""
        conn_frame = QFrame()
        conn_frame.setObjectName("contentCard")
        conn_layout = QVBoxLayout(conn_frame)
        conn_layout.setContentsMargins(32, 28, 32, 28)
        conn_layout.setSpacing(24)
        
        # Section title
        conn_title = QLabel("CONNECTION SETTINGS")
        conn_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: 0.5px;
        """)
        conn_layout.addWidget(conn_title)
        
        # Form layout
        form_layout = QGridLayout()
        form_layout.setSpacing(16)
        form_layout.setColumnStretch(1, 1)
        
        # Labels styling
        label_style = """
            font-size: 14px;
            font-weight: 600;
            color: #b8a5d8;
        """
        
        # Input styling
        input_style = """
            QLineEdit {
                background-color: #2A2F4A;
                border: 1px solid #3A4560;
                border-radius: 8px;
                padding: 0 16px;
                color: #E0E7FF;
                font-size: 14px;
                min-height: 44px;
            }
            QLineEdit:focus {
                border: 1px solid #0EA5E9;
                background-color: #323852;
            }
            QLineEdit::placeholder {
                color: #7C8BA8;
            }
        """
        
        # Host
        host_label = QLabel("Host:")
        host_label.setStyleSheet(label_style)
        form_layout.addWidget(host_label, 0, 0, Qt.AlignRight | Qt.AlignTop)
        
        self.host_input = QLineEdit("localhost")
        self.host_input.setStyleSheet(input_style)
        self.host_input.setPlaceholderText("Enter database host")
        form_layout.addWidget(self.host_input, 0, 1)
        
        # Port
        port_label = QLabel("Port:")
        port_label.setStyleSheet(label_style)
        form_layout.addWidget(port_label, 1, 0, Qt.AlignRight | Qt.AlignTop)
        
        self.port_input = QLineEdit("3306")
        self.port_input.setStyleSheet(input_style)
        self.port_input.setPlaceholderText("MySQL default: 3306")
        form_layout.addWidget(self.port_input, 1, 1)
        
        # Username
        user_label = QLabel("Username:")
        user_label.setStyleSheet(label_style)
        form_layout.addWidget(user_label, 2, 0, Qt.AlignRight | Qt.AlignTop)
        
        self.user_input = QLineEdit("root")
        self.user_input.setStyleSheet(input_style)
        self.user_input.setPlaceholderText("Database username")
        form_layout.addWidget(self.user_input, 2, 1)
        
        # Password
        pass_label = QLabel("Password:")
        pass_label.setStyleSheet(label_style)
        form_layout.addWidget(pass_label, 3, 0, Qt.AlignRight | Qt.AlignTop)
        
        password_layout = QHBoxLayout()
        password_layout.setSpacing(8)
        
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setStyleSheet(input_style)
        self.pass_input.setPlaceholderText("Database password")
        
        self.toggle_password_btn = QPushButton("◉")
        self.toggle_password_btn.setFixedSize(44, 44)
        self.toggle_password_btn.setToolTip("Show/Hide Password")
        self.toggle_password_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_password_btn.clicked.connect(self._toggle_password_visibility)
        self.toggle_password_btn.setStyleSheet("""
            QPushButton {
                background-color: #4A5578;
                border: 1px solid #5A6588;
                border-radius: 8px;
                color: #E0E7FF;
                font-size: 16px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #0EA5E9;
                border-color: #0EA5E9;
            }
        """)
        
        password_layout.addWidget(self.pass_input)
        password_layout.addWidget(self.toggle_password_btn)
        
        form_layout.addLayout(password_layout, 3, 1)
        
        conn_layout.addLayout(form_layout)
        
        # Test connection button
        btn_test_conn = QPushButton("⚡ Test Connection")
        btn_test_conn.setObjectName("secondaryButton")
        btn_test_conn.setMinimumHeight(44)
        btn_test_conn.setCursor(Qt.PointingHandCursor)
        btn_test_conn.clicked.connect(self._handle_test_connection)
        conn_layout.addWidget(btn_test_conn)
        
        return conn_frame
    
    def _create_backup_settings(self):
        """Create backup settings section"""
        backup_frame = QFrame()
        backup_frame.setObjectName("contentCard")
        backup_layout = QVBoxLayout(backup_frame)
        backup_layout.setContentsMargins(32, 28, 32, 28)
        backup_layout.setSpacing(24)
        
        # Section title
        backup_title = QLabel("BACKUP SETTINGS")
        backup_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: 0.5px;
        """)
        backup_layout.addWidget(backup_title)
        
        # Form layout
        backup_form = QGridLayout()
        backup_form.setSpacing(16)
        backup_form.setColumnStretch(1, 1)
        
        label_style = """
            font-size: 14px;
            font-weight: 600;
            color: #b8a5d8;
        """
        
        # Default location
        location_label = QLabel("Default Location:")
        location_label.setStyleSheet(label_style)
        backup_form.addWidget(location_label, 0, 0, Qt.AlignRight | Qt.AlignTop)
        
        location_layout = QHBoxLayout()
        location_layout.setSpacing(8)
        
        self.location_input = QLineEdit("/backups")
        self.location_input.setStyleSheet("""
            QLineEdit {
                background-color: #2A2F4A;
                border: 1px solid #3A4560;
                border-radius: 8px;
                padding: 0 16px;
                color: #E0E7FF;
                font-size: 14px;
                min-height: 44px;
            }
            QLineEdit:focus {
                border: 1px solid #0EA5E9;
                background-color: #323852;
            }
        """)
        
        btn_browse = QPushButton("◰ Browse")
        btn_browse.setObjectName("secondaryButton")
        btn_browse.setMinimumHeight(44)
        btn_browse.setMinimumWidth(120)
        btn_browse.setCursor(Qt.PointingHandCursor)
        btn_browse.clicked.connect(self._handle_browse_location)
        
        location_layout.addWidget(self.location_input)
        location_layout.addWidget(btn_browse)
        
        backup_form.addLayout(location_layout, 0, 1)
        
        # Auto-backup
        auto_label = QLabel("Auto-backup:")
        auto_label.setStyleSheet(label_style)
        backup_form.addWidget(auto_label, 1, 0, Qt.AlignRight | Qt.AlignTop)
        
        self.auto_checkbox = QCheckBox("Enable automatic backups daily")
        self.auto_checkbox.setStyleSheet("""
            QCheckBox {
                color: #E0E7FF;
                font-size: 14px;
                font-weight: 500;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #5A6588;
                border-radius: 4px;
                background-color: #2A2F4A;
            }
            QCheckBox::indicator:hover {
                border-color: #0EA5E9;
                background-color: #323852;
            }
            QCheckBox::indicator:checked {
                background-color: #0EA5E9;
                border-color: #0EA5E9;
            }
        """)
        backup_form.addWidget(self.auto_checkbox, 1, 1)
        
        # Compression
        compression_label = QLabel("Compression:")
        compression_label.setStyleSheet(label_style)
        backup_form.addWidget(compression_label, 2, 0, Qt.AlignRight | Qt.AlignTop)
        
        self.compression_combo = QComboBox()
        self.compression_combo.addItems(["gzip", "zip", "None"])
        self.compression_combo.setCursor(Qt.PointingHandCursor)
        self.compression_combo.setStyleSheet("""
            QComboBox {
                background-color: #2A2F4A;
                border: 1px solid #3A4560;
                border-radius: 8px;
                padding: 0 16px;
                color: #E0E7FF;
                font-size: 14px;
                font-weight: 500;
                min-height: 44px;
            }
            QComboBox:hover {
                border: 1px solid #0EA5E9;
                background-color: #323852;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #2A2F4A;
                border: 1px solid #3A4560;
                selection-background-color: #0EA5E9;
                selection-color: #FFFFFF;
                color: #E0E7FF;
                padding: 4px;
            }
        """)
        backup_form.addWidget(self.compression_combo, 2, 1)
        
        backup_layout.addLayout(backup_form)
        
        return backup_frame
    
    def _create_theme_settings(self):
        """Create theme settings section"""
        theme_frame = QFrame()
        theme_frame.setObjectName("contentCard")
        theme_layout = QVBoxLayout(theme_frame)
        theme_layout.setContentsMargins(32, 28, 32, 28)
        theme_layout.setSpacing(24)
        
        # Section title
        theme_title = QLabel("APPEARANCE")
        theme_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: 0.5px;
        """)
        theme_layout.addWidget(theme_title)
        
        # Dark mode toggle
        self.theme_toggle = QCheckBox("◐ Dark Mode (Currently Enabled)")
        self.theme_toggle.setChecked(True)
        self.theme_toggle.setStyleSheet("""
            QCheckBox {
                color: #E0E7FF;
                font-size: 15px;
                font-weight: 500;
                spacing: 12px;
                padding: 8px 0;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
                border: 2px solid #5A6588;
                border-radius: 6px;
                background-color: #2A2F4A;
            }
            QCheckBox::indicator:hover {
                border-color: #0EA5E9;
                background-color: #323852;
            }
            QCheckBox::indicator:checked {
                background-color: #0EA5E9;
                border-color: #0EA5E9;
            }
        """)
        theme_layout.addWidget(self.theme_toggle)
        
        # Theme description
        theme_desc = QLabel("Switch between light and dark color schemes")
        theme_desc.setStyleSheet("""
            color: #7C8BA8;
            font-size: 13px;
            padding-left: 36px;
        """)
        theme_layout.addWidget(theme_desc)
        
        return theme_frame
    
    # Event Handlers
    
    def _toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.pass_input.echoMode() == QLineEdit.Password:
            self.pass_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_btn.setText("●")
        else:
            self.pass_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_btn.setText("◉")
    
    def _handle_test_connection(self):
        """Handle test connection button click"""
        from core.database import DatabaseManager
        
        # Get connection details from inputs
        connection_data = {
            "host": self.host_input.text(),
            "port": int(self.port_input.text()),
            "username": self.user_input.text(),
            "password": self.pass_input.text()
        }
        
        # Test connection
        db_manager = DatabaseManager(
            host=connection_data["host"],
            port=connection_data["port"],
            user=connection_data["username"],
            password=connection_data["password"]
        )
        
        success, message = db_manager.test_connection()
        
        if success:
            QMessageBox.information(
                self,
                "✓ Connection Successful",
                f"Successfully connected to MySQL server!\n\n{message}"
            )
        else:
            QMessageBox.critical(
                self,
                "✗ Connection Failed",
                f"Failed to connect to MySQL server.\n\n{message}\n\nPlease check:\n"
                "- MySQL is running in XAMPP\n"
                "- Host and port are correct\n"
                "- Username and password are correct"
            )

    
    def _handle_browse_location(self):
        """Handle browse button click"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Backup Directory",
            self.location_input.text()
        )
        
        if directory:
            self.location_input.setText(directory)
    
    def _handle_save_settings(self):
        """Handle save settings button click"""
        settings_data = {
            "connection": {
                "host": self.host_input.text(),
                "port": self.port_input.text(),
                "username": self.user_input.text(),
                "password": self.pass_input.text()
            },
            "backup": {
                "location": self.location_input.text(),
                "auto_backup": self.auto_checkbox.isChecked(),
                "compression": self.compression_combo.currentText()
            },
            "appearance": {
                "dark_mode": self.theme_toggle.isChecked()
            }
        }
        
        self.save_settings_requested.emit(settings_data)
        
        QMessageBox.information(
            self,
            "Settings Saved",
            "All settings have been successfully saved!\n\n"
            "The changes will take effect immediately."
        )
