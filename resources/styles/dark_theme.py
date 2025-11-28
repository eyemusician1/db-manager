"""
Modern Pastel Dark Theme - FIXED for collapsed sidebar
"""

MODERN_GRAY_THEME = """
* {
    font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 14px;
}

QMainWindow {
    background-color: #1a1625;
}

/* Sidebar - Deep purple with pastel accents */
#sidebar {
    background-color: #252235;
    border-right: 1px solid #33304a;
}

#sidebarHeader {
    background-color: transparent;
    border-bottom: 1px solid #33304a;
}

/* Center header content when sidebar is collapsed */
#sidebarHeader QHBoxLayout {
    justify-content: center;
}

#sidebarSeparator {
    background-color: #33304a;
}

#sidebarFooter {
    background-color: transparent;
}

#appTitle {
    font-size: 20px;
    font-weight: 700;
    color: #e6d9ff;
    letter-spacing: -0.5px;
}

#toggleButton {
    background-color: transparent;
    border: 1px solid #33304a;
    border-radius: 8px;
    color: #b8a5d8;
    padding: 8px;
    font-size: 18px;
}

#toggleButton:hover {
    background-color: #33304a;
    border-color: #8b7ab8;
    color: #e6d9ff;
}

/* Navigation Buttons - Pastel purple accents */
#navButton {
    background-color: transparent;
    color: #b8a5d8;
    border: none;
    border-radius: 10px;
    text-align: left;
    padding: 14px 20px;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.2px;
}

/* Collapsed state - centered icons */
#navButton[collapsed="true"] {
    text-align: center;
    padding: 14px 8px;
    font-size: 20px;
}

#navButton:hover {
    background-color: #33304a;
    color: #e6d9ff;
}

#navButton:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #8b7ab8, stop:1 #b8a5d8);
    color: #1a1625;
    font-weight: 700;
}

/* Content Area - Dark purple background */
#contentArea {
    background-color: #1a1625;
}

#mainScrollArea {
    background-color: transparent;
    border: none;
}

/* Top bar - Subtle gradient */
#topBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #252235, stop:1 #1f1c2e);
    border-bottom: 1px solid #33304a;
}

#breadcrumb {
    color: #b8a5d8;
    font-size: 14px;
    font-weight: 500;
}

#profileButton {
    background-color: transparent;
    color: #e6d9ff;
    border: 1px solid #8b7ab8;
    padding: 10px 18px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
}

#profileButton:hover {
    background-color: #33304a;
    border-color: #b8a5d8;
}

/* Page Content */
#pageTitle {
    font-size: 32px;
    font-weight: 700;
    color: #e6d9ff;
    letter-spacing: -1px;
}

#sectionTitle {
    font-size: 18px;
    font-weight: 700;
    color: #e6d9ff;
}

/* Cards - Dark with pastel borders */
#contentCard {
    background-color: #252235;
    border: 1px solid #33304a;
    border-radius: 16px;
}

/* Stat Cards */
#statCard {
    background-color: #252235;
    border: 1px solid #33304a;
    border-radius: 16px;
}

#cardValue {
    color: #e6d9ff;
    font-size: 32px;
    font-weight: 700;
}

#cardTitle {
    color: #b8a5d8;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Activity */
#activityItem {
    background-color: transparent;
    border-bottom: 1px solid #33304a;
}

#activityItem:last-child {
    border-bottom: none;
}

#activityText {
    color: #e6d9ff;
    font-size: 14px;
    font-weight: 500;
}

#activityTime {
    color: #b8a5d8;
    font-size: 13px;
}

/* Buttons - Pastel accents */
#primaryButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #8b7ab8, stop:1 #7a6ba3);
    color: #1a1625;
    border: none;
    padding: 12px 24px;
    border-radius: 10px;
    font-weight: 700;
    font-size: 14px;
}

#primaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #9b8ac8, stop:1 #8b7ab8);
}

#primaryButton:pressed {
    background-color: #7a6ba3;
}

#secondaryButton {
    background-color: transparent;
    color: #e6d9ff;
    border: 1px solid #8b7ab8;
    padding: 12px 24px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 14px;
}

#secondaryButton:hover {
    background-color: #33304a;
    border-color: #b8a5d8;
}

#destructiveButton {
    background-color: transparent;
    color: #f8a5c2;
    border: 1px solid #f8a5c2;
    padding: 12px 24px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 14px;
}

#destructiveButton:hover {
    background-color: #2d1f27;
}

/* Form Elements */
QLineEdit, QComboBox {
    background-color: #1f1c2e;
    color: #e6d9ff;
    border: 1px solid #33304a;
    border-radius: 10px;
    padding: 11px 16px;
    font-size: 14px;
}

QLineEdit:focus, QComboBox:focus {
    border: 2px solid #8b7ab8;
    padding: 10px 15px;
}

QLineEdit::placeholder {
    color: #736887;
}

/* Tables */
QTableWidget, QTreeWidget {
    background-color: #252235;
    color: #e6d9ff;
    border: 1px solid #33304a;
    border-radius: 12px;
    gridline-color: #33304a;
}

QTableWidget::item, QTreeWidget::item {
    padding: 14px 10px;
    border-bottom: 1px solid #33304a;
}

QTableWidget::item:selected, QTreeWidget::item:selected {
    background-color: #33304a;
    color: #e6d9ff;
}

QHeaderView::section {
    background-color: #1f1c2e;
    color: #b8a5d8;
    padding: 14px 10px;
    border: none;
    border-bottom: 2px solid #33304a;
    font-weight: 700;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* Tabs */
QTabWidget::pane {
    border: none;
    background-color: transparent;
}

QTabBar::tab {
    background-color: transparent;
    color: #b8a5d8;
    padding: 14px 24px;
    border-bottom: 3px solid transparent;
    margin-right: 4px;
    font-weight: 600;
}

QTabBar::tab:selected {
    color: #e6d9ff;
    border-bottom: 3px solid #8b7ab8;
}

QTabBar::tab:hover:!selected {
    color: #e6d9ff;
    background-color: #33304a;
}

/* Checkbox */
QCheckBox {
    color: #e6d9ff;
    spacing: 12px;
    font-weight: 500;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #8b7ab8;
    border-radius: 6px;
    background-color: #1f1c2e;
}

QCheckBox::indicator:hover {
    border-color: #b8a5d8;
}

QCheckBox::indicator:checked {
    background-color: #8b7ab8;
    border-color: #8b7ab8;
}

/* Scrollbar - Pastel accent */
QScrollBar:vertical {
    background-color: transparent;
    width: 12px;
    margin: 4px;
}

QScrollBar::handle:vertical {
    background-color: #33304a;
    border-radius: 6px;
    min-height: 40px;
}

QScrollBar::handle:vertical:hover {
    background-color: #8b7ab8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: transparent;
    height: 12px;
    margin: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #33304a;
    border-radius: 6px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #8b7ab8;
}

/* Status Bar */
#statusBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1f1c2e, stop:1 #252235);
    color: #b8a5d8;
    border-top: 1px solid #33304a;
    font-size: 13px;
    padding: 6px 0;
}

QLabel {
    color: #e6d9ff;
}

QSplitter::handle {
    background-color: #33304a;
}

QSplitter::handle:hover {
    background-color: #8b7ab8;
}

/* Tooltips */
QToolTip {
    background-color: #252235;
    color: #e6d9ff;
    border: 1px solid #8b7ab8;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
}
"""