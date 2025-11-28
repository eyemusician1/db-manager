"""
Users and access control page with modern card-based design
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QTableWidget, QTableWidgetItem, QGridLayout,
    QCheckBox, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor


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
    """Users and permissions management page with modern design"""
    
    # Signals for actions
    add_user_requested = Signal()
    edit_user_requested = Signal(str)
    delete_user_requested = Signal(str)
    save_permissions_requested = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_user = "admin"
        self._init_ui()
    
    def _init_ui(self):
        """Initialize users page UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(40)
        
        # Page header
        header_frame = self._create_page_header()
        layout.addWidget(header_frame)
        
        # Users list
        users_frame = self._create_users_list()
        layout.addWidget(users_frame)
        
        # Permissions grid
        permissions_frame = self._create_permissions_grid()
        layout.addWidget(permissions_frame)
        
        layout.addStretch()
    
    def _create_page_header(self):
        """Create clean page header matching databases page"""
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)
        
        title = QLabel("Users & Access Control")
        title.setStyleSheet("""
            font-size: 36px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: -1.2px;
        """)
        
        subtitle = QLabel("Manage database users and their permissions")
        subtitle.setStyleSheet("""
            color: #b8a5d8;
            font-size: 16px;
            font-weight: 500;
        """)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        return header_frame
    
    def _create_users_list(self):
        """Create users list section with modern design"""
        users_frame = QFrame()
        users_frame.setObjectName("contentCard")
        users_layout = QVBoxLayout(users_frame)
        users_layout.setContentsMargins(32, 28, 32, 28)
        users_layout.setSpacing(24)
        
        # Header with title and add button
        header_layout = QHBoxLayout()
        header_layout.setSpacing(0)
        
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
        self.users_table.setRowCount(0)
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
        
        # Sample users data
        users_data = [
            ("◉ admin", "Administrator", "2 hours ago"),
            ("◉ developer", "Developer", "1 day ago"),
            ("◉ analyst", "Read Only", "3 days ago"),
        ]
        
        for user, role, login in users_data:
            self._add_user_row(user, role, login)
        
        users_layout.addWidget(self.users_table)
        
        return users_frame
    
    def _add_user_row(self, username: str, role: str, last_login: str):
        """Add a row to users table with action buttons"""
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
        
        # Edit button
        btn_edit = ActionButton("✎", "Edit User")
        btn_edit.clicked.connect(lambda checked=False, name=username: self._handle_edit_user(name))
        
        # Delete button (destructive)
        btn_delete = ActionButton("×", "Delete User", "destructive")
        btn_delete.clicked.connect(lambda checked=False, name=username: self._handle_delete_user(name))
        
        actions_layout.addWidget(btn_edit)
        actions_layout.addWidget(btn_delete)
        
        self.users_table.setCellWidget(row, 3, actions_widget)
        self.users_table.setRowHeight(row, 75)
    
    def _create_permissions_grid(self):
        """Create permissions grid section with modern design"""
        permissions_frame = QFrame()
        permissions_frame.setObjectName("contentCard")
        permissions_layout = QVBoxLayout(permissions_frame)
        permissions_layout.setContentsMargins(32, 28, 32, 28)
        permissions_layout.setSpacing(24)
        
        # Title
        perm_title = QLabel(f"PERMISSIONS (SELECTED USER: {self.selected_user.upper()})")
        perm_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: 0.5px;
        """)
        permissions_layout.addWidget(perm_title)
        
        # Permissions grid
        perm_grid_widget = QWidget()
        perm_grid = QGridLayout(perm_grid_widget)
        perm_grid.setSpacing(16)
        perm_grid.setContentsMargins(0, 16, 0, 16)
        
        # Header row styling
        header_label = QLabel("Database/Table")
        header_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 700;
            color: #b8a5d8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        """)
        perm_grid.addWidget(header_label, 0, 0)
        
        # Permission column headers
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
        databases = ["◆ production_db", "◆ staging_db", "◆ test_db"]
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
                checkbox.setChecked(row == 1 or (row == 2 and col in [1, 2, 3]))  # Sample data
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
                        image: url(none);
                    }
                    QCheckBox::indicator:checked:after {
                        content: "✓";
                        color: white;
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
        btn_save_perms = QPushButton("↓ Save Permissions")
        btn_save_perms.setObjectName("primaryButton")
        btn_save_perms.setMinimumHeight(44)
        btn_save_perms.setCursor(Qt.PointingHandCursor)
        btn_save_perms.clicked.connect(self._handle_save_permissions)
        permissions_layout.addWidget(btn_save_perms)
        
        return permissions_frame
    
    # Event Handlers
    
    def _handle_add_user(self):
        """Handle add user button click"""
        self.add_user_requested.emit()
        QMessageBox.information(
            self,
            "Add User",
            "Add new database user dialog will open here.\n\nYou can set username, password, and default permissions."
        )
    
    def _handle_edit_user(self, username: str):
        """Handle edit user button click"""
        clean_username = username.replace("◉ ", "")
        self.edit_user_requested.emit(clean_username)
        QMessageBox.information(
            self,
            "Edit User",
            f"Edit user dialog will open here for: {clean_username}"
        )
    
    def _handle_delete_user(self, username: str):
        """Handle delete user button click with confirmation"""
        clean_username = username.replace("◉ ", "")
        
        dialog = ConfirmationDialog(
            self,
            "⚠️ Confirm User Deletion",
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
    
    def _handle_save_permissions(self):
        """Handle save permissions button click"""
        # Collect all permission states
        permissions_data = {}
        for db, perms in self.permission_checkboxes.items():
            db_name = db.replace("◆ ", "")
            permissions_data[db_name] = {}
            for perm_name, checkbox in perms.items():
                permissions_data[db_name][perm_name] = checkbox.isChecked()
        
        self.save_permissions_requested.emit(permissions_data)
        
        QMessageBox.information(
            self,
            "Permissions Saved",
            f"Permissions for user '{self.selected_user}' have been successfully updated.\n\n"
            "The changes will take effect immediately."
        )
