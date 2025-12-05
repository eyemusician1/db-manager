"""
Database management page with modern card-based design - Fully Functional
Version: 2.0 - Refactored for better debugging and maintainability
"""
from core.permission_checker import PermissionChecker
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QDialog, QLineEdit,
    QDialogButtonBox, QFormLayout, QComboBox, QCheckBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from core.database import DatabaseManager
import subprocess
import os
from datetime import datetime
import traceback





# ============================================================================
# HELPER CLASSES - Action Buttons and Dialogs
# ============================================================================

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
                }
                QPushButton:pressed {
                    background-color: #DC2626;
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
                }
                QPushButton:pressed {
                    background-color: #0284C7;
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


# ============================================================================
# DATABASE DIALOGS
# ============================================================================

class NewDatabaseDialog(QDialog):
    """Dialog for creating a new database"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Database")
        self.setMinimumWidth(400)
        self._init_ui()
        print("[DEBUG] NewDatabaseDialog initialized")
    
    def _init_ui(self):
        layout = QFormLayout(self)
        
        self.db_name_input = QLineEdit()
        self.db_name_input.setPlaceholderText("Enter database name (e.g., my_database)")
        self.db_name_input.setMinimumHeight(36)
        
        layout.addRow("Database Name:", self.db_name_input)
        
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addRow(button_box)
    
    def get_database_name(self):
        name = self.db_name_input.text().strip()
        print(f"[DEBUG] Database name entered: {name}")
        return name


# ============================================================================
# TABLE DIALOGS
# ============================================================================

class CreateTableDialog(QDialog):
    """Dialog for creating a new table with columns"""
    
    def __init__(self, db_name, parent=None):
        super().__init__(parent)
        self.db_name = db_name
        self.setWindowTitle(f"Create New Table in '{db_name}'")
        self.setMinimumWidth(650)
        self.setMinimumHeight(450)
        self.columns = []
        self._init_ui()
        print(f"[DEBUG] CreateTableDialog initialized for database: {db_name}")
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # Instructions
        instructions = QLabel("Create a new table by entering a name and defining at least one column:")
        instructions.setStyleSheet("color: #b8a5d8; font-size: 13px; margin-bottom: 8px;")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Table name input
        form_layout = QFormLayout()
        form_layout.setSpacing(8)
        
        self.table_name_input = QLineEdit()
        self.table_name_input.setPlaceholderText("e.g., users, products, orders")
        self.table_name_input.setMinimumHeight(40)
        self.table_name_input.setStyleSheet("""
            QLineEdit {
                background-color: #2A2F4A;
                border: 2px solid #3A4560;
                border-radius: 6px;
                padding: 0 12px;
                color: #E0E7FF;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0EA5E9;
            }
        """)
        
        table_label = QLabel("Table Name:")
        table_label.setStyleSheet("font-weight: bold; color: #E0E7FF; font-size: 14px;")
        form_layout.addRow(table_label, self.table_name_input)
        
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        
        # Columns section
        columns_header = QHBoxLayout()
        columns_label = QLabel("Columns:")
        columns_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #E0E7FF;")
        columns_header.addWidget(columns_label)
        
        columns_hint = QLabel("(Define the structure of your table)")
        columns_hint.setStyleSheet("color: #7C8BA8; font-size: 12px;")
        columns_header.addWidget(columns_hint)
        columns_header.addStretch()
        
        layout.addLayout(columns_header)
        
        # Columns table
        self.columns_table = QTableWidget()
        self.columns_table.setColumnCount(6)
        self.columns_table.setHorizontalHeaderLabels([
            "Column Name", "Data Type", "Primary Key", "Auto Increment", "NOT NULL", "Remove"
        ])
        self.columns_table.horizontalHeader().setStretchLastSection(False)
        self.columns_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.columns_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.columns_table.setMinimumHeight(200)
        self.columns_table.setStyleSheet("""
            QTableWidget {
                background-color: #1E293B;
                border: 1px solid #3A4560;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #2D3748;
                color: #E0E7FF;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.columns_table)
        
        # Add column button
        btn_add_column = QPushButton("+ Add Column")
        btn_add_column.setMinimumHeight(38)
        btn_add_column.setStyleSheet("""
            QPushButton {
                background-color: #4A5578;
                color: #E0E7FF;
                border: 1px solid #5A6588;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #5A6588;
            }
        """)
        btn_add_column.clicked.connect(self._add_column_row)
        layout.addWidget(btn_add_column)
        
        # Add first column row by default
        self._add_column_row()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        btn_create = QPushButton("✓ Create Table")
        btn_create.setObjectName("primaryButton")
        btn_create.setMinimumHeight(44)
        btn_create.clicked.connect(self._validate_and_accept)
        
        btn_cancel = QPushButton("✕ Cancel")
        btn_cancel.setObjectName("secondaryButton")
        btn_cancel.setMinimumHeight(44)
        btn_cancel.clicked.connect(self.reject)
        
        button_layout.addWidget(btn_create)
        button_layout.addWidget(btn_cancel)
        
        layout.addLayout(button_layout)
    
    def _validate_and_accept(self):
        """Validate before accepting"""
        table_name = self.table_name_input.text().strip()
        
        if not table_name:
            QMessageBox.warning(
                self,
                "Missing Table Name",
                "Please enter a table name before creating."
            )
            self.table_name_input.setFocus()
            return
        
        # Check if at least one column is defined
        has_columns = False
        for row in range(self.columns_table.rowCount()):
            name_widget = self.columns_table.cellWidget(row, 0)
            if name_widget and name_widget.text().strip():
                has_columns = True
                break
        
        if not has_columns:
            QMessageBox.warning(
                self,
                "No Columns Defined",
                "Please add at least one column to the table.\n\n"
                "Click '+ Add Column' and enter a column name."
            )
            return
        
        # If validation passes, accept the dialog
        self.accept()
    
    def _add_column_row(self):
        """Add a new column definition row"""
        row = self.columns_table.rowCount()
        self.columns_table.insertRow(row)
        print(f"[DEBUG] Adding column row {row}")
        
        # Column name
        name_input = QLineEdit()
        name_input.setPlaceholderText(f"column_{row + 1}" if row > 0 else "id")
        name_input.setStyleSheet("""
            QLineEdit {
                background-color: #2A2F4A;
                border: 1px solid #3A4560;
                border-radius: 4px;
                padding: 4px 8px;
                color: #E0E7FF;
            }
            QLineEdit:focus {
                border: 1px solid #0EA5E9;
            }
        """)
        self.columns_table.setCellWidget(row, 0, name_input)
        
        # Data type
        type_combo = QComboBox()
        type_combo.addItems([
            "INT", 
            "VARCHAR(255)", 
            "TEXT", 
            "DATE", 
            "DATETIME",
            "TIMESTAMP",
            "DECIMAL(10,2)", 
            "BOOLEAN", 
            "BIGINT", 
            "FLOAT",
            "DOUBLE"
        ])
        type_combo.setStyleSheet("""
            QComboBox {
                background-color: #2A2F4A;
                border: 1px solid #3A4560;
                border-radius: 4px;
                padding: 4px 8px;
                color: #E0E7FF;
            }
        """)
        self.columns_table.setCellWidget(row, 1, type_combo)
        
        # Primary Key checkbox
        pk_check = QCheckBox()
        pk_widget = QWidget()
        pk_layout = QHBoxLayout(pk_widget)
        pk_layout.addWidget(pk_check)
        pk_layout.setAlignment(Qt.AlignCenter)
        pk_layout.setContentsMargins(0, 0, 0, 0)
        self.columns_table.setCellWidget(row, 2, pk_widget)
        
        # Auto Increment checkbox
        ai_check = QCheckBox()
        ai_widget = QWidget()
        ai_layout = QHBoxLayout(ai_widget)
        ai_layout.addWidget(ai_check)
        ai_layout.setAlignment(Qt.AlignCenter)
        ai_layout.setContentsMargins(0, 0, 0, 0)
        self.columns_table.setCellWidget(row, 3, ai_widget)
        
        # NOT NULL checkbox
        nn_check = QCheckBox()
        nn_widget = QWidget()
        nn_layout = QHBoxLayout(nn_widget)
        nn_layout.addWidget(nn_check)
        nn_layout.setAlignment(Qt.AlignCenter)
        nn_layout.setContentsMargins(0, 0, 0, 0)
        self.columns_table.setCellWidget(row, 4, nn_widget)
        
        # Remove button
        btn_remove = QPushButton("×")
        btn_remove.setFixedSize(28, 28)
        btn_remove.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border-radius: 4px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        btn_remove.clicked.connect(lambda: self.columns_table.removeRow(row))
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.addWidget(btn_remove)
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        self.columns_table.setCellWidget(row, 5, btn_widget)
        
        # Set row height
        self.columns_table.setRowHeight(row, 45)
    
    def get_table_info(self):
        """Extract table name and column definitions"""
        table_name = self.table_name_input.text().strip()
        columns = []
        
        for row in range(self.columns_table.rowCount()):
            name_widget = self.columns_table.cellWidget(row, 0)
            type_widget = self.columns_table.cellWidget(row, 1)
            pk_widget = self.columns_table.cellWidget(row, 2).findChild(QCheckBox)
            ai_widget = self.columns_table.cellWidget(row, 3).findChild(QCheckBox)
            nn_widget = self.columns_table.cellWidget(row, 4).findChild(QCheckBox)
            
            if name_widget and type_widget:
                col_name = name_widget.text().strip()
                if col_name:  # Only add if column name is not empty
                    columns.append({
                        'name': col_name,
                        'type': type_widget.currentText(),
                        'primary_key': pk_widget.isChecked() if pk_widget else False,
                        'auto_increment': ai_widget.isChecked() if ai_widget else False,
                        'not_null': nn_widget.isChecked() if nn_widget else False
                    })
        
        print(f"[DEBUG] Extracted table info: name='{table_name}', columns={len(columns)}")
        for col in columns:
            print(f"[DEBUG] Column: {col}")
        
        return table_name, columns



class TableDataDialog(QDialog):
    """Dialog for viewing table data"""
    
    def __init__(self, table_name, columns, rows, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Data in table '{table_name}'")
        self.setMinimumSize(800, 500)
        self._init_ui(columns, rows)
        print(f"[DEBUG] TableDataDialog showing {len(rows)} rows, {len(columns)} columns")
    
    def _init_ui(self, columns, rows):
        layout = QVBoxLayout(self)
        
        info_label = QLabel(f"Showing {len(rows)} rows (limited to 100)")
        info_label.setStyleSheet("color: #b8a5d8; font-size: 13px;")
        layout.addWidget(info_label)
        
        # Data table
        table = QTableWidget()
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.setRowCount(len(rows))
        
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value) if value is not None else "NULL")
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                if value is None:
                    item.setForeground(Qt.gray)
                table.setItem(i, j, item)
        
        table.horizontalHeader().setStretchLastSection(True)
        table.setAlternatingRowColors(True)
        layout.addWidget(table)
        
        # Close button
        btn_close = QPushButton("Close")
        btn_close.setMinimumHeight(40)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)


