"""
Backups management page with modern card-based design - Auto-Refresh Enabled
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QLineEdit, QComboBox, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QCursor
import os
from datetime import datetime


class ActionButton(QPushButton):
    """Custom action button with icon and enhanced hover effects"""
    
    def __init__(self, icon: str, tooltip: str, button_type: str = "normal", parent=None):
        super().__init__(icon, parent)
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(36, 36)
        self.button_type = button_type
        
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


class BackupsPage(QWidget):
    """Backups page with automatic refresh and real-time updates"""
    
    # Signals for actions
    restore_requested = Signal(str)
    delete_requested = Signal(str)
    view_details_requested = Signal(str)
    backup_created = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backup_directory = "backups"
        self.last_backup_count = 0
        self.auto_refresh_enabled = True
        self._init_ui()
        self.load_real_backups()
        self._setup_auto_refresh()
        print("[DEBUG] BackupsPage initialized with auto-refresh")
    
    def _setup_auto_refresh(self):
        """Setup automatic refresh timer"""
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self._check_for_changes)
        self.refresh_timer.start(5000)
        print("[DEBUG] Auto-refresh timer started (5 seconds)")
    
    def _check_for_changes(self):
        """Check if backup directory has changed"""
        if not self.auto_refresh_enabled:
            return
        
        try:
            if not os.path.exists(self.backup_directory):
                return
            
            current_count = 0
            for file in os.listdir(self.backup_directory):
                if file.endswith('.sql') or file.endswith('.sql.gz'):
                    current_count += 1
            
            if current_count != self.last_backup_count:
                print(f"[DEBUG] Backup count changed: {self.last_backup_count} -> {current_count}")
                self.load_real_backups(silent=True)
                self.last_backup_count = current_count
                
        except Exception as e:
            print(f"[ERROR] Auto-refresh check failed: {e}")
    
    def _init_ui(self):
        """Initialize backups page UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(40)
        
        header_frame = self._create_page_header()
        layout.addWidget(header_frame)
        
        controls_frame = self._create_controls()
        layout.addWidget(controls_frame)
        
        backups_frame = self._create_backups_table()
        layout.addWidget(backups_frame)
        
        layout.addStretch()
    
    def _create_page_header(self):
        """Create simplified page header with auto-refresh"""
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(20)
        
        # Left side - titles
        titles_layout = QVBoxLayout()
        titles_layout.setSpacing(12)
        
        title = QLabel("Backups")
        title.setStyleSheet("""
            font-size: 36px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: -1.2px;
        """)
        
        subtitle = QLabel("Manage your database backups and restore operations")
        subtitle.setStyleSheet("""
            color: #b8a5d8;
            font-size: 16px;
            font-weight: 500;
        """)
        
        titles_layout.addWidget(title)
        titles_layout.addWidget(subtitle)
        
        # Right side - auto-refresh toggle
        refresh_layout = QHBoxLayout()
        refresh_layout.setSpacing(8)
        
        auto_refresh_label = QLabel("Auto-refresh:")
        auto_refresh_label.setStyleSheet("""
            color: #b8a5d8; 
            font-size: 14px;
            font-weight: 500;
        """)
        
        self.auto_refresh_checkbox = QCheckBox()
        self.auto_refresh_checkbox.setChecked(True)
        self.auto_refresh_checkbox.toggled.connect(self.toggle_auto_refresh)
        self.auto_refresh_checkbox.setStyleSheet("""
            QCheckBox {
                color: #E0E7FF;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #5A6588;
                border-radius: 4px;
                background-color: #2A2F4A;
            }
            QCheckBox::indicator:checked {
                background-color: #0EA5E9;
                border-color: #0EA5E9;
            }
        """)
        
        refresh_layout.addWidget(auto_refresh_label)
        refresh_layout.addWidget(self.auto_refresh_checkbox)
        
        header_layout.addLayout(titles_layout)
        header_layout.addStretch()
        header_layout.addLayout(refresh_layout)
        
        return header_frame
    
    def load_real_backups(self, silent=False):
        """Load real backup files"""
        print(f"[DEBUG] Loading backups (silent={silent})")
        try:
            if not os.path.exists(self.backup_directory):
                os.makedirs(self.backup_directory)
            
            self.backups_table.setRowCount(0)
            
            backup_files = []
            if os.path.exists(self.backup_directory):
                for file in os.listdir(self.backup_directory):
                    if file.endswith('.sql') or file.endswith('.sql.gz'):
                        file_path = os.path.join(self.backup_directory, file)
                        backup_files.append(file_path)
            
            self.last_backup_count = len(backup_files)
            
            if backup_files:
                backup_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                
                for file_path in backup_files:
                    file_name = os.path.basename(file_path)
                    source_db = file_name.split('_')[0] if '_' in file_name else "Unknown"
                    
                    mod_time = os.path.getmtime(file_path)
                    date_time = datetime.fromtimestamp(mod_time).strftime("%m/%d %H:%M")
                    
                    size_bytes = os.path.getsize(file_path)
                    if size_bytes >= 1024 * 1024:
                        size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
                    elif size_bytes >= 1024:
                        size_str = f"{size_bytes / 1024:.2f} KB"
                    else:
                        size_str = f"{size_bytes} B"
                    
                    self._add_backup_row(file_name, source_db, date_time, size_str)
                
                if not silent:
                    print(f"[SUCCESS] Loaded {len(backup_files)} backup files")
            else:
                if not silent:
                    print("[INFO] No backup files found")
                row = self.backups_table.rowCount()
                self.backups_table.insertRow(row)
                no_data_item = QTableWidgetItem("No backups found. Create your first backup from Databases page.")
                no_data_item.setFlags(no_data_item.flags() & ~Qt.ItemIsEditable)
                no_data_item.setForeground(Qt.GlobalColor.gray)
                self.backups_table.setItem(row, 0, no_data_item)
                self.backups_table.setSpan(row, 0, 1, 6)
            
            self._update_status_label(len(backup_files))
                
        except Exception as e:
            print(f"[ERROR] Failed to load backups: {e}")
            if not silent:
                QMessageBox.warning(self, "Error", f"Could not load backup files.\n\nError: {str(e)}")
    
    def _update_status_label(self, count):
        """Update status label"""
        if hasattr(self, 'status_label'):
            if count > 0:
                self.status_label.setText(f"Showing {count} backup file{'s' if count != 1 else ''}")
                self.status_label.setStyleSheet("color: #6ee7b7; font-size: 13px; font-weight: 600;")
            else:
                self.status_label.setText("No backups available")
                self.status_label.setStyleSheet("color: #fca5a5; font-size: 13px; font-weight: 600;")
    
    def toggle_auto_refresh(self, enabled):
        """Toggle auto-refresh"""
        self.auto_refresh_enabled = enabled
        if enabled:
            self.refresh_timer.start(5000)
            print("[DEBUG] Auto-refresh enabled")
        else:
            self.refresh_timer.stop()
            print("[DEBUG] Auto-refresh disabled")
    
    def _create_controls(self):
        """Create search and filter controls"""
        controls_frame = QFrame()
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(16)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("⌕ Search backups...")
        self.search_input.setMinimumHeight(44)
        self.search_input.textChanged.connect(self._filter_backups)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #2A2F4A;
                border: 1px solid #3A4560;
                border-radius: 8px;
                padding: 0 16px;
                color: #E0E7FF;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #0EA5E9;
                background-color: #323852;
            }
            QLineEdit::placeholder {
                color: #7C8BA8;
            }
        """)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Sort by Date ▼", "Sort by Size", "Sort by Name"])
        self.sort_combo.setMinimumHeight(44)
        self.sort_combo.setMinimumWidth(180)
        self.sort_combo.setCursor(Qt.PointingHandCursor)
        self.sort_combo.setStyleSheet("""
            QComboBox {
                background-color: #2A2F4A;
                border: 1px solid #3A4560;
                border-radius: 8px;
                padding: 0 16px;
                color: #E0E7FF;
                font-size: 14px;
                font-weight: 500;
            }
            QComboBox:hover {
                border: 1px solid #0EA5E9;
                background-color: #323852;
            }
            QComboBox QAbstractItemView {
                background-color: #2A2F4A;
                border: 1px solid #3A4560;
                selection-background-color: #0EA5E9;
                selection-color: #FFFFFF;
                color: #E0E7FF;
            }
        """)
        
        controls_layout.addWidget(self.search_input, stretch=3)
        controls_layout.addWidget(self.sort_combo, stretch=1)
        
        return controls_frame
    
    def _filter_backups(self, text):
        """Filter backups"""
        for row in range(self.backups_table.rowCount()):
            item = self.backups_table.item(row, 0)
            if item:
                should_show = text.lower() in item.text().lower()
                self.backups_table.setRowHidden(row, not should_show)
    
    def _create_backups_table(self):
        """Create backups table"""
        backups_frame = QFrame()
        backups_frame.setObjectName("contentCard")
        backups_layout = QVBoxLayout(backups_frame)
        backups_layout.setContentsMargins(32, 28, 32, 28)
        backups_layout.setSpacing(24)
        
        header_layout = QHBoxLayout()
        
        section_title = QLabel("BACKUP FILES")
        section_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: 0.5px;
        """)
        
        self.status_label = QLabel("Loading...")
        self.status_label.setStyleSheet("color: #b8a5d8; font-size: 13px;")
        
        header_layout.addWidget(section_title)
        header_layout.addStretch()
        header_layout.addWidget(self.status_label)
        
        backups_layout.addLayout(header_layout)
        
        self.backups_table = QTableWidget()
        self.backups_table.setColumnCount(6)
        self.backups_table.setRowCount(0)
        self.backups_table.setHorizontalHeaderLabels([
            "BACKUP NAME", "SOURCE DATABASE", "DATE/TIME", "FILE SIZE", "STATUS", "ACTIONS"
        ])
        
        self.backups_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.backups_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.backups_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.backups_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.backups_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.backups_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.backups_table.horizontalHeader().resizeSection(5, 160)
        
        self.backups_table.verticalHeader().setVisible(False)
        self.backups_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.backups_table.setSelectionMode(QTableWidget.SingleSelection)
        self.backups_table.setShowGrid(False)
        self.backups_table.setMinimumHeight(400)
        
        backups_layout.addWidget(self.backups_table)
        
        return backups_frame
    
    def _add_backup_row(self, backup_name: str, source: str, datetime: str, size: str):
        """Add backup row"""
        row = self.backups_table.rowCount()
        self.backups_table.insertRow(row)
        
        name_item = QTableWidgetItem(backup_name)
        name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
        self.backups_table.setItem(row, 0, name_item)
        
        source_item = QTableWidgetItem(source)
        source_item.setFlags(source_item.flags() & ~Qt.ItemIsEditable)
        self.backups_table.setItem(row, 1, source_item)
        
        datetime_item = QTableWidgetItem(datetime)
        datetime_item.setFlags(datetime_item.flags() & ~Qt.ItemIsEditable)
        self.backups_table.setItem(row, 2, datetime_item)
        
        size_item = QTableWidgetItem(size)
        size_item.setFlags(size_item.flags() & ~Qt.ItemIsEditable)
        self.backups_table.setItem(row, 3, size_item)
        
        status_item = QTableWidgetItem(f"● Complete")
        status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
        status_item.setForeground(Qt.GlobalColor.green)
        self.backups_table.setItem(row, 4, status_item)
        
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(8, 6, 8, 6)
        actions_layout.setSpacing(8)
        
        btn_restore = ActionButton("↻", "Restore Database")
        btn_restore.clicked.connect(lambda checked=False, name=backup_name: self._handle_restore(name))
        
        btn_delete = ActionButton("⌧", "Delete Backup", "destructive")
        btn_delete.clicked.connect(lambda checked=False, name=backup_name: self._handle_delete(name))
        
        btn_details = ActionButton("i", "View Details")
        btn_details.clicked.connect(lambda checked=False, name=backup_name: self._handle_details(name))
        
        actions_layout.addWidget(btn_restore)
        actions_layout.addWidget(btn_delete)
        actions_layout.addWidget(btn_details)
        
        self.backups_table.setCellWidget(row, 5, actions_widget)
        self.backups_table.setRowHeight(row, 75)
    
    def _handle_restore(self, backup_name: str):
        """Handle restore"""
        dialog = ConfirmationDialog(
            self,
            "⚠️ Confirm Restore",
            f"Are you sure you want to restore '{backup_name}'?",
            "This will create a new database or overwrite an existing one."
        )
        
        if dialog.exec() == QMessageBox.Yes:
            self.restore_requested.emit(backup_name)
            QMessageBox.information(self, "Restore Started", f"Restoring from: {backup_name}")
            QTimer.singleShot(2000, self.load_real_backups)
    
    def _handle_delete(self, backup_name: str):
        """Handle delete"""
        dialog = ConfirmationDialog(
            self,
            "⚠️ Confirm Deletion",
            f"Are you sure you want to delete '{backup_name}'?",
            "This action cannot be undone."
        )
        
        if dialog.exec() == QMessageBox.Yes:
            try:
                file_path = os.path.join(self.backup_directory, backup_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.delete_requested.emit(backup_name)
                    QMessageBox.information(self, "Deleted", f"Backup '{backup_name}' deleted.")
                    self.load_real_backups()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete.\n\nError: {str(e)}")
    
    def _handle_details(self, backup_name: str):
        """Handle details"""
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
            
            QMessageBox.information(
                self,
                "Backup Details",
                f"Backup: {backup_name}\n\n"
                f"Source: {source_db}\n"
                f"Date: {date_time}\n"
                f"Size: {size_str}\n"
                f"Path: {file_path}"
            )
        else:
            QMessageBox.warning(self, "Not Found", f"Backup file '{backup_name}' not found.")
    
    def closeEvent(self, event):
        """Stop timer on close"""
        if hasattr(self, 'refresh_timer'):
            self.refresh_timer.stop()
        event.accept()
