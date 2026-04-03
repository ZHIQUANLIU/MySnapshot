import sys
import os
import logging
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtCore import Qt, QObject, Signal, Slot, QBuffer, QIODevice
from PySide6.QtGui import QIcon, QAction, QPixmap, QPainter
from io import BytesIO
from PIL import Image

from capture_overlay import CaptureOverlay
from editor_window import ImageEditor
from browser_window import BrowserWindow
from utils import storage
from styles import STYLESHEET

from pynput import keyboard
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("mysnapshot.log", encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class GlobalHotkeyListener(QObject):
    # Signal emitted when a hotkey is pressed
    trigger_capture = Signal()
    trigger_browser = Signal()

    def __init__(self):
        super().__init__()
        self.listener = None

    def start(self):
        logger.info("Starting Global Hotkey Listener...")
        def on_activate_s():
            logger.info("Hotkey Ctrl+Alt+S detected")
            self.trigger_capture.emit()

        def on_activate_b():
            logger.info("Hotkey Ctrl+Alt+B detected")
            self.trigger_browser.emit()

        try:
            self.listener = keyboard.GlobalHotKeys({
                '<ctrl>+<alt>+s': on_activate_s,
                '<ctrl>+<alt>+b': on_activate_b
            })
            self.listener.start()
            logger.info("Hotkey listener started successfully.")
        except Exception as e:
            logger.error(f"Failed to start hotkey listener: {e}")

class MySnapshotApp(QObject):
    def __init__(self, app):
        super().__init__()
        logger.info("Initializing MySnapshotApp...")
        self.app = app
        self.app.setStyleSheet(STYLESHEET)
        
        self.tray_icon = QSystemTrayIcon(self)
        # Create a simple colored icon for the tray
        icon_pixmap = QPixmap(32, 32)
        icon_pixmap.fill(Qt.transparent)
        from PySide6.QtGui import QPainter, QColor
        p = QPainter(icon_pixmap)
        p.setBrush(QColor("#1A73E8"))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, 0, 32, 32, 8, 8)
        p.end()
        self.tray_icon.setIcon(QIcon(icon_pixmap))
        
        self.tray_menu = QMenu()
        self.update_tray_menu()
        
        self.tray_icon.show()
        logger.info("System Tray Icon visible.")
        
        # Hotkey listener
        self.hotkey_listener = GlobalHotkeyListener()
        self.hotkey_listener.trigger_capture.connect(self.start_capture)
        self.hotkey_listener.trigger_browser.connect(self.open_browser)
        self.hotkey_listener.start()
        
        self.overlay = None
        self.editor = None
        self.browser = None

    def update_tray_menu(self):
        self.tray_menu.clear()
        
        current_col_action = QAction(f"Current Collection: {storage.current_collection}", self)
        current_col_action.setEnabled(False)
        self.tray_menu.addAction(current_col_action)
        
        self.tray_menu.addSeparator()
        
        capture_action = QAction("Area Capture (Ctrl+Alt+S)", self)
        capture_action.triggered.connect(self.start_capture)
        self.tray_menu.addAction(capture_action)
        
        change_col_action = QAction("Change Collection...", self)
        change_col_action.triggered.connect(self.change_collection)
        self.tray_menu.addAction(change_col_action)
        
        browser_action = QAction("Open Browser (Ctrl+Alt+B)", self)
        browser_action.triggered.connect(self.open_browser)
        self.tray_menu.addAction(browser_action)
        
        self.tray_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.app.quit)
        self.tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(self.tray_menu)

    def change_collection(self):
        from PySide6.QtWidgets import QInputDialog
        collections = storage.get_all_collections()
        # Add an "Add New..." option
        items = collections + ["+ Add New..."]
        
        col, ok = QInputDialog.getItem(None, "Select Collection", 
                                     "Choose or create a collection:", 
                                     items, 
                                     items.index(storage.current_collection) if storage.current_collection in items else 0, 
                                     True) # Editable
        if ok and col:
            if col == "+ Add New...":
                new_col, ok_new = QInputDialog.getText(None, "New Collection", "Enter collection name:")
                if ok_new and new_col:
                    storage.set_collection(new_col)
                    logger.info(f"New collection created: {new_col}")
            else:
                storage.set_collection(col)
                logger.info(f"Collection switched to: {col}")
            self.update_tray_menu()

    @Slot()
    def start_capture(self):
        logger.info("Initiating Area Capture...")
        if self.overlay:
            self.overlay.close()
        self.overlay = CaptureOverlay()
        self.overlay.captured.connect(self.handle_capture)
        self.overlay.show()

    def handle_capture(self, pixmap):
        # Auto-save original first
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        pixmap.save(buffer, "PNG")
        
        img = Image.open(BytesIO(buffer.data().data()))
        saved_path = storage.save_image(img)
        self.last_saved_path = saved_path 
        
        logger.info(f"Capture auto-saved to {saved_path}")
        
        # Open browser and select the new image
        self.open_browser()
        # Find the item and select it
        filename = saved_path.name
        for i in range(self.browser.image_list.count()):
            item = self.browser.image_list.item(i)
            if item.data(Qt.UserRole) == filename:
                self.browser.image_list.setCurrentItem(item)
                self.browser.on_image_click(item)
                break

    def open_browser(self):
        if not self.browser:
            self.browser = BrowserWindow()
        self.browser.refresh_collections()
        self.browser.load_images()
        self.browser.show()
        self.browser.raise_()
        self.browser.activateWindow()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    mysnapshot = MySnapshotApp(app)
    sys.exit(app.exec())
