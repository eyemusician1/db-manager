"""

Users and access control page with user selection and permission editing

"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QTableWidget, QTableWidgetItem, QGridLayout,
    QCheckBox, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from datetime import datetime


class ActionButton(QPushButton):
    """Custom action button with icon and enhanced hover effects"""

    def __init__(self, icon: str, tooltip: str, button_type: str = "normal", parent=None):
        super().__init__(icon, parent)
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(36, 36)
        self.button_type = button_type

        # Different styles for destructive actions
        if button_type == "destructive":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #4A5578;
                    border: 1px solid #5A6588;
                    border-radius: 6px;
                    color: #FF6B6B;
                    font-size: 18px;
                    font-weight: 700;
                    padding: 0px;
                }
                QPushButton:hover {
                    background-color: #EF4444;
                    border-color: #DC2626;
                    color: #FFFFFF;
                    transform: scale(1.05);
                }
                QPushButton:pressed {
                    background-color: #DC2626;
                    transform: scale(0.95);
                }
                QPushButton:disabled {
                    background-color: #3A4558;
                    border-color: #4A5578;
                    color: #6B7280;
                    opacity: 0.5;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #4A5578;
                    border: 1px solid #5A6588;
                    border-radius: 6px;
                    color: #E0E7FF;
                    font-size: 16px;
                    font-weight: 700;
                    padding: 0px;
                }
                QPushButton:hover {
                    background-color: #0EA5E9;
                    border-color: #0EA5E9;
                    color: #FFFFFF;
                    transform: scale(1.05);
                }
                QPushButton:pressed {
                    background-color: #0284C7;
                    transform: scale(0.95);
                }
                QPushButton:disabled {
                    background-color: #3A4558;
                    border-color: #4A5578;
                    color: #6B7280;
                    opacity: 0.5;
                }
            """)


