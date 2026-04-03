import sys
import os
from datetime import datetime
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QListWidgetItem, QLabel, QScrollArea, 
                             QSplitter, QFrame, QPushButton, QFileDialog, QToolBar,
                             QMessageBox, QMenu, QGraphicsView, QGraphicsScene,
                             QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem,
                             QGraphicsPolygonItem, QColorDialog)
from PySide6.QtCore import Qt, QSize, Signal, QRectF, QPointF, QLineF, QTimer
from PySide6.QtGui import QPixmap, QIcon, QAction, QCursor, QColor, QBrush, QPen, QFont, QPolygonF, QPainter
from utils import storage

class AnnotationScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.browser = parent
        self.selection_start = None
        self.temp_item = None
        self.temp_arrow_head = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.scenePos()
            self.selection_start = pos
            tool = self.browser.current_tool
            color = self.browser.current_tool_color
            
            # Check if we clicked an existing text item to edit
            item = self.itemAt(pos, self.browser.view.transform())
            if isinstance(item, QGraphicsTextItem) and not tool:
                item.setTextInteractionFlags(Qt.TextEditorInteraction)
                item.setFocus()
                super().mousePressEvent(event)
                return

            if not tool:
                super().mousePressEvent(event)
                return

            if tool == "Text":
                text_item = QGraphicsTextItem("Type here...")
                text_item.setFlags(QGraphicsTextItem.ItemIsMovable | QGraphicsTextItem.ItemIsSelectable)
                text_item.setTextInteractionFlags(Qt.TextEditorInteraction) # MAKE EDITABLE
                text_item.setDefaultTextColor(color)
                text_item.setFont(QFont("Segoe UI", 20, QFont.Bold))
                text_item.setPos(pos)
                self.addItem(text_item)
                # Auto-focus and select all for immediate typing
                text_item.setFocus()
                cursor = text_item.textCursor()
                cursor.select(cursor.SelectionType.Document)
                text_item.setTextCursor(cursor)
                
                self.selection_start = None
            elif tool in ["Rectangle", "Highlight", "Cover"]:
                self.temp_item = QGraphicsRectItem()
                if tool == "Highlight":
                    c = QColor(color)
                    c.setAlpha(100)
                    self.temp_item.setBrush(QBrush(c))
                    self.temp_item.setPen(Qt.NoPen)
                elif tool == "Cover":
                    self.temp_item.setBrush(QBrush(color))
                    self.temp_item.setPen(Qt.NoPen)
                else: 
                    self.temp_item.setPen(QPen(color, 3))
                self.addItem(self.temp_item)
            elif tool == "Arrow":
                self.temp_item = QGraphicsLineItem()
                self.temp_item.setPen(QPen(color, 3))
                self.addItem(self.temp_item)
                self.temp_arrow_head = QGraphicsPolygonItem()
                self.temp_arrow_head.setBrush(QBrush(color))
                self.temp_arrow_head.setPen(Qt.NoPen)
                self.addItem(self.temp_arrow_head)
                
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.selection_start and self.temp_item:
            pos = event.scenePos()
            tool = self.browser.current_tool
            
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

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.scenePos(), self.browser.view.transform())
        if isinstance(item, QGraphicsTextItem):
            item.setTextInteractionFlags(Qt.TextEditorInteraction)
            item.setFocus()
            # Restore selection
            cursor = item.textCursor()
            cursor.select(cursor.SelectionType.Document)
            item.setTextCursor(cursor)
        super().mouseDoubleClickEvent(event)

class ResponsiveButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40) # Slightly taller for better scaling
        from PySide6.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        h = self.height()
        w = self.width()
        # Adjusted formula for unified widths:
        # We want it to scale with height mostly unless width is extremely narrow.
        # h*0.4 is a good baseline for a button of height 40-50.
        new_size = max(10, min(15, int(h * 0.42)))
        # If the button is wide (like Apply Changes), we can allow larger font
        if w > 150:
            new_size = max(10, min(20, int(h * 0.45)))
            
        font = self.font()
        font.setPointSize(new_size)
        self.setFont(font)

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MySnapshot - Browse & Annotate")
        self.resize(1400, 900)
        
        self.current_img_name = None
        self.zoom_factor = 1.0
        self.current_tool = None 
        self.current_tool_color = QColor(255, 0, 0)
        
        self._init_ui()
        self.refresh_collections()
        self.load_images()

    def _init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        splitter = QSplitter(Qt.Horizontal)
        
        # Sidebar
        self.sidebar_container = QWidget()
        self.sidebar_container.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar_container)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        sidebar_title = QLabel(" 📁 COLLECTIONS")
        sidebar_title.setStyleSheet("font-weight: bold; color: #5F6368; padding: 15px 10px; font-size: 11px;")
        sidebar_layout.addWidget(sidebar_title)
        
        self.sidebar = QListWidget()
        self.sidebar.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sidebar.customContextMenuRequested.connect(self.on_sidebar_context_menu)
        self.sidebar.itemClicked.connect(self.on_collection_click)
        sidebar_layout.addWidget(self.sidebar)
        splitter.addWidget(self.sidebar_container)
        
        # Image List
        self.list_container = QWidget()
        list_layout = QVBoxLayout(self.list_container)
        list_layout.setContentsMargins(0, 0, 0, 0)
        
        list_title = QLabel(" 🖼️ SCREENSHOTS")
        list_title.setStyleSheet("font-weight: bold; color: #5F6368; padding: 15px 10px; font-size: 11px;")
        list_layout.addWidget(list_title)
        
        self.image_list = QListWidget()
        self.image_list.setIconSize(QSize(110, 110))
        self.image_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.image_list.customContextMenuRequested.connect(self.on_image_list_context_menu)
        self.image_list.itemClicked.connect(self.on_image_click)
        list_layout.addWidget(self.image_list)
        splitter.addWidget(self.list_container)
        
        # Preview Area
        self.preview_pane = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_pane)
        self.preview_pane.setMinimumWidth(800)
        self.preview_layout.setContentsMargins(15, 15, 15, 15)
        self.preview_layout.setSpacing(15)
        
        # MODERN TOOLBAR
        self.toolbar_frame = QFrame()
        self.toolbar_frame.setObjectName("ToolbarFrame")
        toolbar = QHBoxLayout(self.toolbar_frame)
        toolbar.setContentsMargins(10, 8, 10, 8)
        toolbar.setSpacing(8)
        
        # Group: Zoom
        self.zoom_out = ResponsiveButton("➖ Zoom Out")
        self.zoom_out.clicked.connect(lambda: self.adjust_zoom(0.8))
        self.zoom_in = ResponsiveButton("➕ Zoom In")
        self.zoom_in.clicked.connect(lambda: self.adjust_zoom(1.2))
        
        toolbar.addWidget(self.zoom_out)
        toolbar.addWidget(self.zoom_in)
        
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setFixedWidth(1)
        line.setStyleSheet("background-color: #E0E0E0; margin: 4px;")
        toolbar.addWidget(line)
        
        # Group: Tools
        self.tool_buttons = {}
        tools = [("Rectangle", "🟦 Rect"), ("Highlight", "🖊️ High"), 
                 ("Cover", "🛡️ Cover"), ("Arrow", "↗️ Arrow"), ("Text", "text Text")]
        
        # Tools Container for Neatness
        for internal, display in tools:
            btn = ResponsiveButton(display)
            btn.setCheckable(True)
            btn.setMinimumWidth(90) # UNIFIED WIDTH
            btn.clicked.connect(lambda checked, t=internal: self.set_tool(t))
            toolbar.addWidget(btn)
            self.tool_buttons[internal] = btn
            
        self.color_btn = ResponsiveButton("🎨 Color")
        self.color_btn.setMinimumWidth(100)
        self.color_btn.clicked.connect(self.pick_color)
        toolbar.addWidget(self.color_btn)
        
        toolbar.addStretch(1) # Push primary actions to right
        
        self.copy_btn = ResponsiveButton("📋 Copy")
        self.copy_btn.setMinimumWidth(100)
        self.copy_btn.setEnabled(False)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        toolbar.addWidget(self.copy_btn)

        self.apply_btn = ResponsiveButton("💾 Apply")
        self.apply_btn.setMinimumWidth(100)
        self.apply_btn.setObjectName("ApplyBtn")
        self.apply_btn.setEnabled(False)
        self.apply_btn.clicked.connect(self.apply_edits)
        toolbar.addWidget(self.apply_btn)
        
        self.preview_layout.addWidget(self.toolbar_frame)
        
        # Graphics View
        self.scene = AnnotationScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.preview_layout.addWidget(self.view)
        
        # Footer
        footer = QHBoxLayout()
        self.details_label = QLabel("Ready")
        self.details_label.setStyleSheet("color: #70757A; font-size: 12px;")
        footer.addWidget(self.details_label)
        footer.addStretch()
        
        self.save_as_btn = QPushButton("📂 Export...")
        self.save_as_btn.setEnabled(False)
        self.save_as_btn.clicked.connect(self.save_as)
        footer.addWidget(self.save_as_btn)
        
        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.setObjectName("DeleteBtn")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_active_image)
        footer.addWidget(self.delete_btn)
        
        self.preview_layout.addLayout(footer)
        
        splitter.addWidget(self.preview_pane)
        main_layout.addWidget(splitter)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def set_tool(self, tool):
        self.current_tool = tool if self.current_tool != tool else None
        for name, btn in self.tool_buttons.items():
            btn.setChecked(name == self.current_tool)

    def pick_color(self):
        color = QColorDialog.getColor(self.current_tool_color, self)
        if color.isValid(): self.current_tool_color = color

    def adjust_zoom(self, delta):
        self.zoom_factor *= delta
        self.zoom_factor = max(0.1, min(self.zoom_factor, 8.0))
        self.view.resetTransform()
        self.view.scale(self.zoom_factor, self.zoom_factor)

    def on_image_click(self, item):
        img_name = item.data(Qt.UserRole)
        self.current_img_name = img_name
        self.zoom_factor = 1.0
        self.view.resetTransform()
        self.load_image_to_canvas(img_name)
        self.details_label.setText(f"File: {img_name}")
        self.save_as_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)
        self.apply_btn.setEnabled(True)
        self.copy_btn.setEnabled(True)

    def copy_to_clipboard(self):
        if not self.current_img_name: return
        pixmap = QPixmap(self.scene.sceneRect().size().toSize())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        self.scene.render(painter)
        painter.end()
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setPixmap(pixmap)
        # Show a small feedback in status or tooltip
        self.details_label.setText("✅ Copied to clipboard!")
        QTimer.singleShot(2000, lambda: self.details_label.setText(f"File: {self.current_img_name}"))

    def load_image_to_canvas(self, img_name):
        path = storage.get_collection_path() / img_name
        if not path.exists(): return
        self.scene.clear()
        pixmap = QPixmap(str(path))
        if not pixmap.isNull():
            self.scene.addPixmap(pixmap)
            self.scene.setSceneRect(pixmap.rect())
            QTimer.singleShot(80, lambda: self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio))

    def apply_edits(self):
        if not self.current_img_name: return
        path = storage.get_collection_path() / self.current_img_name
        
        # Save original scene rect to keep quality
        pixmap = QPixmap(self.scene.sceneRect().size().toSize())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        self.scene.render(painter)
        painter.end()
        
        pixmap.save(str(path), "PNG")
        QMessageBox.information(self, "Success", "Changes applied successfully!")
        self.load_images()

    def refresh_collections(self):
        self.sidebar.clear()
        for col in storage.get_all_collections():
            item = QListWidgetItem(col)
            self.sidebar.addItem(item)
            if col == storage.current_collection: self.sidebar.setCurrentItem(item)

    def on_collection_click(self, item):
        storage.set_collection(item.text())
        self.load_images()
        self.scene.clear()
        self.apply_btn.setEnabled(False)

    def load_images(self):
        self.image_list.clear()
        col_path = storage.get_collection_path()
        if not col_path.exists(): return
        images = sorted([f for f in os.listdir(col_path) if f.lower().endswith(('.png', '.jpg'))], reverse=True)
        for img_name in images:
            img_path = os.path.join(col_path, img_name)
            pixmap = QPixmap(img_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            stats = os.stat(img_path)
            dt = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
            item = QListWidgetItem(f"{img_name}\n{dt}")
            item.setIcon(QIcon(pixmap))
            item.setData(Qt.UserRole, img_name)
            self.image_list.addItem(item)

    def delete_active_image(self):
        if self.current_img_name and QMessageBox.question(self, "Delete", "Confirm delete image?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            if storage.delete_image(self.current_img_name):
                self.load_images()
                self.scene.clear()
                self.apply_btn.setEnabled(False)

    def on_sidebar_context_menu(self, pos):
        item = self.sidebar.itemAt(pos)
        if not item: return
        
        menu = QMenu(self)
        del_action = menu.addAction("🗑️ Delete Collection")
        
        action = menu.exec(self.sidebar.mapToGlobal(pos))
        if action == del_action:
            col_name = item.text()
            if col_name == "Default":
                QMessageBox.warning(self, "Error", "Cannot delete the Default collection.")
                return
                
            if QMessageBox.question(self, "Delete Collection", f"Are you sure you want to delete the collection '{col_name}' and all its images?", 
                                    QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
                if storage.delete_collection(col_name):
                    self.refresh_collections()
                    # If we deleted the current one, the logic in storage resets it to Default
                    self.load_images()
                    self.scene.clear()

    def on_image_list_context_menu(self, pos):
        item = self.image_list.itemAt(pos)
        if not item: return
        
        self.image_list.setCurrentItem(item)
        self.on_image_click(item) # Select it
        
        menu = QMenu(self)
        copy_action = menu.addAction("📋 Copy to Clipboard")
        export_action = menu.addAction("📂 Export...")
        menu.addSeparator()
        del_action = menu.addAction("🗑️ Delete Image")
        
        action = menu.exec(self.image_list.mapToGlobal(pos))
        if action == copy_action:
            self.copy_to_clipboard()
        elif action == export_action:
            self.save_as()
        elif action == del_action:
            self.delete_active_image()

    def save_as(self):
        if not self.current_img_name: return
        src = os.path.join(storage.get_collection_path(), self.current_img_name)
        dest, _ = QFileDialog.getSaveFileName(self, "Export File", self.current_img_name, "Images (*.png *.jpg)")
        if dest:
            import shutil
            shutil.copy2(src, dest)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec())
