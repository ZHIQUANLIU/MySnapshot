import sys
from PySide6.QtWidgets import (QMainWindow, QGraphicsView, QGraphicsScene, 
                             QVBoxLayout, QHBoxLayout, QWidget, QPushButton, 
                             QColorDialog, QToolBar, QGraphicsPixmapItem, 
                             QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem,
                             QGraphicsPolygonItem, QLabel)
from PySide6.QtCore import Qt, QRectF, QPointF, QLineF, Signal
from PySide6.QtGui import QPixmap, QColor, QBrush, QPen, QAction, QFont, QPolygonF, QCursor

class AnnotationScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_editor = parent
        self.selection_start = None
        self.temp_item = None
        self.temp_arrow_head = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.scenePos()
            self.selection_start = pos
            tool = self.parent_editor.current_tool
            color = self.parent_editor.current_color
            
            if tool == "Text":
                text_item = QGraphicsTextItem("Type here...")
                text_item.setFlags(QGraphicsTextItem.ItemIsMovable | QGraphicsTextItem.ItemIsSelectable)
                text_item.setDefaultTextColor(color)
                text_item.setFont(QFont("Arial", 16, QFont.Bold))
                text_item.setPos(pos)
                self.addItem(text_item)
                self.selection_start = None
            elif tool in ["Rectangle", "Highlight", "Cover"]:
                self.temp_item = QGraphicsRectItem()
                if tool == "Highlight":
                    c = QColor(color)
                    c.setAlpha(120)
                    self.temp_item.setBrush(QBrush(c))
                    self.temp_item.setPen(Qt.NoPen)
                elif tool == "Cover":
                    self.temp_item.setBrush(QBrush(color))
                    self.temp_item.setPen(Qt.NoPen)
                else: 
                    self.temp_item.setPen(QPen(color, 4))
                self.addItem(self.temp_item)
            elif tool == "Arrow":
                self.temp_item = QGraphicsLineItem()
                self.temp_item.setPen(QPen(color, 4))
                self.addItem(self.temp_item)
                self.temp_arrow_head = QGraphicsPolygonItem()
                self.temp_arrow_head.setBrush(QBrush(color))
                self.temp_arrow_head.setPen(Qt.NoPen)
                self.addItem(self.temp_arrow_head)
                
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.selection_start and self.temp_item:
            pos = event.scenePos()
            tool = self.parent_editor.current_tool
            
            if tool in ["Rectangle", "Highlight", "Cover"]:
                rect = QRectF(self.selection_start, pos).normalized()
                self.temp_item.setRect(rect)
            elif tool == "Arrow":
                line = QLineF(self.selection_start, pos)
                self.temp_item.setLine(line)
                angle = line.angle()
                p1 = line.p2()
                arrow_size = 20
                h1 = QLineF.fromPolar(arrow_size, angle + 150).p2() + p1
                h2 = QLineF.fromPolar(arrow_size, angle - 150).p2() + p1
                poly = QPolygonF([p1, h1, h2])
                self.temp_arrow_head.setPolygon(poly)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.temp_item:
            self.temp_item.setFlags(QGraphicsRectItem.ItemIsMovable | QGraphicsRectItem.ItemIsSelectable)
        self.selection_start = None
        self.temp_item = None
        self.temp_arrow_head = None
        super().mouseReleaseEvent(event)

class ImageEditor(QMainWindow):
    # Important signals for main.py integration
    save_requested = Signal()
    cancel_requested = Signal()

    def __init__(self, pixmap):
        super().__init__()
        self.setWindowTitle("MySnapshot Editor - Annotate Your Image")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint) # FORCE STAY ON TOP
        self.pixmap = pixmap
        self.scene = AnnotationScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(Qt.Antialiasing)
        
        self.pixmap_item = self.scene.addPixmap(self.pixmap)
        self.scene.setSceneRect(self.pixmap.rect())
        
        self.current_tool = "Rectangle"
        self.current_color = QColor(255, 0, 0) # Default Red
        
        self._init_ui()

    def _init_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # BRIGHT BLUE TOOLBAR
        self.toolbar_container = QWidget()
        self.toolbar_container.setStyleSheet("background-color: #1A73E8; border-bottom: 2px solid #0D47A1;")
        toolbar_layout = QHBoxLayout(self.toolbar_container)
        toolbar_layout.setContentsMargins(15, 8, 15, 8)
        
        header_label = QLabel("🛠️ EDIT TOOLS:")
        header_label.setStyleSheet("color: white; font-weight: bold; font-size: 15px; margin-right: 15px;")
        toolbar_layout.addWidget(header_label)

        self.tool_buttons = {}
        tools = [
            ("Rectangle", "🟦 Rect"),
            ("Highlight", "🖊️ High"),
            ("Cover", "🛡️ Cover"),
            ("Arrow", "↗️ Arrow"),
            ("Text", "text Text")
        ]
        
        for internal_name, display_name in tools:
            btn = QPushButton(display_name)
            btn.setCheckable(True)
            btn.setMinimumHeight(35)
            btn.setStyleSheet("""
                QPushButton { background-color: #FFFFFF; color: #1A73E8; border: none; font-weight: bold; padding: 5px 15px; border-radius: 4px; }
                QPushButton:checked { background-color: #FFD600; color: #000000; }
                QPushButton:hover { background-color: #E8F0FE; }
            """)
            btn.clicked.connect(lambda checked, n=internal_name: self.set_tool(n))
            toolbar_layout.addWidget(btn)
            self.tool_buttons[internal_name] = btn
        
        self.tool_buttons["Rectangle"].setChecked(True)
        
        color_btn = QPushButton("🎨 Color")
        color_btn.setStyleSheet("background-color: #FFFFFF; color: #333; margin-left: 15px;")
        color_btn.clicked.connect(self.pick_color)
        toolbar_layout.addWidget(color_btn)
        
        toolbar_layout.addStretch()
        
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.setStyleSheet("background-color: #EF5350; color: white; border: none;")
        cancel_btn.clicked.connect(self.cancel_requested.emit)
        toolbar_layout.addWidget(cancel_btn)

        save_btn = QPushButton("💾 SAVE EDITS")
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; border: none; font-weight: bold; padding: 5px 25px;")
        save_btn.clicked.connect(self.save_requested.emit) # Emit signal instead of direct call
        toolbar_layout.addWidget(save_btn)
        
        layout.addWidget(self.toolbar_container)
        layout.addWidget(self.view)
        self.setCentralWidget(main_widget)
        self.resize(1100, 850)

    def set_tool(self, tool):
        self.current_tool = tool
        for name, btn in self.tool_buttons.items():
            btn.setChecked(name == tool)

    def pick_color(self):
        color = QColorDialog.getColor(self.current_color, self)
        if color.isValid():
            self.current_color = color