class ViewTablesDialog(QDialog):
    """Enhanced dialog for viewing and managing tables in a database"""
    
    def __init__(self, db_name, tables, db_manager, parent=None):
        super().__init__(parent)
        self.db_name = db_name
        self.db_manager = db_manager
        self.backup_directory = "backups"
        self.setWindowTitle(f"Tables in '{db_name}'")
        self.setMinimumSize(800, 500)
        self._init_ui(tables)
        print(f"[DEBUG] ViewTablesDialog initialized for {db_name} with {len(tables)} tables")
    
    def _init_ui(self, tables):
        layout = QVBoxLayout(self)
        
        # Header with title and New Table button
        header_layout = QHBoxLayout()
        
        title = QLabel(f"Managing {len(tables)} tables in '{self.db_name}':")
        title.setStyleSheet("font-weight: bold; font-size: 16px; color: #e6d9ff;")
        
        btn_new_table = QPushButton("+ New Table")
        btn_new_table.setObjectName("primaryButton")
        btn_new_table.setMinimumHeight(35)
        btn_new_table.setCursor(Qt.PointingHandCursor)
        btn_new_table.clicked.connect(self._create_table)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(btn_new_table)
        
        layout.addLayout(header_layout)
        layout.addSpacing(10)
        
        # Table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Table Name", "Rows", "Actions"])
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.table_widget.horizontalHeader().resizeSection(2, 160)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setShowGrid(False)
        self.table_widget.setMinimumHeight(300)
        
        # Populate tables
        self._populate_tables(tables)
        
        layout.addWidget(self.table_widget)
        
        # Close button
        btn_close = QPushButton("Close")
        btn_close.setObjectName("secondaryButton")
        btn_close.setMinimumHeight(40)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
    
    def _populate_tables(self, tables):
        """Populate the table widget with tables and action buttons"""
        self.table_widget.setRowCount(len(tables))
        
        for i, table_name in enumerate(tables):
            # Table name
            name_item = QTableWidgetItem(table_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table_widget.setItem(i, 0, name_item)
            
            # Get row count
            try:
                cursor = self.db_manager.connection.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM `{self.db_name}`.`{table_name}`")
                row_count = cursor.fetchone()[0]
                cursor.close()
                
                count_item = QTableWidgetItem(str(row_count))
                count_item.setFlags(count_item.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(i, 1, count_item)
                print(f"[DEBUG] Table {table_name} has {row_count} rows")
            except Exception as e:
                print(f"[ERROR] Failed to get row count for {table_name}: {e}")
                count_item = QTableWidgetItem("N/A")
                count_item.setFlags(count_item.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(i, 1, count_item)
            
            # Action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(8, 6, 8, 6)
            actions_layout.setSpacing(8)
            
            # Backup table button
            btn_backup = ActionButton("↓", "Backup Table")
            btn_backup.clicked.connect(lambda checked=False, tbl=table_name: self._backup_table(tbl))
            
            # Drop table button
            btn_drop = ActionButton("×", "Drop Table", "destructive")
            btn_drop.clicked.connect(lambda checked=False, tbl=table_name: self._drop_table(tbl))
            
            # View data button
            btn_view = ActionButton("☰", "View Data")
            btn_view.clicked.connect(lambda checked=False, tbl=table_name: self._view_table_data(tbl))
            
            actions_layout.addWidget(btn_backup)
            actions_layout.addWidget(btn_drop)
            actions_layout.addWidget(btn_view)
            
            self.table_widget.setCellWidget(i, 2, actions_widget)
            self.table_widget.setRowHeight(i, 75)
    
    def _refresh_tables(self):
        """Refresh the table list"""
        print(f"[DEBUG] Refreshing tables for {self.db_name}")
        try:
            cursor = self.db_manager.connection.cursor()
            cursor.execute(f"USE `{self.db_name}`")
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            cursor.close()
            
            self.table_widget.setRowCount(0)
            self._populate_tables(tables)
            print(f"[DEBUG] Refreshed: {len(tables)} tables")
            
        except Exception as e:
            print(f"[ERROR] Failed to refresh tables: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to refresh tables.\n\nError: {str(e)}")
    
    def _create_table(self):
        """Create a new table with improved validation"""
        print(f"[DEBUG] Opening Create Table dialog for {self.db_name}")
        dialog = CreateTableDialog(self.db_name, self)
            # Check permission
        if hasattr(self.parent(), 'permission_checker'):
            perm_checker = self.parent().permission_checker
            if perm_checker and not perm_checker.can_create_table(self.db_name):
                QMessageBox.warning(
                    self,
                    " Permission Denied",
                    f"You do not have permission to create tables in '{self.db_name}'.\n\n"
                    f"Required permission: CREATE on '{self.db_name}'\n"
                    f"Please contact your administrator for access."
                )
                print(f"[PERMISSIONS] ✗ User denied CREATE TABLE in {self.db_name}")
                return

        dialog = CreateTableDialog(self.db_name, self)                   
        if dialog.exec() == QDialog.Accepted:
            table_name, columns = dialog.get_table_info()
            
            print(f"[DEBUG] Table name: '{table_name}', Columns: {columns}")
            
            # Validation
            if not table_name:
                print("[ERROR] No table name provided")
                QMessageBox.warning(
                    self, 
                    "Invalid Input", 
                    "Please enter a table name."
                )
                return
            
            if not columns or len(columns) == 0:
                print("[ERROR] No columns defined")
                QMessageBox.warning(
                    self, 
                    "Invalid Input", 
                    "Please add at least one column to the table."
                )
                return
            
            try:
                # Ensure database connection is active
                if not self.db_manager or not self.db_manager.connection.is_connected():
                    print("[DEBUG] Reconnecting to database")
                    from core.database import DatabaseManager
                    self.db_manager = DatabaseManager()
                    self.db_manager.connect()
                
                # Build CREATE TABLE statement
                column_defs = []
                for col in columns:
                    col_def = f"`{col['name']}` {col['type']}"
                    
                    if col.get('primary_key'):
                        col_def += " PRIMARY KEY"
                    if col.get('auto_increment'):
                        col_def += " AUTO_INCREMENT"
                    if col.get('not_null'):
                        col_def += " NOT NULL"
                    
                    column_defs.append(col_def)
                    print(f"[DEBUG] Column definition: {col_def}")
                
                # Create SQL statement
                create_sql = f"CREATE TABLE `{self.db_name}`.`{table_name}` ({', '.join(column_defs)})"
                print(f"[DEBUG] Executing SQL: {create_sql}")
                
                # Execute CREATE TABLE
                cursor = self.db_manager.connection.cursor()
                cursor.execute(create_sql)
                self.db_manager.connection.commit()  # Ensure changes are committed
                cursor.close()
                
                print(f"[SUCCESS] Table '{table_name}' created successfully in database '{self.db_name}'")
                
                # Show success message
                QMessageBox.information(
                    self,
                    "✓ Success",
                    f"Table '{table_name}' has been created successfully in database '{self.db_name}'!\n\n"
                    f"Columns: {len(columns)}\n"
                    f"You can now view it in phpMyAdmin."
                )
                
                # Refresh the tables list
                self._refresh_tables()
                
            except Exception as e:
                print(f"[ERROR] Failed to create table: {e}")
                import traceback
                traceback.print_exc()
                QMessageBox.critical(
                    self,
                    "✗ Error Creating Table",
                    f"Failed to create table '{table_name}' in database '{self.db_name}'.\n\n"
                    f"Error: {str(e)}\n\n"
                    "Common issues:\n"
                    "• Table already exists\n"
                    "• Invalid column name or data type\n"
                    "• Connection to MySQL lost"
                )

    
    def _backup_table(self, table_name):
        """Backup a specific table using mysqldump"""
        print(f"[DEBUG] Starting backup for table {table_name}")
        try:
            # Create backup directory
            if not os.path.exists(self.backup_directory):
                os.makedirs(self.backup_directory)
                print(f"[DEBUG] Created backup directory: {self.backup_directory}")
            
            # Generate backup filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{self.db_name}_{table_name}_backup_{timestamp}.sql"
            backup_path = os.path.join(self.backup_directory, backup_filename)
            
            # Path to mysqldump
            mysqldump_path = r"C:\xampp\mysql\bin\mysqldump.exe"
            
            if not os.path.exists(mysqldump_path):
                print(f"[ERROR] mysqldump not found at: {mysqldump_path}")
                QMessageBox.warning(
                    self,
                    "mysqldump Not Found",
                    f"mysqldump not found at: {mysqldump_path}\n\nPlease check your XAMPP installation."
                )
                return
            
            # Execute mysqldump
            command = [
                mysqldump_path,
                "-u", "root",
                "-h", "localhost",
                self.db_name,
                table_name
            ]
            
            print(f"[DEBUG] Running command: {' '.join(command)}")
            
            with open(backup_path, 'w') as backup_file:
                result = subprocess.run(
                    command,
                    stdout=backup_file,
                    stderr=subprocess.PIPE,
                    text=True
                )
            
            if result.returncode == 0:
                size_bytes = os.path.getsize(backup_path)
                size_str = f"{size_bytes / 1024:.2f} KB" if size_bytes >= 1024 else f"{size_bytes} B"
                
                print(f"[SUCCESS] Backup created: {backup_filename} ({size_str})")
                QMessageBox.information(
                    self,
                    "Backup Successful",
                    f"Table '{table_name}' has been backed up successfully!\n\n"
                    f"Backup file: {backup_filename}\n"
                    f"Size: {size_str}"
                )
            else:
                print(f"[ERROR] mysqldump failed: {result.stderr}")
                QMessageBox.critical(
                    self,
                    "Backup Failed",
                    f"Failed to backup table.\n\nError: {result.stderr}"
                )
                
        except Exception as e:
            print(f"[ERROR] Backup exception: {e}")
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Backup Error",
                f"An error occurred during backup.\n\nError: {str(e)}"
            )
    
    def _drop_table(self, table_name):
        """Drop a table with confirmation"""
        print(f"[DEBUG] Drop table requested: {table_name}")

        # ========== PERMISSION CHECK - ADD THIS AT THE START ==========
        # Check if user has permission to drop tables in this database
        if hasattr(self.parent(), 'permission_checker'):
            perm_checker = self.parent().permission_checker
            if perm_checker and not perm_checker.can_drop_table(self.db_name):
                QMessageBox.warning(
                    self,
                    "🔒 Permission Denied",
                    f"You do not have permission to drop tables in '{self.db_name}'.\n\n"
                    f"Required permission: DELETE on '{self.db_name}'\n"
                    f"Please contact your administrator for access."
                )
                print(f"[PERMISSIONS] ✗ User denied DROP TABLE {table_name} in {self.db_name}")
                return  # STOP HERE - Do not proceed
        # ========== END PERMISSION CHECK ==========

        # If we get here, user has permission - proceed with confirmation
        reply = QMessageBox.question(
            self,
            "Confirm Drop Table",
            f"Are you sure you want to drop table '{table_name}'?\n\n"
            "This will permanently delete the table and all its data.\n"
            "This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                cursor = self.db_manager.connection.cursor()
                cursor.execute(f"DROP TABLE `{self.db_name}`.`{table_name}`")
                cursor.close()
                print(f"[SUCCESS] Table {table_name} dropped successfully")

                QMessageBox.information(
                    self,
                    "Table Dropped",
                    f"Table '{table_name}' has been successfully dropped."
                )
                self._refresh_tables()
            except Exception as e:
                print(f"[ERROR] Failed to drop table: {e}")
                traceback.print_exc()
                QMessageBox.critical(
                    self,
                    "Error Dropping Table",
                    f"Failed to drop table '{table_name}'.\n\nError: {str(e)}"
                )
    
    def _view_table_data(self, table_name):
        """View table data (first 100 rows)"""
        print(f"[DEBUG] Viewing data for table {table_name}")
        try:
            cursor = self.db_manager.connection.cursor()
            cursor.execute(f"SELECT * FROM `{self.db_name}`.`{table_name}` LIMIT 100")
            rows = cursor.fetchall()
            
            # Get column names
            cursor.execute(f"DESCRIBE `{self.db_name}`.`{table_name}`")
            columns = [col[0] for col in cursor.fetchall()]
            cursor.close()
            
            print(f"[DEBUG] Fetched {len(rows)} rows with {len(columns)} columns")
            
            # Show data dialog
            data_dialog = TableDataDialog(table_name, columns, rows, self)
            data_dialog.exec()
            
        except Exception as e:
            print(f"[ERROR] Failed to load table data: {e}")
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Error Loading Data",
                f"Failed to load data from table '{table_name}'.\n\nError: {str(e)}"
            )


# ============================================================================
# MAIN DATABASES PAGE
# ============================================================================

class DatabasesPage(QWidget):
    """Main databases management page"""
    
    # Signals
    backup_requested = Signal(str)
    drop_requested = Signal(str)
    view_tables_requested = Signal(str)
    restore_requested = Signal(str)
    delete_backup_requested = Signal(str)
    view_details_requested = Signal(str)
    
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.db_manager = None
        self.backup_directory = "backups"
        self.user_data = user_data or {}
        self.permission_checker = None
        print("[DEBUG] DatabasesPage initialized")
        self._init_ui()
        self.load_real_databases()
        self._init_permissions()  


    def _init_permissions(self):
        """Initialize permission checker"""
        if self.user_data and self.db_manager:
            username = self.user_data.get('username', 'unknown')
            role = self.user_data.get('role', 'user')
            self.permission_checker = PermissionChecker(
                self.db_manager,
                username,
                role
            )
            print(f"[PERMISSIONS] ✓ Initialized for {username} ({role})")

    
    def _init_ui(self):
        """Initialize UI components"""
        print("[DEBUG] Initializing DatabasesPage UI")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(40)
        
        header_frame = self._create_page_header()
        layout.addWidget(header_frame)
        
        primary_frame = self._create_primary_databases()
        layout.addWidget(primary_frame)
        
        backup_frame = self._create_backup_databases()
        layout.addWidget(backup_frame)
        
        layout.addStretch()
    
    def load_real_databases(self):
        """Load real databases from MySQL"""
        print("[DEBUG] Loading real databases from MySQL")
        try:
            self.db_manager = DatabaseManager(
                host="localhost",
                port=3306,
                user="root",
                password=""
            )
            
            if self.db_manager.connect():
                databases = self.db_manager.get_databases()
                print(f"[DEBUG] Found {len(databases)} databases: {databases}")
                
                if databases:
                    self.primary_table.setRowCount(0)
                    
                    for db_name in databases:
                        db_info = self.db_manager.get_database_info(db_name)
                        if db_info:
                            self._add_primary_database_row(
                                db_info["name"],
                                db_info["type"],
                                db_info["size"],
                                str(db_info["tables"]),
                                db_info["status"]
                            )
                    
                    print(f"[SUCCESS] Loaded {len(databases)} databases")
                
                self.load_backup_files()
                
        except Exception as e:
            print(f"[ERROR] Failed to load databases: {e}")
            traceback.print_exc()
            QMessageBox.warning(
                self,
                "Connection Error",
                f"Could not connect to MySQL.\n\nError: {str(e)}\n\n"
                "Make sure MySQL is running in XAMPP."
            )
    
    def load_backup_files(self):
        """Load backup files"""
        print("[DEBUG] Loading backup files")
        try:
            if not os.path.exists(self.backup_directory):
                os.makedirs(self.backup_directory)
            
            self.backup_table.setRowCount(0)
            
            backup_files = []
            if os.path.exists(self.backup_directory):
                for file in os.listdir(self.backup_directory):
                    if file.endswith('.sql') or file.endswith('.sql.gz'):
                        file_path = os.path.join(self.backup_directory, file)
                        backup_files.append(file_path)
            
            if backup_files:
                backup_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                
                for file_path in backup_files:
                    file_name = os.path.basename(file_path)
                    source_db = file_name.split('_')[0] if '_' in file_name else "Unknown"
                    
                    mod_time = os.path.getmtime(file_path)
                    date_time = datetime.fromtimestamp(mod_time).strftime("%m/%d %H:%M")
                    
                    size_bytes = os.path.getsize(file_path)
                    if size_bytes >= 1024 * 1024:
                        size_str = f"{size_bytes / (1024 * 1024):.2f}MB"
                    elif size_bytes >= 1024:
                        size_str = f"{size_bytes / 1024:.2f}KB"
                    else:
                        size_str = f"{size_bytes}B"
                    
                    self._add_backup_database_row(file_name, source_db, date_time, size_str)
                
                print(f"[SUCCESS] Loaded {len(backup_files)} backup files")
                
        except Exception as e:
            print(f"[ERROR] Failed to load backup files: {e}")
            traceback.print_exc()

    def refresh_all(self):
        """Refresh all databases and backups"""
        print("[DEBUG] Refresh all triggered")
        
        # Show loading message
        from PySide6.QtWidgets import QApplication
        QApplication.setOverrideCursor(Qt.WaitCursor)
        
        try:
            # Reconnect to database if needed
            if not self.db_manager or not self.db_manager.connection.is_connected():
                print("[DEBUG] Reconnecting to MySQL")
                from core.database import DatabaseManager
                self.db_manager = DatabaseManager(
                    host="localhost",
                    port=3306,
                    user="root",
                    password=""
                )
                self.db_manager.connect()
            
            # Refresh databases
            print("[DEBUG] Refreshing primary databases")
            databases = self.db_manager.get_databases()
            
            if databases:
                self.primary_table.setRowCount(0)
                
                for db_name in databases:
                    db_info = self.db_manager.get_database_info(db_name)
                    if db_info:
                        self._add_primary_database_row(
                            db_info["name"],
                            db_info["type"],
                            db_info["size"],
                            str(db_info["tables"]),
                            db_info["status"]
                        )
                
                print(f"[SUCCESS] Refreshed {len(databases)} databases")
            
            # Refresh backups
            print("[DEBUG] Refreshing backup files")
            self.load_backup_files()
            
            # Show success message
            QMessageBox.information(
                self,
                "✓ Refresh Complete",
                f"Successfully refreshed:\n\n"
                f"• Primary Databases: {len(databases)}\n"
                f"• Backup Files: {self.backup_table.rowCount()}\n\n"
                "All data is now up to date."
            )
            
            print("[SUCCESS] Refresh completed")
            
        except Exception as e:
            print(f"[ERROR] Refresh failed: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(
                self,
                "Refresh Error",
                f"Failed to refresh data.\n\nError: {str(e)}\n\n"
                "Please check:\n"
                "• MySQL is running in XAMPP\n"
                "• Connection settings are correct"
            )
        
        finally:
            # Restore cursor
            QApplication.restoreOverrideCursor()

    
    def _create_page_header(self):
        """Create page header with refresh button"""
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)  # Changed to HBoxLayout
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(20)
        
        # Left side - titles
        titles_layout = QVBoxLayout()
        titles_layout.setSpacing(12)
        
        title = QLabel("Databases")
        title.setStyleSheet("""
            font-size: 36px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: -1.2px;
        """)
        
        subtitle = QLabel("Manage your database connections and configurations")
        subtitle.setStyleSheet("""
            color: #b8a5d8;
            font-size: 16px;
            font-weight: 500;
        """)
        
        titles_layout.addWidget(title)
        titles_layout.addWidget(subtitle)
        
        # Right side - refresh button
        btn_refresh = QPushButton("⟳ Refresh")
        btn_refresh.setObjectName("secondaryButton")
        btn_refresh.setMinimumHeight(44)
        btn_refresh.setMinimumWidth(120)
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.setToolTip("Refresh databases and backups from MySQL")
        btn_refresh.clicked.connect(self.refresh_all)
        btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #4A5578;
                border: 1px solid #5A6588;
                border-radius: 8px;
                color: #E0E7FF;
                font-size: 14px;
                font-weight: 600;
                padding: 0 16px;
            }
            QPushButton:hover {
                background-color: #0EA5E9;
                border-color: #0EA5E9;
                color: #FFFFFF;
            }
            QPushButton:pressed {
                background-color: #0284C7;
            }
        """)
        
        header_layout.addLayout(titles_layout)
        header_layout.addStretch()
        header_layout.addWidget(btn_refresh, 0, Qt.AlignTop)
        
        return header_frame

    
    def _create_primary_databases(self):
        """Create primary databases section"""
        primary_frame = QFrame()
        primary_frame.setObjectName("contentCard")
        primary_layout = QVBoxLayout(primary_frame)
        primary_layout.setContentsMargins(32, 28, 32, 28)
        primary_layout.setSpacing(24)
        
        header_layout = QHBoxLayout()
        
        section_title = QLabel("PRIMARY DATABASES")
        section_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: 0.5px;
        """)
        
        btn_new_db = QPushButton("+ New Database")
        btn_new_db.setObjectName("primaryButton")
        btn_new_db.setMinimumHeight(44)
        btn_new_db.setCursor(Qt.PointingHandCursor)
        btn_new_db.clicked.connect(self._handle_new_database)
        
        header_layout.addWidget(section_title)
        header_layout.addStretch()
        header_layout.addWidget(btn_new_db)
        
        primary_layout.addLayout(header_layout)
        
        self.primary_table = QTableWidget()
        self.primary_table.setColumnCount(6)
        self.primary_table.setRowCount(0)
        self.primary_table.setHorizontalHeaderLabels([
            "DATABASE NAME", "TYPE", "SIZE", "TABLES", "STATUS", "ACTIONS"
        ])
        
        self.primary_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.primary_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.primary_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.primary_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.primary_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.primary_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.primary_table.horizontalHeader().resizeSection(5, 160)
        
        self.primary_table.verticalHeader().setVisible(False)
        self.primary_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.primary_table.setSelectionMode(QTableWidget.SingleSelection)
        self.primary_table.setShowGrid(False)
        self.primary_table.setMinimumHeight(280)
        
        primary_layout.addWidget(self.primary_table)
        
        return primary_frame
    
    def _add_primary_database_row(self, db_name: str, db_type: str, size: str, tables: str, status: str):
        """Add database row with action buttons"""
        row = self.primary_table.rowCount()
        self.primary_table.insertRow(row)
        
        # Database name
        name_item = QTableWidgetItem(db_name)
        name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
        self.primary_table.setItem(row, 0, name_item)
        
        # Type
        type_item = QTableWidgetItem(db_type)
        type_item.setFlags(type_item.flags() & ~Qt.ItemIsEditable)
        self.primary_table.setItem(row, 1, type_item)
        
        # Size
        size_item = QTableWidgetItem(size)
        size_item.setFlags(size_item.flags() & ~Qt.ItemIsEditable)
        self.primary_table.setItem(row, 2, size_item)
        
        # Tables
        tables_item = QTableWidgetItem(tables)
        tables_item.setFlags(tables_item.flags() & ~Qt.ItemIsEditable)
        self.primary_table.setItem(row, 3, tables_item)
        
        # Status
        status_item = QTableWidgetItem(f"● {status}")
        status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
        status_item.setForeground(Qt.GlobalColor.green)
        self.primary_table.setItem(row, 4, status_item)
        
        # Actions
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(8, 6, 8, 6)
        actions_layout.setSpacing(8)
        
        btn_backup = ActionButton("↓", "Backup Database")
        btn_backup.clicked.connect(lambda checked=False, name=db_name: self._handle_backup(name))
        
        btn_drop = ActionButton("×", "Drop Database", "destructive")
        btn_drop.clicked.connect(lambda checked=False, name=db_name: self._handle_drop(name))
        
        btn_view = ActionButton("☰", "View Tables & More")
        btn_view.clicked.connect(lambda checked=False, name=db_name: self._handle_view_tables(name))
        
        actions_layout.addWidget(btn_backup)
        actions_layout.addWidget(btn_drop)
        actions_layout.addWidget(btn_view)
        
        self.primary_table.setCellWidget(row, 5, actions_widget)
        self.primary_table.setRowHeight(row, 75)
    
    def _create_backup_databases(self):
        """Create backup databases section"""
        backup_frame = QFrame()
        backup_frame.setObjectName("contentCard")
        backup_layout = QVBoxLayout(backup_frame)
        backup_layout.setContentsMargins(32, 28, 32, 28)
        backup_layout.setSpacing(24)
        
        section_title = QLabel("BACKUP DATABASES")
        section_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: 0.5px;
        """)
        
        backup_layout.addWidget(section_title)
        
        self.backup_table = QTableWidget()
        self.backup_table.setColumnCount(5)
        self.backup_table.setRowCount(0)
        self.backup_table.setHorizontalHeaderLabels([
            "BACKUP NAME", "SOURCE", "DATE/TIME", "SIZE", "ACTIONS"
        ])
        
        self.backup_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.backup_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.backup_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.backup_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.backup_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.backup_table.horizontalHeader().resizeSection(4, 160)
        
        self.backup_table.verticalHeader().setVisible(False)
        self.backup_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.backup_table.setSelectionMode(QTableWidget.SingleSelection)
        self.backup_table.setShowGrid(False)
        self.backup_table.setMinimumHeight(220)
        
        backup_layout.addWidget(self.backup_table)
        
        return backup_frame
    
    def _add_backup_database_row(self, backup_name: str, source: str, datetime: str, size: str):
        """Add backup row with action buttons"""
        row = self.backup_table.rowCount()
        self.backup_table.insertRow(row)
        
        name_item = QTableWidgetItem(backup_name)
        name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
        self.backup_table.setItem(row, 0, name_item)
        
        source_item = QTableWidgetItem(source)
        source_item.setFlags(source_item.flags() & ~Qt.ItemIsEditable)
        self.backup_table.setItem(row, 1, source_item)
        
        datetime_item = QTableWidgetItem(datetime)
        datetime_item.setFlags(datetime_item.flags() & ~Qt.ItemIsEditable)
        self.backup_table.setItem(row, 2, datetime_item)
        
        size_item = QTableWidgetItem(size)
        size_item.setFlags(size_item.flags() & ~Qt.ItemIsEditable)
        self.backup_table.setItem(row, 3, size_item)
        
        # Actions
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(8, 6, 8, 6)
        actions_layout.setSpacing(8)
        
        btn_restore = ActionButton("↶", "Restore Database")
        btn_restore.clicked.connect(lambda checked=False, name=backup_name: self._handle_restore(name))
        
        btn_delete = ActionButton("×", "Delete Backup", "destructive")
        btn_delete.clicked.connect(lambda checked=False, name=backup_name: self._handle_delete_backup(name))
        
        btn_details = ActionButton("i", "View Details")
        btn_details.clicked.connect(lambda checked=False, name=backup_name: self._handle_details(name))
        
        actions_layout.addWidget(btn_restore)
        actions_layout.addWidget(btn_delete)
        actions_layout.addWidget(btn_details)
        
        self.backup_table.setCellWidget(row, 4, actions_widget)
        self.backup_table.setRowHeight(row, 75)
    
    # ========================================================================
    # EVENT HANDLERS - Database Operations
    # ========================================================================
    
    def _handle_new_database(self):
        """Create new database"""
        print("[DEBUG] New database dialog opened")

        # Check permission
        if self.permission_checker and not self.permission_checker.can_create_database():
            QMessageBox.warning(
                self,
                "🔒 Permission Denied",
                f"You do not have permission to create databases.\n\n"
                f"Only administrators can create new databases.\n"
                f"Please contact your administrator for access."
            )
            print(f"[PERMISSIONS] ✗ {self.user_data.get('username')} denied CREATE DATABASE")
            return

        dialog = NewDatabaseDialog(self)
        if dialog.exec() == QDialog.Accepted:
            db_name = dialog.get_database_name()
            if not db_name:
                QMessageBox.warning(self, "Invalid Input", "Please enter a database name.")
                return
            try:
                if not self.db_manager or not self.db_manager.connection.is_connected():
                    self.db_manager = DatabaseManager()
                    self.db_manager.connect()
                cursor = self.db_manager.connection.cursor()
                cursor.execute(f"CREATE DATABASE `{db_name}`")
                cursor.close()
                print(f"[SUCCESS] Database {db_name} created")
                QMessageBox.information(
                    self,
                    "Success",
                    f"Database '{db_name}' has been created successfully!"
                )
                self.load_real_databases()
            except Exception as e:
                print(f"[ERROR] Failed to create database: {e}")
                traceback.print_exc()
                QMessageBox.critical(
                    self,
                    "Error Creating Database",
                    f"Failed to create database '{db_name}'.\n\nError: {str(e)}"
                )
    
    def _handle_backup(self, db_name: str):
        """Backup database using mysqldump"""
        print(f"[DEBUG] Backup requested for database: {db_name}")
        self.backup_requested.emit(db_name)
        
        try:
            if not os.path.exists(self.backup_directory):
                os.makedirs(self.backup_directory)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{db_name}_backup_{timestamp}.sql"
            backup_path = os.path.join(self.backup_directory, backup_filename)
            
            mysqldump_path = r"C:\xampp\mysql\bin\mysqldump.exe"
            
            if not os.path.exists(mysqldump_path):
                print(f"[ERROR] mysqldump not found at: {mysqldump_path}")
                QMessageBox.warning(
                    self,
                    "mysqldump Not Found",
                    f"mysqldump not found at: {mysqldump_path}\n\nPlease check your XAMPP installation."
                )
                return
            
            command = [
                mysqldump_path,
                "-u", "root",
                "-h", "localhost",
                db_name
            ]
            
            print(f"[DEBUG] Running: {' '.join(command)}")
            
            with open(backup_path, 'w') as backup_file:
                result = subprocess.run(
                    command,
                    stdout=backup_file,
                    stderr=subprocess.PIPE,
                    text=True
                )
            
            if result.returncode == 0:
                print(f"[SUCCESS] Backup created: {backup_filename}")
                QMessageBox.information(
                    self,
                    "Backup Successful",
                    f"Database '{db_name}' has been backed up successfully!\n\n"
                    f"Backup file: {backup_filename}"
                )
                
                self.load_backup_files()
            else:
                print(f"[ERROR] mysqldump failed: {result.stderr}")
                QMessageBox.critical(
                    self,
                    "Backup Failed",
                    f"Failed to backup database.\n\nError: {result.stderr}"
                )
                
        except Exception as e:
            print(f"[ERROR] Backup exception: {e}")
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Backup Error",
                f"An error occurred during backup.\n\nError: {str(e)}"
            )
    
    def _handle_drop(self, db_name: str):
        """Drop database with confirmation"""
        print(f"[DEBUG] Drop requested for database: {db_name}")

        # Check permission
        if self.permission_checker and not self.permission_checker.can_drop_database(db_name):
            QMessageBox.warning(
                self,
                "🔒 Permission Denied",
                f"You do not have permission to drop database '{db_name}'.\n\n"
                f"Required permission: DELETE on '{db_name}'\n"
                f"Please contact your administrator for access."
            )
            print(f"[PERMISSIONS] ✗ {self.user_data.get('username')} denied DROP DATABASE {db_name}")
            return

        dialog = ConfirmationDialog(
            self,
            "⚠️ Confirm Database Drop",
            f"Are you sure you want to drop database '{db_name}'?",
            "This will permanently delete the database and all its data.\nThis action cannot be undone."
        )
        reply = dialog.exec()
        if reply == QMessageBox.Yes:
            try:
                if not self.db_manager or not self.db_manager.connection.is_connected():
                    self.db_manager = DatabaseManager()
                    self.db_manager.connect()
                cursor = self.db_manager.connection.cursor()
                cursor.execute(f"DROP DATABASE `{db_name}`")
                cursor.close()
                self.drop_requested.emit(db_name)
                print(f"[SUCCESS] Database {db_name} dropped")
                QMessageBox.information(
                    self,
                    "Database Dropped",
                    f"Database '{db_name}' has been successfully dropped."
                )
                self.load_real_databases()
            except Exception as e:
                print(f"[ERROR] Failed to drop database: {e}")
                traceback.print_exc()
                QMessageBox.critical(
                    self,
                    "Error Dropping Database",
                    f"Failed to drop database '{db_name}'.\n\nError: {str(e)}"
                )

    
    def _handle_view_tables(self, db_name: str):
        """View and manage tables in database"""
        print(f"[DEBUG] View tables requested for database: {db_name}")
        self.view_tables_requested.emit(db_name)
        
        try:
            if not self.db_manager or not self.db_manager.connection.is_connected():
                self.db_manager = DatabaseManager()
                self.db_manager.connect()
            
            cursor = self.db_manager.connection.cursor()
            cursor.execute(f"USE `{db_name}`")
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            cursor.close()
            
            print(f"[DEBUG] Found {len(tables)} tables in {db_name}")
            
            # Show enhanced tables dialog
            dialog = ViewTablesDialog(db_name, tables, self.db_manager, self)
            dialog.exec()
                
        except Exception as e:
            print(f"[ERROR] Failed to load tables: {e}")
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Error Loading Tables",
                f"Failed to load tables from '{db_name}'.\n\nError: {str(e)}"
            )
    
    def _handle_restore(self, backup_name: str):
        """Restore database from backup file"""
        print(f"[DEBUG] Restore requested for: {backup_name}")
        dialog = ConfirmationDialog(
            self,
            "⚠️ Confirm Restore",
            f"Are you sure you want to restore '{backup_name}'?",
            "This will create a new database or overwrite an existing one.\nChoose carefully to avoid data loss."
        )
        
        reply = dialog.exec()
        
        if reply == QMessageBox.Yes:
            try:
                backup_path = os.path.join(self.backup_directory, backup_name)
                
                if not os.path.exists(backup_path):
                    QMessageBox.warning(self, "File Not Found", f"Backup file '{backup_name}' not found.")
                    return
                
                restore_db_name = backup_name.split('_')[0]
                
                mysql_path = r"C:\xampp\mysql\bin\mysql.exe"
                
                if not os.path.exists(mysql_path):
                    print(f"[ERROR] mysql not found at: {mysql_path}")
                    QMessageBox.warning(
                        self,
                        "mysql Not Found",
                        f"mysql not found at: {mysql_path}\n\nPlease check your XAMPP installation."
                    )
                    return
                
                if not self.db_manager or not self.db_manager.connection.is_connected():
                    self.db_manager = DatabaseManager()
                    self.db_manager.connect()
                
                cursor = self.db_manager.connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{restore_db_name}`")
                cursor.close()
                
                command = [
                    mysql_path,
                    "-u", "root",
                    "-h", "localhost",
                    restore_db_name
                ]
                
                print(f"[DEBUG] Running: {' '.join(command)}")
                
                with open(backup_path, 'r') as backup_file:
                    result = subprocess.run(
                        command,
                        stdin=backup_file,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                
                if result.returncode == 0:
                    self.restore_requested.emit(backup_name)
                    print(f"[SUCCESS] Database restored from {backup_name}")
                    QMessageBox.information(
                        self,
                        "Restore Successful",
                        f"Database '{restore_db_name}' has been restored successfully from '{backup_name}'!"
                    )
                    
                    self.load_real_databases()
                else:
                    print(f"[ERROR] mysql restore failed: {result.stderr}")
                    QMessageBox.critical(
                        self,
                        "Restore Failed",
                        f"Failed to restore database.\n\nError: {result.stderr}"
                    )
                    
            except Exception as e:
                print(f"[ERROR] Restore exception: {e}")
                traceback.print_exc()
                QMessageBox.critical(
                    self,
                    "Restore Error",
                    f"An error occurred during restore.\n\nError: {str(e)}"
                )
    
    def _handle_delete_backup(self, backup_name: str):
        """Delete backup file"""
        print(f"[DEBUG] Delete backup requested: {backup_name}")
        dialog = ConfirmationDialog(
            self,
            "⚠️ Confirm Backup Deletion",
            f"Are you sure you want to delete backup '{backup_name}'?",
            "This will permanently delete the backup file.\nThis action cannot be undone."
        )
        
        reply = dialog.exec()
        
        if reply == QMessageBox.Yes:
            try:
                file_path = os.path.join(self.backup_directory, backup_name)
                
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.delete_backup_requested.emit(backup_name)
                    
                    print(f"[SUCCESS] Backup deleted: {backup_name}")
                    QMessageBox.information(
                        self,
                        "Backup Deleted",
                        f"Backup '{backup_name}' has been successfully deleted."
                    )
                    
                    self.load_backup_files()
                else:
                    QMessageBox.warning(self, "File Not Found", f"Backup file '{backup_name}' not found.")
                    
            except Exception as e:
                print(f"[ERROR] Failed to delete backup: {e}")
                traceback.print_exc()
                QMessageBox.critical(
                    self,
                    "Delete Error",
                    f"Failed to delete backup.\n\nError: {str(e)}"
                )
    
    def _handle_details(self, backup_name: str):
        """Show backup file details"""
        print(f"[DEBUG] Details requested for: {backup_name}")
        self.view_details_requested.emit(backup_name)
        
        file_path = os.path.join(self.backup_directory, backup_name)
        
        if os.path.exists(file_path):
            size_bytes = os.path.getsize(file_path)
            mod_time = os.path.getmtime(file_path)
            date_time = datetime.fromtimestamp(mod_time).strftime("%m/%d/%Y %H:%M:%S")
            
            if size_bytes >= 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
            elif size_bytes >= 1024:
                size_str = f"{size_bytes / 1024:.2f} KB"
            else:
                size_str = f"{size_bytes} B"
            
            source_db = backup_name.split('_')[0] if '_' in backup_name else "Unknown"
            
            details_dialog = QMessageBox(self)
            details_dialog.setWindowTitle("Backup Details")
            details_dialog.setText(f"Details for backup: {backup_name}")
            details_dialog.setInformativeText(
                f"Source Database: {source_db}\n"
                f"Backup Date: {date_time}\n"
                f"File Size: {size_str}\n"
                f"File Format: {'Compressed (.gz)' if backup_name.endswith('.gz') else 'SQL (.sql)'}\n"
                f"Status: Complete\n"
                f"File Path: {file_path}"
            )
            details_dialog.setIcon(QMessageBox.Information)
            details_dialog.exec()
        else:
            QMessageBox.warning(self, "File Not Found", f"Backup file '{backup_name}' not found.")
