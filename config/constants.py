"""
Application constants
"""

# Application info
APP_NAME = "BackMeUp"
APP_VERSION = "1.0.0"

# Page names
PAGE_DASHBOARD = "Dashboard"
PAGE_DATABASES = "Databases"
PAGE_BACKUPS = "Backups"
PAGE_USERS = "Users"
PAGE_SETTINGS = "Settings"

NAV_ITEMS = [
    (PAGE_DASHBOARD, "SP_ComputerIcon"),
    (PAGE_DATABASES, "SP_DriveHDIcon"),
    (PAGE_BACKUPS, "SP_DialogSaveButton"),
    (PAGE_USERS, "SP_FileIcon"),
    (PAGE_SETTINGS, "SP_FileDialogDetailedView"),
]

# Status messages
STATUS_CONNECTED = "Connected"
STATUS_DISCONNECTED = "Disconnected"
STATUS_CONNECTING = "Connecting..."

# UI constants
SIDEBAR_WIDTH_EXPANDED = 200
SIDEBAR_WIDTH_COLLAPSED = 56
TOP_BAR_HEIGHT = 50
MIN_WINDOW_WIDTH = 1024
MIN_WINDOW_HEIGHT = 768
