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
        # self.setAttribute(Qt.WA_TranslucentBackground) # Removed to avoid visibility issues
        self.setWindowState(Qt.WindowFullScreen)
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)
        
        self.origin = QPoint()
        self.selection_rect = QRect()
        self.is_selecting = False
        
        # Grab the screen once at the start.
        self.full_screen_pixmap = QApplication.primaryScreen().grabWindow(0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 1. Draw the actual screen capture as the base layer
        painter.drawPixmap(self.rect(), self.full_screen_pixmap)
        
        # 2. Draw the semi-transparent overlay everywhere except the selection
        overlay_color = QColor(0, 0, 0, 120)
        
        if self.selection_rect.isNull():
            painter.fillRect(self.rect(), overlay_color)
        else:
            from PySide6.QtGui import QRegion
            full_region = QRegion(self.rect())
            cutout_region = QRegion(self.selection_rect)
            mask_region = full_region.subtracted(cutout_region)
            
            painter.setClipRegion(mask_region)
            painter.fillRect(self.rect(), overlay_color)
            painter.setClipping(False)
            
            # 3. Draw selection border and dimensions
            pen = QPen(QColor("#1A73E8"), 2)
            painter.setPen(pen)
            painter.drawRect(self.selection_rect)
            
            dim_text = f" {self.selection_rect.width()} x {self.selection_rect.height()} "
            painter.setBrush(QColor("#1A73E8"))
            painter.setPen(Qt.white)
            
            # Position the text slightly below the selection or at the bottom if no space
            text_pos = self.selection_rect.bottomLeft() + QPoint(0, 5)
            if text_pos.y() + 20 > self.height():
                text_pos = self.selection_rect.topLeft() - QPoint(0, 20)
                
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
