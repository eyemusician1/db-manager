"""
Custom monochrome icon provider - draws clean black icons using QPainter
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QIcon, QPainterPath


class IconProvider:
    """Provides custom monochrome icons drawn with QPainter"""
    
    @staticmethod
    def get_icon(name: str, size: int = 20, color: str = "#374151") -> QIcon:
        """Get a monochrome icon by name"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(color))
        pen.setWidth(max(1, size // 12))
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        
        margin = size // 5
        rect = QRect(margin, margin, size - 2 * margin, size - 2 * margin)
        
        if name == "dashboard":
            IconProvider._draw_dashboard(painter, rect)
        elif name == "database":
            IconProvider._draw_database(painter, rect)
        elif name == "backup":
            IconProvider._draw_backup(painter, rect)
        elif name == "users":
            IconProvider._draw_users(painter, rect)
        elif name == "settings":
            IconProvider._draw_settings(painter, rect)
        elif name == "storage":
            IconProvider._draw_storage(painter, rect)
        elif name == "time":
            IconProvider._draw_time(painter, rect)
        elif name == "add":
            IconProvider._draw_add(painter, rect)
        elif name == "restore":
            IconProvider._draw_restore(painter, rect)
        elif name == "menu":
            IconProvider._draw_menu(painter, rect)
        elif name == "chevron_left":
            IconProvider._draw_chevron_left(painter, rect)
        elif name == "chevron_right":
            IconProvider._draw_chevron_right(painter, rect)
        elif name == "user":
            IconProvider._draw_user(painter, rect)
        else:
            IconProvider._draw_default(painter, rect)
        
        painter.end()
        return QIcon(pixmap)
    
    @staticmethod
    def _draw_dashboard(painter: QPainter, rect: QRect):
        """Draw dashboard grid icon"""
        w, h = rect.width(), rect.height()
        x, y = rect.x(), rect.y()
        gap = w // 8
        half = (w - gap) // 2
        
        # Top-left square
        painter.drawRoundedRect(x, y, half, half, 2, 2)
        # Top-right square
        painter.drawRoundedRect(x + half + gap, y, half, half, 2, 2)
        # Bottom-left square
        painter.drawRoundedRect(x, y + half + gap, half, half, 2, 2)
        # Bottom-right square
        painter.drawRoundedRect(x + half + gap, y + half + gap, half, half, 2, 2)
    
    @staticmethod
    def _draw_database(painter: QPainter, rect: QRect):
        """Draw database cylinder icon"""
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        ellipse_h = h // 4
        
        # Top ellipse
        painter.drawEllipse(x, y, w, ellipse_h)
        # Body lines
        painter.drawLine(x, y + ellipse_h // 2, x, y + h - ellipse_h // 2)
        painter.drawLine(x + w, y + ellipse_h // 2, x + w, y + h - ellipse_h // 2)
        # Bottom ellipse
        painter.drawEllipse(x, y + h - ellipse_h, w, ellipse_h)
        # Middle line
        painter.drawArc(x, y + h // 2 - ellipse_h // 2, w, ellipse_h, 0, -180 * 16)
    
    @staticmethod
    def _draw_backup(painter: QPainter, rect: QRect):
        """Draw backup/save icon"""
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        
        # Outer rectangle
        painter.drawRoundedRect(x, y, w, h, 2, 2)
        # Inner save slot
        slot_w = w // 2
        slot_h = h // 3
        painter.drawRect(x + (w - slot_w) // 2, y, slot_w, slot_h)
        # Bottom detail
        detail_w = w * 2 // 3
        detail_h = h // 3
        painter.drawRoundedRect(x + (w - detail_w) // 2, y + h - detail_h - h // 8, detail_w, detail_h, 1, 1)
    
    @staticmethod
    def _draw_users(painter: QPainter, rect: QRect):
        """Draw users/people icon"""
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        
        # First person (front)
        head_r = w // 4
        painter.drawEllipse(x + w // 2 - head_r, y, head_r * 2, head_r * 2)
        # Body arc
        painter.drawArc(x + w // 6, y + h // 2, w * 2 // 3, h, 0, 180 * 16)
    
    @staticmethod
    def _draw_settings(painter: QPainter, rect: QRect):
        """Draw settings gear icon"""
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        cx, cy = x + w // 2, y + h // 2
        
        # Inner circle
        inner_r = w // 4
        painter.drawEllipse(cx - inner_r, cy - inner_r, inner_r * 2, inner_r * 2)
        
        # Outer gear teeth (simplified as circle with notches)
        outer_r = w // 2
        painter.drawEllipse(x, y, w, h)
    
    @staticmethod
    def _draw_storage(painter: QPainter, rect: QRect):
        """Draw storage/hard drive icon"""
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        
        # Main rectangle
        painter.drawRoundedRect(x, y, w, h, 3, 3)
        # Drive indicator circle
        indicator_r = w // 6
        painter.drawEllipse(x + w - indicator_r * 2 - w // 8, y + (h - indicator_r * 2) // 2, 
                           indicator_r * 2, indicator_r * 2)
        # Drive lines
        painter.drawLine(x + w // 8, y + h // 2, x + w // 2, y + h // 2)
    
    @staticmethod
    def _draw_time(painter: QPainter, rect: QRect):
        """Draw clock icon"""
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        cx, cy = x + w // 2, y + h // 2
        
        # Clock circle
        painter.drawEllipse(x, y, w, h)
        # Hour hand
        painter.drawLine(cx, cy, cx, y + h // 4)
        # Minute hand
        painter.drawLine(cx, cy, x + w * 3 // 4, cy)
    
    @staticmethod
    def _draw_add(painter: QPainter, rect: QRect):
        """Draw plus icon"""
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        cx, cy = x + w // 2, y + h // 2
        
        painter.drawLine(cx, y, cx, y + h)
        painter.drawLine(x, cy, x + w, cy)
    
    @staticmethod
    def _draw_restore(painter: QPainter, rect: QRect):
        """Draw restore/refresh icon"""
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        
        # Circular arrow
        painter.drawArc(x, y, w, h, 45 * 16, 270 * 16)
        # Arrow head
        ax, ay = x + w * 3 // 4, y + h // 4
        painter.drawLine(ax, ay, ax + w // 5, ay)
        painter.drawLine(ax, ay, ax, ay + h // 5)
    
    @staticmethod
    def _draw_menu(painter: QPainter, rect: QRect):
        """Draw hamburger menu icon"""
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        spacing = h // 4
        
        painter.drawLine(x, y + spacing, x + w, y + spacing)
        painter.drawLine(x, y + h // 2, x + w, y + h // 2)
        painter.drawLine(x, y + h - spacing, x + w, y + h - spacing)
    
    @staticmethod
    def _draw_chevron_left(painter: QPainter, rect: QRect):
        """Draw left chevron"""
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        
        painter.drawLine(x + w * 2 // 3, y, x + w // 3, y + h // 2)
        painter.drawLine(x + w // 3, y + h // 2, x + w * 2 // 3, y + h)
    
    @staticmethod
    def _draw_chevron_right(painter: QPainter, rect: QRect):
        """Draw right chevron"""
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        
        painter.drawLine(x + w // 3, y, x + w * 2 // 3, y + h // 2)
        painter.drawLine(x + w * 2 // 3, y + h // 2, x + w // 3, y + h)
    
    @staticmethod
    def _draw_user(painter: QPainter, rect: QRect):
        """Draw single user icon"""
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        
        # Head
        head_r = w // 3
        painter.drawEllipse(x + w // 2 - head_r, y, head_r * 2, head_r * 2)
        # Body
        painter.drawArc(x, y + h // 2, w, h, 0, 180 * 16)
    
    @staticmethod
    def _draw_default(painter: QPainter, rect: QRect):
        """Draw default file icon"""
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        fold = w // 4
        
        path = QPainterPath()
        path.moveTo(x, y)
        path.lineTo(x + w - fold, y)
        path.lineTo(x + w, y + fold)
        path.lineTo(x + w, y + h)
        path.lineTo(x, y + h)
        path.closeSubpath()
        painter.drawPath(path)
        painter.drawLine(x + w - fold, y, x + w - fold, y + fold)
        painter.drawLine(x + w - fold, y + fold, x + w, y + fold)
