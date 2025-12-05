"""
Main application window with user permission management
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QFrame, QStackedWidget, QLabel, QStatusBar, QPushButton, QMessageBox, QDialog
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
from core.database import DatabaseManager


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self, db_manager=None, user_data=None):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.resize(1320, 840)

        # Initialize database manager (use provided or create new)
        if db_manager:
            self.db_manager = db_manager
        else:
            self.db_manager = DatabaseManager(
                host="localhost",
                port=3306,
                user="root",
                password="",
                database="backmeup_system"
            )

        # Store authenticated user data
        self.user_data = user_data or {}

        # Apply styles with logout button styling
        self._apply_styles()
        self._init_ui()

    def _apply_styles(self):
        """Apply application styles including logout button"""
        # Extend the existing theme with logout button styles
        logout_styles = """
        /* Logout Button Styles */
        #logoutButton {
            background-color: rgba(239, 68, 68, 0.1);
            border: 2px solid #DC2626;
            border-radius: 10px;
            color: #FCA5A5;
            font-size: 14px;
            font-weight: 600;
            padding: 0 16px;
            text-align: left;
        }

        #logoutButton:hover {
            background-color: rgba(239, 68, 68, 0.2);
            border-color: #EF4444;
            color: #FEE2E2;
        }

        #logoutButton:pressed {
            background-color: rgba(220, 38, 38, 0.3);
            border-color: #B91C1C;
        }

        #logoutButton[collapsed="true"] {
            text-align: center;
            padding: 0;
        }

        #footerSeparator {
            background-color: #334155;
            border: none;
        }
        """

        # Combine existing theme with logout styles
        complete_stylesheet = MODERN_GRAY_THEME + logout_styles
        self.setStyleSheet(complete_stylesheet)

    def _init_ui(self):
        """Initialize user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar with logout functionality and role-based access
        self.sidebar = Sidebar(user_data=self.user_data)
        self.sidebar.page_changed.connect(self.switch_page)
        self.sidebar.logout_requested.connect(self.handle_logout)
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

        # Pass user_data to DatabasesPage for permission checking
        self.databases_page = DatabasesPage(user_data=self.user_data)
        self.stack.addWidget(self.databases_page)

        self.stack.addWidget(BackupsPage())

        # Pass database manager and user data to UsersPage
        self.users_page = UsersPage(db_manager=self.db_manager, user_data=self.user_data)

        # Connect users page signals
        self.users_page.save_permissions_requested.connect(self._handle_save_permissions)
        self.users_page.add_user_requested.connect(self._handle_add_user)
        self.users_page.edit_user_requested.connect(self._handle_edit_user)
        self.users_page.delete_user_requested.connect(self._handle_delete_user)

        self.stack.addWidget(self.users_page)
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
        """Create top bar with breadcrumbs and user info"""
        top_bar = QFrame()
        top_bar.setObjectName("topBar")
        top_bar.setFixedHeight(64)

        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(32, 0, 32, 0)

        self.breadcrumb = QLabel("Home / Dashboard")
        self.breadcrumb.setObjectName("breadcrumb")
        layout.addWidget(self.breadcrumb)

        layout.addStretch()

        # User info display
        if self.user_data:
            username = self.user_data.get('username', 'User')
            full_name = self.user_data.get('full_name', '')
            display_name = full_name if full_name else username

            user_label = QLabel(f"Logged in as: {display_name}")
            user_label.setObjectName("userLabel")
            user_label.setStyleSheet("""
                color: #94A3B8;
                font-size: 13px;
                font-weight: 500;
                padding-right: 16px;
            """)
            layout.addWidget(user_label)

        return top_bar

    def switch_page(self, index: int, page_name: str):
        """Switch to selected page with role-based access control"""
        # Get user role
        user_role = self.user_data.get('role', 'user') if self.user_data else 'user'
        is_admin = user_role.lower() in ['admin', 'superadmin']

        # Restrict access to Users (index 3) and Settings (index 4) for non-admin users
        if index in [3, 4] and not is_admin:
            QMessageBox.warning(
                self,
                "Access Denied",
                "You do not have permission to access this page.\n\n"
                "Only administrators can access Users & Access Control and Settings."
            )
            # Reset to dashboard
            self.stack.setCurrentIndex(0)
            self.breadcrumb.setText("Home / Dashboard")

            # Update sidebar selection
            if self.sidebar.button_group.button(0):
                self.sidebar.button_group.button(0).setChecked(True)
            return

        # Allow access
        self.stack.setCurrentIndex(index)
        self.breadcrumb.setText(f"Home / {page_name}")

    # ==================== USER PERMISSION HANDLERS ====================

    def _handle_save_permissions(self, username: str, permissions_data: dict):
        """Handle saving user permissions to database"""
        try:
            if not self.db_manager or not self.db_manager.connection:
                QMessageBox.critical(
                    self,
                    "Database Error",
                    "No database connection available."
                )
                return

            # Ensure connection is active
            if not self.db_manager.connection.is_connected():
                self.db_manager.connect()

            cursor = self.db_manager.connection.cursor()

            # Get the admin username who is granting permissions
            granted_by = self.user_data.get('username', 'admin')

            # Delete existing permissions for this user
            delete_query = "DELETE FROM user_permissions WHERE username = %s"
            cursor.execute(delete_query, (username,))

            # Insert new permissions (only those that are checked)
            insert_query = """
                INSERT INTO user_permissions 
                (username, database_name, permission_type, granted_by) 
                VALUES (%s, %s, %s, %s)
            """

            permissions_count = 0
            for db_name, perms in permissions_data.items():
                # Remove bullet point if present
                clean_db_name = db_name.replace("• ", "").strip()

                for perm_type, is_granted in perms.items():
                    if is_granted:  # Only insert checked permissions
                        cursor.execute(
                            insert_query,
                            (username, clean_db_name, perm_type, granted_by)
                        )
                        permissions_count += 1

            # Commit the transaction
            self.db_manager.connection.commit()
            cursor.close()

            # Show success message
            QMessageBox.information(
                self,
                "Permissions Updated",
                f"Successfully updated permissions for user '{username}'.\n\n"
                f"Total permissions granted: {permissions_count}"
            )
            print(f"✓ Saved {permissions_count} permissions for user: {username}")

        except Exception as e:
            # Rollback on error
            if self.db_manager and self.db_manager.connection:
                self.db_manager.connection.rollback()

            error_msg = str(e)

            # Check if user_permissions table doesn't exist
            if "doesn't exist" in error_msg or "Table" in error_msg:
                QMessageBox.critical(
                    self,
                    "Database Setup Required",
                    "The 'user_permissions' table does not exist.\n\n"
                    "Please run the SQL schema file to create the required table:\n"
                    "user_permissions_schema.sql\n\n"
                    f"Error: {error_msg}"
                )
            else:
                QMessageBox.critical(
                    self,
                    "Error Saving Permissions",
                    f"Failed to save permissions for user '{username}'.\n\n"
                    f"Error: {error_msg}"
                )

            print(f"✗ Error saving permissions: {error_msg}")

    def _handle_add_user(self):
        """Handle add new user request"""
        # TODO: Implement add user dialog
        QMessageBox.information(
            self,
            "Add User",
            "Add user functionality will be implemented here.\n\n"
            "This will open a dialog to create a new database user with:\n"
            "• Username\n"
            "• Password\n"
            "• Email\n"
            "• Role\n"
            "• Initial permissions"
        )
        print("Add user requested")

    def _handle_edit_user(self, username: str):
        """Handle edit user request"""
        # Note: In the updated version, Edit button selects the user
        # This handler is kept for backward compatibility or future use
        print(f"Edit user: {username}")

    def _handle_delete_user(self, username: str):
        """Handle delete user from database"""
        try:
            if not self.db_manager or not self.db_manager.connection:
                return

            # Ensure connection
            if not self.db_manager.connection.is_connected():
                self.db_manager.connect()

            cursor = self.db_manager.connection.cursor()

            # Check if trying to delete yourself
            if username == self.user_data.get('username'):
                QMessageBox.warning(
                    self,
                    "Cannot Delete",
                    "You cannot delete your own user account while logged in."
                )
                return

            # Soft delete - set is_active to 0
            update_query = "UPDATE users SET is_active = 0 WHERE username = %s"
            cursor.execute(update_query, (username,))

            # Also delete their permissions
            delete_perms_query = "DELETE FROM user_permissions WHERE username = %s"
            cursor.execute(delete_perms_query, (username,))

            self.db_manager.connection.commit()
            cursor.close()

            # Reload users list
            if hasattr(self.users_page, '_load_users_from_database'):
                self.users_page._load_users_from_database()

            print(f"✓ Deleted user: {username}")

        except Exception as e:
            if self.db_manager and self.db_manager.connection:
                self.db_manager.connection.rollback()

            QMessageBox.critical(
                self,
                "Error Deleting User",
                f"Failed to delete user '{username}'.\n\nError: {str(e)}"
            )
            print(f"✗ Error deleting user: {e}")

    # ==================== LOGOUT HANDLER ====================

    def handle_logout(self):
        """Handle logout request from sidebar"""
        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            'Logout Confirmation',
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Clear user session
            self.user_data = None

            # Close database connection if needed
            if self.db_manager and hasattr(self.db_manager, 'connection'):
                try:
                    if self.db_manager.connection and self.db_manager.connection.is_connected():
                        self.db_manager.connection.close()
                except:
                    pass

            # Close main window
            self.close()

            # Show login dialog
            from ui.dialog.login_dialog import LoginDialog
            login_dialog = LoginDialog(self.db_manager)

            if login_dialog.exec() == QDialog.Accepted:
                # User logged in again - create new main window
                authenticated_user = login_dialog.get_authenticated_user()
                new_window = MainWindow(self.db_manager, authenticated_user)
                new_window.show()
            else:
                # User cancelled login - application will close
                pass