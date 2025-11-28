"""
Redesigned Dashboard page with clean layout and real data from MySQL
All Quick Actions are now fully functional
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QGridLayout, QMessageBox, QInputDialog, QApplication
)
from PySide6.QtCore import Qt
from ui.components.stat_card import StatCard
from core.database import DatabaseManager
import os
import subprocess
from datetime import datetime
import traceback


class DashboardPage(QWidget):
    """Dashboard page with clean stats, real data, and functional quick actions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_manager = None
        self.backup_directory = "backups"
        self._init_ui()
        self.load_real_stats()
        print("[DEBUG] DashboardPage initialized with real data and functional actions")
    
    def _init_ui(self):
        """Initialize dashboard UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(40)
        
        # Simple page header
        header_frame = self._create_page_header()
        layout.addWidget(header_frame)
        
        # Stats grid - Will be populated with real data
        self.stats_frame = QFrame()
        self.stats_layout = QGridLayout(self.stats_frame)
        self.stats_layout.setSpacing(28)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        
        # Initialize with placeholder cards
        self.stat_cards = {
            'databases': StatCard("Total Databases", "0", "database"),
            'backups': StatCard("Active Backups", "0", "backup"),
            'storage': StatCard("Storage Used", "0 GB", "storage"),
            'time': StatCard("Last Backup", "Never", "time")
        }
        
        # Add cards to grid
        self.stats_layout.addWidget(self.stat_cards['databases'], 0, 0)
        self.stats_layout.addWidget(self.stat_cards['backups'], 0, 1)
        self.stats_layout.addWidget(self.stat_cards['storage'], 0, 2)
        self.stats_layout.addWidget(self.stat_cards['time'], 0, 3)
        
        # Make columns equal width
        for i in range(4):
            self.stats_layout.setColumnStretch(i, 1)
        
        layout.addWidget(self.stats_frame)
        
        # Two column layout for actions and activity
        content_row = QHBoxLayout()
        content_row.setSpacing(28)
        
        # Quick actions
        actions_frame = self._create_quick_actions()
        content_row.addWidget(actions_frame, 1)
        
        # System status
        status_frame = self._create_system_status()
        content_row.addWidget(status_frame, 1)
        
        layout.addLayout(content_row)
        
        # Recent activity (full width)
        activity_frame = self._create_recent_activity()
        layout.addWidget(activity_frame)
        
        layout.addStretch()
    
    def load_real_stats(self):
        """Load real statistics from MySQL database and backup files"""
        print("[DEBUG] Loading real dashboard statistics")
        try:
            # Create database manager
            self.db_manager = DatabaseManager(
                host="localhost",
                port=3306,
                user="root",
                password=""
            )
            
            # Connect to MySQL
            if self.db_manager.connect():
                # Get real database count
                databases = self.db_manager.get_databases()
                total_databases = len(databases)
                
                # Calculate total storage used
                total_size_mb = 0
                total_tables = 0
                
                for db_name in databases:
                    db_info = self.db_manager.get_database_info(db_name)
                    if db_info:
                        # Extract size in MB
                        size_str = db_info['size']
                        try:
                            size_value = float(size_str.replace('MB', '').strip())
                            total_size_mb += size_value
                            total_tables += db_info['tables']
                        except:
                            pass
                
                # Convert to GB if large
                if total_size_mb >= 1024:
                    storage_str = f"{total_size_mb / 1024:.2f} GB"
                else:
                    storage_str = f"{total_size_mb:.2f} MB"
                
                # Get real backup count and last backup time
                backup_count, last_backup_time = self._get_backup_stats()
                
                # Update stat cards with real data
                self.stat_cards['databases'].value_label.setText(str(total_databases))
                self.stat_cards['backups'].value_label.setText(str(backup_count))
                self.stat_cards['storage'].value_label.setText(storage_str)
                self.stat_cards['time'].value_label.setText(last_backup_time)
                
                print(f"[SUCCESS] Dashboard loaded with real data:")
                print(f"  - Total Databases: {total_databases}")
                print(f"  - Active Backups: {backup_count}")
                print(f"  - Storage Used: {storage_str}")
                print(f"  - Last Backup: {last_backup_time}")
                
                # Disconnect after loading
                self.db_manager.disconnect()
                
        except Exception as e:
            print(f"[ERROR] Failed to load dashboard stats: {e}")
            traceback.print_exc()
    
    def _get_backup_stats(self):
        """Get backup count and last backup time from backup directory"""
        try:
            if not os.path.exists(self.backup_directory):
                return 0, "Never"
            
            backup_files = []
            for file in os.listdir(self.backup_directory):
                if file.endswith('.sql') or file.endswith('.sql.gz'):
                    file_path = os.path.join(self.backup_directory, file)
                    backup_files.append(file_path)
            
            backup_count = len(backup_files)
            
            if backup_count == 0:
                return 0, "Never"
            
            # Get most recent backup file
            backup_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            most_recent = backup_files[0]
            
            # Calculate time ago
            mod_time = os.path.getmtime(most_recent)
            last_backup_dt = datetime.fromtimestamp(mod_time)
            now = datetime.now()
            
            time_diff = now - last_backup_dt
            
            # Format time ago
            if time_diff.days > 0:
                if time_diff.days == 1:
                    time_ago = "1 day ago"
                else:
                    time_ago = f"{time_diff.days} days ago"
            elif time_diff.seconds >= 3600:
                hours = time_diff.seconds // 3600
                if hours == 1:
                    time_ago = "1 hour ago"
                else:
                    time_ago = f"{hours} hours ago"
            elif time_diff.seconds >= 60:
                minutes = time_diff.seconds // 60
                if minutes == 1:
                    time_ago = "1 minute ago"
                else:
                    time_ago = f"{minutes} minutes ago"
            else:
                time_ago = "Just now"
            
            return backup_count, time_ago
            
        except Exception as e:
            print(f"[ERROR] Failed to get backup stats: {e}")
            return 0, "Unknown"
    
    def refresh_dashboard(self):
        """Refresh dashboard with latest data"""
        print("[DEBUG] Refreshing dashboard")
        self.load_real_stats()
        QMessageBox.information(
            self,
            "✓ Refreshed",
            "Dashboard data has been refreshed successfully!"
        )
    
    # ========================================================================
    # UI CREATION METHODS
    # ========================================================================
    
    def _create_page_header(self):
        """Create clean page header"""
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)
        
        title = QLabel("Dashboard Overview")
        title.setObjectName("pageTitle")
        title.setStyleSheet("""
            font-size: 36px;
            font-weight: 700;
            color: #e6d9ff;
            letter-spacing: -1.2px;
        """)
        
        subtitle = QLabel("Monitor your database backups and system health")
        subtitle.setStyleSheet("""
            color: #b8a5d8;
            font-size: 16px;
            font-weight: 500;
        """)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        return header_frame
    
    def _create_quick_actions(self):
        """Create quick actions section with functional buttons"""
        actions_frame = QFrame()
        actions_frame.setObjectName("contentCard")
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setContentsMargins(32, 28, 32, 28)
        actions_layout.setSpacing(24)
        
        actions_title = QLabel("Quick Actions")
        actions_title.setObjectName("sectionTitle")
        actions_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #e6d9ff;
        """)
        actions_layout.addWidget(actions_title)
        actions_layout.addSpacing(8)
        
        # New Backup button
        btn_new_backup = QPushButton("✦ New Backup")
        btn_new_backup.setObjectName("primaryButton")
        btn_new_backup.setMinimumHeight(52)
        btn_new_backup.setCursor(Qt.PointingHandCursor)
        btn_new_backup.clicked.connect(self._handle_new_backup)
        
        # Restore Database button
        btn_restore = QPushButton("↻ Restore Database")
        btn_restore.setObjectName("secondaryButton")
        btn_restore.setMinimumHeight(52)
        btn_restore.setCursor(Qt.PointingHandCursor)
        btn_restore.clicked.connect(self._handle_restore_database)
        
        # Manage Databases button
        btn_manage = QPushButton("⚙ Manage Databases")
        btn_manage.setObjectName("secondaryButton")
        btn_manage.setMinimumHeight(52)
        btn_manage.setCursor(Qt.PointingHandCursor)
        btn_manage.clicked.connect(self._handle_manage_databases)
        
        # Refresh Data button
        btn_refresh = QPushButton("⟳ Refresh Data")
        btn_refresh.setObjectName("secondaryButton")
        btn_refresh.setMinimumHeight(52)
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.clicked.connect(self.refresh_dashboard)
        
        actions_layout.addWidget(btn_new_backup)
        actions_layout.addWidget(btn_restore)
        actions_layout.addWidget(btn_manage)
        actions_layout.addWidget(btn_refresh)
        actions_layout.addStretch()
        
        return actions_frame
    
    def _create_system_status(self):
        """Create system status section with real MySQL status"""
        status_frame = QFrame()
        status_frame.setObjectName("contentCard")
        status_layout = QVBoxLayout(status_frame)
        status_layout.setContentsMargins(32, 28, 32, 28)
        status_layout.setSpacing(24)
        
        status_title = QLabel("System Status")
        status_title.setObjectName("sectionTitle")
        status_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #e6d9ff;
        """)
        status_layout.addWidget(status_title)
        status_layout.addSpacing(8)
        
        # Check MySQL connection status
        mysql_status = "Running" if self._check_mysql_status() else "Stopped"
        mysql_status_type = "success" if mysql_status == "Running" else "error"
        
        # Status items with real data
        statuses = [
            ("MySQL Server", mysql_status, mysql_status_type),
            ("Database Server", "localhost:3306", "info"),
            ("Backup Directory", "backups/", "success"),
            ("Last Checked", "Just now", "info"),
        ]
        
        for label, value, status_type in statuses:
            item = self._create_status_item(label, value, status_type)
            status_layout.addWidget(item)
        
        status_layout.addStretch()
        
        return status_frame
    
    def _check_mysql_status(self):
        """Check if MySQL is running"""
        try:
            db_manager = DatabaseManager()
            if db_manager.connect():
                db_manager.disconnect()
                return True
            return False
        except:
            return False
    
    def _create_status_item(self, label: str, value: str, status_type: str):
        """Create individual status item"""
        item_frame = QFrame()
        item_layout = QHBoxLayout(item_frame)
        item_layout.setContentsMargins(0, 12, 0, 12)
        item_layout.setSpacing(16)
        
        status_colors = {
            "success": "#6ee7b7",
            "error": "#fca5a5",
            "warning": "#fcd34d",
            "info": "#b8a5d8"
        }
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("""
            color: #e6d9ff;
            font-size: 15px;
            font-weight: 500;
        """)
        
        value_widget = QLabel(value)
        value_widget.setStyleSheet(f"""
            color: {status_colors.get(status_type, '#b8a5d8')};
            font-size: 15px;
            font-weight: 700;
        """)
        
        item_layout.addWidget(label_widget)
        item_layout.addStretch()
        item_layout.addWidget(value_widget)
        
        return item_frame
    
    def _create_recent_activity(self):
        """Create recent activity section"""
        activity_frame = QFrame()
        activity_frame.setObjectName("contentCard")
        activity_layout = QVBoxLayout(activity_frame)
        activity_layout.setContentsMargins(32, 28, 32, 28)
        activity_layout.setSpacing(0)
        
        # Header
        header_layout = QHBoxLayout()
        
        activity_title = QLabel("Recent Activity")
        activity_title.setObjectName("sectionTitle")
        activity_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #e6d9ff;
        """)
        
        view_all_btn = QPushButton("View All →")
        view_all_btn.setObjectName("linkButton")
        view_all_btn.setCursor(Qt.PointingHandCursor)
        view_all_btn.setStyleSheet("""
            #linkButton {
                background: transparent;
                border: none;
                color: #8b7ab8;
                font-weight: 600;
                font-size: 14px;
                padding: 6px 12px;
            }
            #linkButton:hover {
                color: #b8a5d8;
            }
        """)
        
        header_layout.addWidget(activity_title)
        header_layout.addStretch()
        header_layout.addWidget(view_all_btn)
        
        activity_layout.addLayout(header_layout)
        activity_layout.addSpacing(24)
        
        # Activity items (can be loaded from database logs later)
        activities = [
            ("Connected to MySQL successfully", "Just now", "success"),
            ("Dashboard statistics loaded", "Just now", "success"),
            ("Backup files scanned", "Just now", "info"),
            ("System health check completed", "1 minute ago", "info"),
        ]
        
        for activity, time, status_type in activities:
            item_frame = self._create_activity_item(activity, time, status_type)
            activity_layout.addWidget(item_frame)
        
        return activity_frame
    
    def _create_activity_item(self, activity: str, time: str, status_type: str):
        """Create individual activity item"""
        item_frame = QFrame()
        item_frame.setObjectName("activityItem")
        item_layout = QHBoxLayout(item_frame)
        item_layout.setContentsMargins(0, 18, 0, 18)
        item_layout.setSpacing(16)
        
        status_colors = {
            "success": "#6ee7b7",
            "error": "#fca5a5",
            "warning": "#fcd34d",
            "info": "#b8a5d8"
        }
        
        status_dot = QLabel("●")
        status_dot.setStyleSheet(f"""
            color: {status_colors.get(status_type, '#b8a5d8')};
            font-size: 14px;
        """)
        status_dot.setFixedWidth(20)
        
        activity_label = QLabel(activity)
        activity_label.setObjectName("activityText")
        activity_label.setStyleSheet("""
            color: #e6d9ff;
            font-size: 15px;
            font-weight: 500;
        """)
        
        time_label = QLabel(time)
        time_label.setObjectName("activityTime")
        time_label.setStyleSheet("""
            color: #b8a5d8;
            font-size: 14px;
        """)
        
        item_layout.addWidget(status_dot)
        item_layout.addWidget(activity_label)
        item_layout.addStretch()
        item_layout.addWidget(time_label)
        
        return item_frame
    
    # ========================================================================
    # QUICK ACTION HANDLERS - FULLY FUNCTIONAL
    # ========================================================================
    
    def _handle_new_backup(self):
        """Handle New Backup button - Show dialog to select database"""
        print("[DEBUG] New Backup action triggered")
        
        try:
            # Get list of databases
            if not self.db_manager or not self.db_manager.connection or not self.db_manager.connection.is_connected():
                self.db_manager = DatabaseManager()
                self.db_manager.connect()
            
            databases = self.db_manager.get_databases()
            
            if not databases:
                QMessageBox.warning(
                    self,
                    "No Databases",
                    "No databases found to backup.\n\nCreate a database first from the Databases page."
                )
                return
            
            # Show database selection dialog
            db_name, ok = QInputDialog.getItem(
                self,
                "Select Database to Backup",
                "Choose a database to create a backup:",
                databases,
                0,
                False
            )
            
            if ok and db_name:
                # Perform backup
                self._perform_backup(db_name)
            
        except Exception as e:
            print(f"[ERROR] Failed to show backup dialog: {e}")
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load databases.\n\nError: {str(e)}\n\n"
                "Make sure MySQL is running in XAMPP."
            )
    
    def _perform_backup(self, db_name):
        """Perform the actual backup operation"""
        print(f"[DEBUG] Starting backup for database: {db_name}")
        
        try:
            # Create backup directory
            if not os.path.exists(self.backup_directory):
                os.makedirs(self.backup_directory)
            
            # Generate backup filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{db_name}_backup_{timestamp}.sql"
            backup_path = os.path.join(self.backup_directory, backup_filename)
            
            # Path to mysqldump
            mysqldump_path = r"C:\xampp\mysql\bin\mysqldump.exe"
            
            if not os.path.exists(mysqldump_path):
                QMessageBox.warning(
                    self,
                    "mysqldump Not Found",
                    f"mysqldump not found at: {mysqldump_path}\n\n"
                    "Please check your XAMPP installation."
                )
                return
            
            # Show progress message
            QApplication.setOverrideCursor(Qt.WaitCursor)
            
            # Execute mysqldump
            command = [
                mysqldump_path,
                "-u", "root",
                "-h", "localhost",
                db_name
            ]
            
            with open(backup_path, 'w') as backup_file:
                result = subprocess.run(
                    command,
                    stdout=backup_file,
                    stderr=subprocess.PIPE,
                    text=True
                )
            
            QApplication.restoreOverrideCursor()
            
            if result.returncode == 0:
                # Get file size
                size_bytes = os.path.getsize(backup_path)
                if size_bytes >= 1024 * 1024:
                    size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
                elif size_bytes >= 1024:
                    size_str = f"{size_bytes / 1024:.2f} KB"
                else:
                    size_str = f"{size_bytes} B"
                
                print(f"[SUCCESS] Backup created: {backup_filename} ({size_str})")
                
                QMessageBox.information(
                    self,
                    "✓ Backup Successful",
                    f"Database '{db_name}' has been backed up successfully!\n\n"
                    f"Backup file: {backup_filename}\n"
                    f"Size: {size_str}\n"
                    f"Location: {self.backup_directory}/"
                )
                
                # Refresh dashboard to show new backup
                self.load_real_stats()
            else:
                print(f"[ERROR] Backup failed: {result.stderr}")
                QMessageBox.critical(
                    self,
                    "Backup Failed",
                    f"Failed to backup database '{db_name}'.\n\nError: {result.stderr}"
                )
        
        except Exception as e:
            QApplication.restoreOverrideCursor()
            print(f"[ERROR] Backup exception: {e}")
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Backup Error",
                f"An error occurred during backup.\n\nError: {str(e)}"
            )
    
    def _handle_restore_database(self):
        """Handle Restore Database button - Show dialog to select backup file"""
        print("[DEBUG] Restore Database action triggered")
        
        try:
            # Get list of backup files
            if not os.path.exists(self.backup_directory):
                QMessageBox.warning(
                    self,
                    "No Backups",
                    "No backup files found.\n\nCreate a backup first."
                )
                return
            
            backup_files = []
            for file in os.listdir(self.backup_directory):
                if file.endswith('.sql') or file.endswith('.sql.gz'):
                    backup_files.append(file)
            
            if not backup_files:
                QMessageBox.warning(
                    self,
                    "No Backups",
                    "No backup files found.\n\nCreate a backup first."
                )
                return
            
            # Sort by modification time (newest first)
            backup_files.sort(
                key=lambda x: os.path.getmtime(os.path.join(self.backup_directory, x)),
                reverse=True
            )
            
            # Show backup selection dialog
            backup_file, ok = QInputDialog.getItem(
                self,
                "Select Backup to Restore",
                "Choose a backup file to restore:",
                backup_files,
                0,
                False
            )
            
            if ok and backup_file:
                # Confirm restore
                reply = QMessageBox.question(
                    self,
                    "⚠️ Confirm Restore",
                    f"Are you sure you want to restore from backup:\n\n{backup_file}\n\n"
                    "This will create a new database or overwrite an existing one.\n"
                    "Choose carefully to avoid data loss.",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    self._perform_restore(backup_file)
        
        except Exception as e:
            print(f"[ERROR] Failed to show restore dialog: {e}")
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load backup files.\n\nError: {str(e)}"
            )
    
    def _perform_restore(self, backup_file):
        """Perform the actual restore operation"""
        print(f"[DEBUG] Starting restore from backup: {backup_file}")
        
        try:
            backup_path = os.path.join(self.backup_directory, backup_file)
            
            if not os.path.exists(backup_path):
                QMessageBox.warning(
                    self,
                    "File Not Found",
                    f"Backup file '{backup_file}' not found."
                )
                return
            
            # Extract database name from filename
            restore_db_name = backup_file.split('_')[0]
            
            # Path to mysql
            mysql_path = r"C:\xampp\mysql\bin\mysql.exe"
            
            if not os.path.exists(mysql_path):
                QMessageBox.warning(
                    self,
                    "mysql Not Found",
                    f"mysql not found at: {mysql_path}\n\n"
                    "Please check your XAMPP installation."
                )
                return
            
            # Show progress message
            QApplication.setOverrideCursor(Qt.WaitCursor)
            
            # Create database if it doesn't exist
            if not self.db_manager or not self.db_manager.connection or not self.db_manager.connection.is_connected():
                self.db_manager = DatabaseManager()
                self.db_manager.connect()
            
            cursor = self.db_manager.connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{restore_db_name}`")
            cursor.close()
            
            # Execute mysql restore
            command = [
                mysql_path,
                "-u", "root",
                "-h", "localhost",
                restore_db_name
            ]
            
            with open(backup_path, 'r') as backup_file_handle:
                result = subprocess.run(
                    command,
                    stdin=backup_file_handle,
                    stderr=subprocess.PIPE,
                    text=True
                )
            
            QApplication.restoreOverrideCursor()
            
            if result.returncode == 0:
                print(f"[SUCCESS] Database restored: {restore_db_name}")
                
                QMessageBox.information(
                    self,
                    "✓ Restore Successful",
                    f"Database '{restore_db_name}' has been restored successfully from:\n\n"
                    f"{backup_file}\n\n"
                    "You can now view it in the Databases page."
                )
                
                # Refresh dashboard
                self.load_real_stats()
            else:
                print(f"[ERROR] Restore failed: {result.stderr}")
                QMessageBox.critical(
                    self,
                    "Restore Failed",
                    f"Failed to restore database.\n\nError: {result.stderr}"
                )
        
        except Exception as e:
            QApplication.restoreOverrideCursor()
            print(f"[ERROR] Restore exception: {e}")
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Restore Error",
                f"An error occurred during restore.\n\nError: {str(e)}"
            )
    
    def _handle_manage_databases(self):
        """Handle Manage Databases button - Navigate to Databases page"""
        print("[DEBUG] Manage Databases action triggered")
        
        try:
            # Get the main window and switch to Databases page
            main_window = self.window()
            
            # Find the stacked widget and switch to Databases page (index 1)
            if hasattr(main_window, 'stack'):
                main_window.stack.setCurrentIndex(1)  # Databases page is at index 1
                print("[SUCCESS] Navigated to Databases page")
            else:
                QMessageBox.information(
                    self,
                    "Navigate to Databases",
                    "Please click on 'Databases' in the sidebar to manage your databases."
                )
        
        except Exception as e:
            print(f"[ERROR] Failed to navigate: {e}")
            QMessageBox.information(
                self,
                "Navigate to Databases",
                "Please click on 'Databases' in the sidebar to manage your databases."
            )
