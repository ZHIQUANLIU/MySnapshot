import sys
from PySide6.QtWidgets import QWidget, QApplication, QRubberBand
from PySide6.QtCore import Qt, QRect, QPoint, Signal, QSize
from PySide6.QtGui import QPainter, QColor, QPen, QCursor, QPixmap, QScreen
import mss
import mss.tools

class CaptureOverlay(QWidget):
    # Signal emitted when capture is finished with the captured QPixmap
    captured = Signal(object)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground) # Make background transparent
        self.setWindowState(Qt.WindowFullScreen)
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)
        
        self.origin = QPoint()
        self.selection_rect = QRect()
        self.is_selecting = False
        
        # We don't necessarily need the full screen pixmap anymore 
        # if we just want to see the "live" screen, but we'll keep it for the dimmed effect
        self.full_screen_pixmap = QApplication.primaryScreen().grabWindow(0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 1. Fill the entire screen with a semi-transparent dark shade
        overlay_color = QColor(0, 0, 0, 120) # 120/255 opacity
        
        if self.selection_rect.isNull():
            # Nothing selected: dim the whole screen
            painter.fillRect(self.rect(), overlay_color)
        else:
            # Masking: Dim everything EXCEPT the selection_rect
            from PySide6.QtGui import QRegion
            full_region = QRegion(self.rect())
            cutout_region = QRegion(self.selection_rect)
            mask_region = full_region.subtracted(cutout_region)
            
            painter.setClipRegion(mask_region)
            painter.fillRect(self.rect(), overlay_color)
            painter.setClipping(False)
            
            # Draw a border around the selection
            pen = QPen(QColor("#1A73E8"), 2)
            painter.setPen(pen)
            painter.drawRect(self.selection_rect)
            
            # Show the dimensions in a tooltip-like box
            dim_text = f" {self.selection_rect.width()} x {self.selection_rect.height()} "
            painter.setBrush(QColor("#1A73E8"))
            painter.setPen(Qt.white)
            rect_text = painter.fontMetrics().boundingRect(dim_text)
            rect_text.moveCenter(self.selection_rect.center())
            # Move text box above or below selection
            text_pos = self.selection_rect.bottomLeft() + QPoint(0, 5)
            painter.drawText(text_pos + QPoint(5, 15), dim_text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.selection_rect = QRect(self.origin, QSize())
            self.is_selecting = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.selection_rect = QRect(self.origin, event.pos()).normalized()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_selecting:
            self.is_selecting = False
            if self.selection_rect.width() > 5 and self.selection_rect.height() > 5:
                self._finish_capture()
            else:
                self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def _finish_capture(self):
        # Crop the background pixmap
        cropped = self.full_screen_pixmap.copy(self.selection_rect)
        self.captured.emit(cropped)
        self.close()

if __name__ == "__main__":
    # Test stub
    app = QApplication(sys.argv)
    overlay = CaptureOverlay()
    overlay.show()
    sys.exit(app.exec())
