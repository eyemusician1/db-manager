"""
DB Manager Application Entry Point
"""
import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QFont
from ui.main_window import MainWindow
from ui.dialog.login_dialog import LoginDialog
from core.database import DatabaseManager


def main():
    app = QApplication(sys.argv)
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Initialize database manager
    db_manager = DatabaseManager(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="backmeup_system"
    )
    
    # Show login dialog first
    login_dialog = LoginDialog(db_manager)
    
    if login_dialog.exec() == LoginDialog.Accepted:
        # Get authenticated user data
        user_data = login_dialog.get_authenticated_user()
        
        if user_data:
            # Show main window with authenticated user
            window = MainWindow(db_manager=db_manager, user_data=user_data)
            window.show()
            sys.exit(app.exec())
        else:
            QMessageBox.warning(
                None,
                "Authentication Failed",
                "Failed to authenticate user. Please try again."
            )
            sys.exit(1)
    else:
        # User cancelled login
        sys.exit(0)


if __name__ == "__main__":
    main()