class ConfirmationDialog(QMessageBox):
    """Custom confirmation dialog with better styling"""

    def __init__(self, parent, title, message, warning_text=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(message)
        if warning_text:
            self.setInformativeText(warning_text)
        self.setIcon(QMessageBox.Warning)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setDefaultButton(QMessageBox.No)

        # Style the dialog
        self.setStyleSheet("""
            QMessageBox {
                background-color: #1E293B;
                color: #E0E7FF;
            }
            QMessageBox QLabel {
                color: #E0E7FF;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4A5578;
                border: 1px solid #5A6588;
                border-radius: 6px;
                color: #E0E7FF;
                padding: 8px 20px;
                font-weight: 600;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0EA5E9;
                border-color: #0EA5E9;
            }
            QPushButton[text="&Yes"] {
                background-color: #DC2626;
                border-color: #B91C1C;
            }
            QPushButton[text="&Yes"]:hover {
                background-color: #EF4444;
                border-color: #DC2626;
            }
        """)


class UsersPage(QWidget):
    """Users and permissions management page with user selection"""

    # Signals for actions
    add_user_requested = Signal()
    edit_user_requested = Signal(str)
    delete_user_requested = Signal(str)
    save_permissions_requested = Signal(str, dict)  # username, permissions

    def __init__(self, parent=None, db_manager=None, user_data=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.user_data = user_data or {}
        self.selected_user = None  # No user selected initially
        self.authenticated_admin = self.user_data.get('username', 'Admin')
        self.content_widget = None

        # Store references to UI elements that need updating
        self.perm_title = None
        self.permission_checkboxes = {}

        self._init_ui()

    def _init_ui(self):
        """Initialize users page UI"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Show content directly
        self._show_content()

    def _show_content(self):
        """Display the actual users page content"""
        # Clear existing content
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Create content widget
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(48, 48, 48, 48)
        content_layout.setSpacing(40)

        # Page header
        header_frame = self._create_page_header()
        content_layout.addWidget(header_frame)

        # Users list
        users_frame = self._create_users_list()
        content_layout.addWidget(users_frame)

        # Permissions grid
        permissions_frame = self._create_permissions_grid()
        content_layout.addWidget(permissions_frame)

        content_layout.addStretch()

        self.main_layout.addWidget(self.content_widget)

    def _create_page_header(self):
        """Create page header"""
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        # Title with auth badge
        title_container = QHBoxLayout()

        title = QLabel("Users & Access Control")
        title.setStyleSheet("""
            font-size: 36px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: -1.2px;
        """)

        # User badge
        user_badge = QLabel(f"Logged in as {self.authenticated_admin}")
        user_badge.setStyleSheet("""
            background-color: #065F46;
            color: #D1FAE5;
            font-size: 13px;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 16px;
            margin-left: 16px;
        """)

        title_container.addWidget(title)
        title_container.addWidget(user_badge)
        title_container.addStretch()

        subtitle = QLabel("Manage database users and their permissions")
        subtitle.setStyleSheet("""
            color: #b8a5d8;
            font-size: 16px;
            font-weight: 500;
        """)

        header_layout.addLayout(title_container)
        header_layout.addWidget(subtitle)

        return header_frame

    def _create_users_list(self):
        """Create users list section"""
        users_frame = QFrame()
        users_frame.setObjectName("contentCard")
        users_layout = QVBoxLayout(users_frame)
        users_layout.setContentsMargins(32, 28, 32, 28)
        users_layout.setSpacing(24)

        # Header
        header_layout = QHBoxLayout()

        users_title = QLabel("DATABASE USERS")
        users_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: 0.5px;
        """)

        btn_add_user = QPushButton("+ New User")
        btn_add_user.setObjectName("primaryButton")
        btn_add_user.setMinimumHeight(44)
        btn_add_user.setCursor(Qt.PointingHandCursor)
        btn_add_user.clicked.connect(self._handle_add_user)

        header_layout.addWidget(users_title)
        header_layout.addStretch()
        header_layout.addWidget(btn_add_user)

        users_layout.addLayout(header_layout)

        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(4)
        self.users_table.setHorizontalHeaderLabels([
            "USER", "ROLE", "LAST LOGIN", "ACTIONS"
        ])

        # Column sizing
        self.users_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.users_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.users_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.users_table.horizontalHeader().resizeSection(3, 120)

        self.users_table.verticalHeader().setVisible(False)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.setSelectionMode(QTableWidget.SingleSelection)
        self.users_table.setShowGrid(False)
        self.users_table.setMinimumHeight(280)

        # Connect row click to select user
        self.users_table.cellClicked.connect(self._on_user_row_clicked)

        # Load users
        self._load_users_from_database()

        users_layout.addWidget(self.users_table)

        return users_frame

    def _add_user_row(self, username: str, role: str, last_login: str):
        """Add a row to users table"""
        row = self.users_table.rowCount()
        self.users_table.insertRow(row)

        # Username
        user_item = QTableWidgetItem(username)
        user_item.setFlags(user_item.flags() & ~Qt.ItemIsEditable)
        self.users_table.setItem(row, 0, user_item)

        # Role
        role_item = QTableWidgetItem(role)
        role_item.setFlags(role_item.flags() & ~Qt.ItemIsEditable)
        self.users_table.setItem(row, 1, role_item)

        # Last Login
        login_item = QTableWidgetItem(last_login)
        login_item.setFlags(login_item.flags() & ~Qt.ItemIsEditable)
        self.users_table.setItem(row, 2, login_item)

        # Actions
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(8, 6, 8, 6)
        actions_layout.setSpacing(8)

        # Edit button (now selects user)
        btn_edit = ActionButton("E", "Edit User Permissions")
        btn_edit.clicked.connect(lambda checked=False, name=username: self._select_user(name))

        # Delete button
        btn_delete = ActionButton("X", "Delete User", "destructive")
        btn_delete.clicked.connect(lambda checked=False, name=username: self._handle_delete_user(name))

        actions_layout.addWidget(btn_edit)
        actions_layout.addWidget(btn_delete)

        self.users_table.setCellWidget(row, 3, actions_widget)
        self.users_table.setRowHeight(row, 75)

    def _create_permissions_grid(self):
        """Create permissions grid section"""
        permissions_frame = QFrame()
        permissions_frame.setObjectName("contentCard")
        permissions_layout = QVBoxLayout(permissions_frame)
        permissions_layout.setContentsMargins(32, 28, 32, 28)
        permissions_layout.setSpacing(24)

        # Title (will be updated when user is selected)
        self.perm_title = QLabel(self._get_permissions_title())
        self.perm_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: 0.5px;
        """)
        permissions_layout.addWidget(self.perm_title)

        # Permissions grid
        perm_grid_widget = QWidget()
        perm_grid = QGridLayout(perm_grid_widget)
        perm_grid.setSpacing(16)
        perm_grid.setContentsMargins(0, 16, 0, 16)

        # Headers
        header_label = QLabel("DATABASE/TABLE")
        header_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 700;
            color: #b8a5d8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        """)
        perm_grid.addWidget(header_label, 0, 0)

        permissions = ["INSERT", "DELETE", "UPDATE", "CREATE"]
        for col, perm in enumerate(permissions, 1):
            label = QLabel(perm)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                font-size: 14px;
                font-weight: 700;
                color: #b8a5d8;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            """)
            perm_grid.addWidget(label, 0, col)

        # Database rows
        databases = self._get_databases_list()
        self.permission_checkboxes = {}

        for row, db in enumerate(databases, 1):
            db_label = QLabel(db)
            db_label.setStyleSheet("""
                font-size: 14px;
                font-weight: 600;
                color: #E0E7FF;
            """)
            perm_grid.addWidget(db_label, row, 0)

            self.permission_checkboxes[db] = {}

            for col, perm in enumerate(permissions, 1):
                checkbox = QCheckBox()
                checkbox.setChecked(False)
                checkbox.setCursor(Qt.PointingHandCursor)
                checkbox.setStyleSheet("""
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

                checkbox_container = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_container)
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)

                perm_grid.addWidget(checkbox_container, row, col)
                self.permission_checkboxes[db][perm] = checkbox

        permissions_layout.addWidget(perm_grid_widget)

        # Save button
        btn_save_perms = QPushButton("Save Permissions")
        btn_save_perms.setObjectName("primaryButton")
        btn_save_perms.setMinimumHeight(44)
        btn_save_perms.setCursor(Qt.PointingHandCursor)
        btn_save_perms.clicked.connect(self._handle_save_permissions)
        permissions_layout.addWidget(btn_save_perms)

        return permissions_frame

    def _get_permissions_title(self):
        """Get permissions section title based on selected user"""
        if self.selected_user:
            clean_name = self.selected_user.replace("• ", "").strip()
            return f"PERMISSIONS (SELECTED USER: {clean_name.upper()})"
        else:
            return "PERMISSIONS (SELECT A USER TO MANAGE)"

    def _on_user_row_clicked(self, row, column):
        """Handle user row click"""
        username_item = self.users_table.item(row, 0)
        if username_item:
            username = username_item.text()
            self._select_user(username)

    def _select_user(self, username: str):
        """Select a user and load their permissions"""
        clean_username = username.replace("• ", "").strip()
        self.selected_user = clean_username

        # Update permissions title
        if self.perm_title:
            self.perm_title.setText(self._get_permissions_title())

        # Load user's permissions
        self._load_user_permissions(clean_username)

        # Show feedback
        print(f"Selected user: {clean_username}")

    def _load_user_permissions(self, username: str):
        """Load permissions for the selected user from database"""
        try:
            if not self.db_manager or not self.db_manager.connection:
                return

            cursor = self.db_manager.connection.cursor(dictionary=True)

            # Query user permissions from database
            # This is a simplified example - adjust based on your schema
            query = """
                SELECT database_name, permission_type
                FROM user_permissions
                WHERE username = %s
            """

            cursor.execute(query, (username,))
            permissions = cursor.fetchall()
            cursor.close()

            # Reset all checkboxes first
            for db, perms in self.permission_checkboxes.items():
                for perm_name, checkbox in perms.items():
                    checkbox.setChecked(False)

            # Apply user's permissions
            for perm in permissions:
                db_name = f"• {perm['database_name']}"
                perm_type = perm['permission_type'].upper()

                if db_name in self.permission_checkboxes:
                    if perm_type in self.permission_checkboxes[db_name]:
                        self.permission_checkboxes[db_name][perm_type].setChecked(True)

        except Exception as e:
            print(f"Error loading user permissions: {e}")
            # If table doesn't exist or error, just reset all checkboxes
            for db, perms in self.permission_checkboxes.items():
                for perm_name, checkbox in perms.items():
                    checkbox.setChecked(False)

    def _handle_add_user(self):
        """Handle add user"""
        self.add_user_requested.emit()
        QMessageBox.information(
            self,
            "Add User",
            "Add new database user dialog will open here.\n\nYou can set username, password, and default permissions."
        )

    def _handle_delete_user(self, username: str):
        """Handle delete user with confirmation"""
        clean_username = username.replace("• ", "").strip()

        dialog = ConfirmationDialog(
            self,
            "Confirm User Deletion",
            f"Are you sure you want to delete user '{clean_username}'?",
            "This will revoke all database access for this user.\nThis action cannot be undone."
        )

        reply = dialog.exec()
        if reply == QMessageBox.Yes:
            self.delete_user_requested.emit(clean_username)
            QMessageBox.information(
                self,
                "User Deleted",
                f"User '{clean_username}' has been successfully deleted."
            )
            # Reload users list
            self._load_users_from_database()

    def _handle_save_permissions(self):
        """Handle save permissions"""
        if not self.selected_user:
            QMessageBox.warning(
                self,
                "No User Selected",
                "Please select a user first to manage their permissions."
            )
            return

        # Collect permissions
        permissions_data = {}
        for db, perms in self.permission_checkboxes.items():
            db_name = db.replace("• ", "").strip()
            permissions_data[db_name] = {}
            for perm_name, checkbox in perms.items():
                permissions_data[db_name][perm_name] = checkbox.isChecked()

        self.save_permissions_requested.emit(self.selected_user, permissions_data)

        QMessageBox.information(
            self,
            "Permissions Saved",
            f"Permissions for user '{self.selected_user}' have been successfully updated.\n\n"
            "The changes will take effect immediately."
        )

    def _load_users_from_database(self):
        """Load users from database"""
        # Clear existing rows
        self.users_table.setRowCount(0)

        try:
            if not self.db_manager:
                return

            if not self.db_manager.connection or not self.db_manager.connection.is_connected():
                self.db_manager.connect()

            if not self.db_manager.connection or not self.db_manager.connection.is_connected():
                QMessageBox.warning(
                    self,
                    "Connection Error",
                    "Unable to connect to database."
                )
                return

            cursor = self.db_manager.connection.cursor(dictionary=True)

            try:
                query = """
                    SELECT username, role, last_login, created_at
                    FROM users
                    WHERE is_active = 1
                    ORDER BY username
                """
                cursor.execute(query)
                users = cursor.fetchall()

                if users:
                    for user in users:
                        username = user['username']
                        role = user.get('role', 'User')
                        last_login = user.get('last_login')

                        # Format last login
                        last_login_str = "Never"
                        if last_login:
                            try:
                                if isinstance(last_login, str):
                                    last_login_dt = datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S')
                                else:
                                    last_login_dt = last_login

                                now = datetime.now()
                                diff = now - last_login_dt

                                if diff.days > 0:
                                    last_login_str = f"{diff.days} day(s) ago"
                                elif diff.seconds > 3600:
                                    hours = diff.seconds // 3600
                                    last_login_str = f"{hours} hour(s) ago"
                                elif diff.seconds > 60:
                                    minutes = diff.seconds // 60
                                    last_login_str = f"{minutes} minute(s) ago"
                                else:
                                    last_login_str = "Just now"
                            except Exception:
                                last_login_str = "Never"

                        self._add_user_row(f"• {username}", role, last_login_str)
                else:
                    self._load_mysql_users(cursor)

            except Exception as e:
                print(f"users table not found: {e}")
                self._load_mysql_users(cursor)

            cursor.close()

        except Exception as e:
            print(f"Error loading users: {e}")
            QMessageBox.warning(
                self,
                "Error",
                f"Failed to load users: {str(e)}"
            )

    def _load_mysql_users(self, cursor):
        """Load users from MySQL user table"""
        try:
            query = """
                SELECT User, Host
                FROM mysql.user
                WHERE User NOT IN ('', 'mysql.sys', 'mysql.session', 'mysql.infoschema')
                ORDER BY User
            """
            cursor.execute(query)
            mysql_users = cursor.fetchall()

            if mysql_users:
                for user in mysql_users:
                    username = user['User']
                    host = user['Host']
                    role = "Administrator" if username == 'root' else "Database User"
                    self._add_user_row(f"• {username}@{host}", role, "Never")
        except Exception as e:
            print(f"Error loading MySQL users: {e}")

    def _get_databases_list(self):
        """Get list of databases"""
        try:
            if not self.db_manager:
                return ["• backmeup_system", "• classicmodels", "• test_database"]

            databases = self.db_manager.get_databases()
            if databases:
                return [f"• {db}" for db in databases]
            else:
                return ["• backmeup_system", "• classicmodels", "• test_database"]
        except Exception as e:
            print(f"Error getting databases: {e}")
            return ["• backmeup_system", "• classicmodels", "• test_database"]