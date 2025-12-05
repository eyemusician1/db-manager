"""

Main login and registration dialog - Separate Heights for Login & Register

"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QWidget, QStackedWidget,
    QMessageBox, QCheckBox, QScrollArea
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont
from core.database import DatabaseManager
from datetime import datetime


class LoginDialog(QDialog):
    """Main login and registration dialog with independent heights"""

    # Signal emitted when authentication is successful
    authenticated = Signal(dict)

    # Define separate heights for login and register modes
    LOGIN_HEIGHT = 540      # Adjust this for login form height
    REGISTER_HEIGHT = 780   # Adjust this for register form height
    DIALOG_WIDTH = 480      # Fixed width for both

    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("BackMeUp - Login")
        self.setModal(True)

        # Start with login size
        self.setFixedSize(self.DIALOG_WIDTH, self.LOGIN_HEIGHT)

        self.authenticated_user = None
        self._init_ui()
        self._apply_styles()

    def _create_icon_label(self, icon_text, size=18):
        """Create a monochrome icon label"""
        icon_label = QLabel(icon_text)
        icon_label.setObjectName("iconLabel")
        icon_label.setFixedSize(size, size)
        icon_label.setAlignment(Qt.AlignCenter)
        return icon_label

    def _create_input_with_icon(self, icon_text, line_edit):
        """Create an input field with a monochrome icon"""
        container = QWidget()
        container.setObjectName("inputContainer")

        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)

        # Icon
        icon = self._create_icon_label(icon_text, 18)

        # Configure line edit
        line_edit.setFrame(False)
        line_edit.setObjectName("iconInput")

        layout.addWidget(icon)
        layout.addWidget(line_edit, 1)

        return container

    def _init_ui(self):
        """Initialize the login dialog UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Main container
        container = QFrame()
        container.setObjectName("loginContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(48, 32, 48, 32)
        container_layout.setSpacing(28)

        # Header
        header_widget = self._create_header()
        container_layout.addWidget(header_widget)

        # Stacked widget for login/register forms
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("formsStack")

        # Login form
        self.login_widget = self._create_login_form()
        self.stacked_widget.addWidget(self.login_widget)

        # Register form
        self.register_widget = self._create_register_form()
        self.stacked_widget.addWidget(self.register_widget)

        container_layout.addWidget(self.stacked_widget, 1)

        # Error message label
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        container_layout.addWidget(self.error_label)

        # Switch between login/register
        switch_widget = self._create_switch_widget()
        container_layout.addWidget(switch_widget)

        main_layout.addWidget(container)

    def _create_header(self):
        """Create the header section"""
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        # Title
        title = QLabel("BackMeUp")
        title.setObjectName("dialogTitle")
        title.setAlignment(Qt.AlignCenter)

        # Subtitle
        subtitle = QLabel("Database Management System")
        subtitle.setObjectName("dialogSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        return header

    def _create_login_form(self):
        """Create the login form"""
        form = QWidget()
        form_layout = QVBoxLayout(form)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(18)

        # Username field
        username_label = QLabel("USERNAME")
        username_label.setObjectName("fieldLabel")

        self.login_username_input = QLineEdit()
        self.login_username_input.setPlaceholderText("Enter your username")
        self.login_username_input.returnPressed.connect(self._handle_login)
        username_container = self._create_input_with_icon("○", self.login_username_input)
        username_container.setMinimumHeight(48)

        # Password field
        password_label = QLabel("PASSWORD")
        password_label.setObjectName("fieldLabel")

        self.login_password_input = QLineEdit()
        self.login_password_input.setPlaceholderText("Enter your password")
        self.login_password_input.setEchoMode(QLineEdit.Password)
        self.login_password_input.returnPressed.connect(self._handle_login)
        password_container = self._create_input_with_icon("▪", self.login_password_input)
        password_container.setMinimumHeight(48)

        # Remember me checkbox
        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setObjectName("rememberCheckbox")

        # Add widgets to layout
        form_layout.addWidget(username_label)
        form_layout.addWidget(username_container)
        form_layout.addSpacing(4)
        form_layout.addWidget(password_label)
        form_layout.addWidget(password_container)
        form_layout.addWidget(self.remember_checkbox)
        form_layout.addSpacing(12)

        # Login button
        self.btn_login = QPushButton("Login")
        self.btn_login.setObjectName("primaryButton")
        self.btn_login.setMinimumHeight(48)
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.clicked.connect(self._handle_login)
        self.btn_login.setDefault(True)

        form_layout.addWidget(self.btn_login)
        form_layout.addStretch()

        return form

    def _create_register_form(self):
        """Create the registration form with proper spacing"""
        form = QWidget()
        form_layout = QVBoxLayout(form)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(15)

        # Full name field
        fullname_label = QLabel("FULL NAME")
        fullname_label.setObjectName("fieldLabel")

        self.register_fullname_input = QLineEdit()
        self.register_fullname_input.setPlaceholderText("Enter your full name")
        fullname_container = self._create_input_with_icon("○", self.register_fullname_input)
        fullname_container.setMinimumHeight(48)

        # Username field
        username_label = QLabel("USERNAME")
        username_label.setObjectName("fieldLabel")

        self.register_username_input = QLineEdit()
        self.register_username_input.setPlaceholderText("Choose a username")
        username_container = self._create_input_with_icon("○", self.register_username_input)
        username_container.setMinimumHeight(48)

        # Email field
        email_label = QLabel("EMAIL")
        email_label.setObjectName("fieldLabel")

        self.register_email_input = QLineEdit()
        self.register_email_input.setPlaceholderText("Enter your email")
        email_container = self._create_input_with_icon("@", self.register_email_input)
        email_container.setMinimumHeight(48)

        # Password field
        password_label = QLabel("PASSWORD")
        password_label.setObjectName("fieldLabel")

        self.register_password_input = QLineEdit()
        self.register_password_input.setPlaceholderText("Choose a password")
        self.register_password_input.setEchoMode(QLineEdit.Password)
        password_container = self._create_input_with_icon("▪", self.register_password_input)
        password_container.setMinimumHeight(48)

        # Confirm password field
        confirm_password_label = QLabel("CONFIRM PASSWORD")
        confirm_password_label.setObjectName("fieldLabel")

        self.register_confirm_password_input = QLineEdit()
        self.register_confirm_password_input.setPlaceholderText("Confirm your password")
        self.register_confirm_password_input.setEchoMode(QLineEdit.Password)
        self.register_confirm_password_input.returnPressed.connect(self._handle_register)
        confirm_password_container = self._create_input_with_icon("▪", self.register_confirm_password_input)
        confirm_password_container.setMinimumHeight(48)

        # Add widgets to layout with consistent spacing
        form_layout.addWidget(fullname_label)
        form_layout.addWidget(fullname_container)
        form_layout.addSpacing(2)

        form_layout.addWidget(username_label)
        form_layout.addWidget(username_container)
        form_layout.addSpacing(2)

        form_layout.addWidget(email_label)
        form_layout.addWidget(email_container)
        form_layout.addSpacing(2)

        form_layout.addWidget(password_label)
        form_layout.addWidget(password_container)
        form_layout.addSpacing(2)

        form_layout.addWidget(confirm_password_label)
        form_layout.addWidget(confirm_password_container)
        form_layout.addSpacing(12)

        # Register button
        self.btn_register = QPushButton("Register")
        self.btn_register.setObjectName("primaryButton")
        self.btn_register.setMinimumHeight(48)
        self.btn_register.setCursor(Qt.PointingHandCursor)
        self.btn_register.clicked.connect(self._handle_register)

        form_layout.addWidget(self.btn_register)
        form_layout.addStretch()

        return form

    def _create_switch_widget(self):
        """Create widget to switch between login and register"""
        switch_widget = QWidget()
        switch_layout = QHBoxLayout(switch_widget)
        switch_layout.setContentsMargins(0, 0, 0, 0)
        switch_layout.setSpacing(6)

        self.switch_label = QLabel("Don't have an account?")
        self.switch_label.setObjectName("switchLabel")

        self.switch_button = QPushButton("Register")
        self.switch_button.setObjectName("linkButton")
        self.switch_button.setCursor(Qt.PointingHandCursor)
        self.switch_button.clicked.connect(self._switch_mode)

        switch_layout.addStretch()
        switch_layout.addWidget(self.switch_label)
        switch_layout.addWidget(self.switch_button)
        switch_layout.addStretch()

        return switch_widget

    def _resize_dialog(self, target_height):
        """Smoothly resize the dialog to target height"""
        self.setFixedSize(self.DIALOG_WIDTH, target_height)

    def _switch_mode(self):
        """Switch between login and register modes with dynamic resizing"""
        current_index = self.stacked_widget.currentIndex()

        if current_index == 0:  # Currently on login -> Switch to register
            self.stacked_widget.setCurrentIndex(1)
            self.switch_label.setText("Already have an account?")
            self.switch_button.setText("Login")
            self.setWindowTitle("BackMeUp - Register")
            # Resize to register height
            self._resize_dialog(self.REGISTER_HEIGHT)
        else:  # Currently on register -> Switch to login
            self.stacked_widget.setCurrentIndex(0)
            self.switch_label.setText("Don't have an account?")
            self.switch_button.setText("Register")
            self.setWindowTitle("BackMeUp - Login")
            # Resize to login height
            self._resize_dialog(self.LOGIN_HEIGHT)

        self.error_label.hide()

    def _handle_login(self):
        """Handle login attempt"""
        username = self.login_username_input.text().strip()
        password = self.login_password_input.text()

        # Validate input
        if not username or not password:
            self._show_error("Please enter both username and password")
            return

        # Authenticate
        user_data = self._authenticate(username, password)

        if user_data:
            # Update last login
            self._update_last_login(user_data['id'])
            self.authenticated_user = user_data
            self.authenticated.emit(user_data)
            self.accept()
        else:
            self._show_error("Invalid username or password")
            self.login_password_input.clear()
            self.login_password_input.setFocus()

    def _handle_register(self):
        """Handle registration attempt"""
        full_name = self.register_fullname_input.text().strip()
        username = self.register_username_input.text().strip()
        email = self.register_email_input.text().strip()
        password = self.register_password_input.text()
        confirm_password = self.register_confirm_password_input.text()

        # Validate input
        if not all([full_name, username, email, password, confirm_password]):
            self._show_error("Please fill in all fields")
            return

        if password != confirm_password:
            self._show_error("Passwords do not match")
            self.register_confirm_password_input.clear()
            self.register_confirm_password_input.setFocus()
            return

        if len(password) < 6:
            self._show_error("Password must be at least 6 characters long")
            return

        # Register user
        user_data = self._register_user(full_name, username, email, password)

        if user_data:
            self.authenticated_user = user_data
            self.authenticated.emit(user_data)
            self.accept()
        else:
            self._show_error("Registration failed. Username or email may already exist.")

    def _authenticate(self, username: str, password: str) -> dict:
        """Authenticate user credentials"""
        try:
            if not self.db_manager.connection or not self.db_manager.connection.is_connected():
                self.db_manager.connect()

            if not self.db_manager.connection or not self.db_manager.connection.is_connected():
                return None

            cursor = self.db_manager.connection.cursor(dictionary=True)

            # Query the users table
            query = """
                SELECT id, username, email, password, full_name, role, is_active
                FROM users
                WHERE username = %s AND is_active = 1
            """

            cursor.execute(query, (username,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                # Simple password comparison (in production, use password hashing)
                stored_password = result['password']
                if stored_password == password:
                    return {
                        'id': result['id'],
                        'username': result['username'],
                        'email': result['email'],
                        'full_name': result['full_name'],
                        'role': result['role']
                    }

            return None

        except Exception as e:
            print(f"Authentication error: {e}")
            return None

    def _register_user(self, full_name: str, username: str, email: str, password: str) -> dict:
        """Register a new user"""
        try:
            if not self.db_manager.connection or not self.db_manager.connection.is_connected():
                self.db_manager.connect()

            if not self.db_manager.connection or not self.db_manager.connection.is_connected():
                return None

            cursor = self.db_manager.connection.cursor(dictionary=True)

            # Check if username or email already exists
            check_query = """
                SELECT id FROM users
                WHERE username = %s OR email = %s
            """

            cursor.execute(check_query, (username, email))
            if cursor.fetchone():
                cursor.close()
                return None

            # Insert new user
            insert_query = """
                INSERT INTO users (username, email, password, full_name, role, is_active)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, (username, email, password, full_name, 'user', True))
            self.db_manager.connection.commit()

            # Get the inserted user
            user_id = cursor.lastrowid
            cursor.close()

            return {
                'id': user_id,
                'username': username,
                'email': email,
                'full_name': full_name,
                'role': 'user'
            }

        except Exception as e:
            print(f"Registration error: {e}")
            if self.db_manager.connection:
                self.db_manager.connection.rollback()
            return None

    def _update_last_login(self, user_id: int):
        """Update user's last login timestamp"""
        try:
            if not self.db_manager.connection or not self.db_manager.connection.is_connected():
                return

            cursor = self.db_manager.connection.cursor()
            update_query = "UPDATE users SET last_login = %s WHERE id = %s"
            cursor.execute(update_query, (datetime.now(), user_id))
            self.db_manager.connection.commit()
            cursor.close()

        except Exception as e:
            print(f"Error updating last login: {e}")

    def _show_error(self, message: str):
        """Display error message"""
        self.error_label.setText(message)
        self.error_label.show()

    def _apply_styles(self):
        """Apply modern stylesheet to the dialog"""
        self.setStyleSheet("""
            QDialog {
                background-color: #0F172A;
            }

            #loginContainer {
                background-color: #1E293B;
                border: 1px solid #334155;
                border-radius: 16px;
            }

            #dialogTitle {
                font-size: 32px;
                font-weight: 700;
                color: #F1F5F9;
                letter-spacing: -0.5px;
                margin-bottom: 4px;
            }

            #dialogSubtitle {
                font-size: 13px;
                font-weight: 500;
                color: #94A3B8;
                letter-spacing: 0.2px;
            }

            #fieldLabel {
                font-size: 11px;
                font-weight: 700;
                color: #94A3B8;
                letter-spacing: 0.8px;
                margin-bottom: 6px;
            }

            #inputContainer {
                background-color: #0F172A;
                border: 2px solid #334155;
                border-radius: 8px;
            }

            #inputContainer:focus-within {
                border-color: #3B82F6;
                background-color: #1E293B;
            }

            #iconLabel {
                color: #64748B;
                font-size: 15px;
                font-weight: bold;
            }

            #iconInput {
                background-color: transparent;
                border: none;
                color: #F1F5F9;
                font-size: 14px;
                font-weight: 500;
                padding: 0;
            }

            #iconInput::placeholder {
                color: #475569;
                font-weight: 400;
            }

            #rememberCheckbox {
                color: #CBD5E1;
                font-size: 13px;
                font-weight: 500;
                spacing: 8px;
            }

            #rememberCheckbox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #475569;
                border-radius: 4px;
                background-color: #0F172A;
            }

            #rememberCheckbox::indicator:checked {
                background-color: #3B82F6;
                border-color: #3B82F6;
            }

            #rememberCheckbox::indicator:hover {
                border-color: #3B82F6;
            }

            #errorLabel {
                background-color: rgba(220, 38, 38, 0.12);
                border: 1px solid #DC2626;
                border-radius: 8px;
                color: #FCA5A5;
                font-size: 13px;
                font-weight: 600;
                padding: 12px 16px;
            }

            #primaryButton {
                background-color: #3B82F6;
                border: none;
                border-radius: 8px;
                color: #FFFFFF;
                font-size: 15px;
                font-weight: 700;
                letter-spacing: 0.3px;
            }

            #primaryButton:hover {
                background-color: #2563EB;
            }

            #primaryButton:pressed {
                background-color: #1D4ED8;
            }

            #switchLabel {
                color: #94A3B8;
                font-size: 13px;
                font-weight: 500;
            }

            #linkButton {
                background-color: transparent;
                border: none;
                color: #3B82F6;
                font-size: 13px;
                font-weight: 700;
                padding: 4px 6px;
            }

            #linkButton:hover {
                color: #60A5FA;
                text-decoration: underline;
            }
        """)

    def get_authenticated_user(self) -> dict:
        """Return the authenticated user data"""
        return self.authenticated_user