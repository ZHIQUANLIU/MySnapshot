# MySnapshot - Screen Capture & Management Tool (Python Edition)

MySnapshot is a modern desktop application built with **Python** and **PySide6** (Qt). It allows users to capture, annotate, and organize screenshots natively on Windows.

> [!IMPORTANT]
> **Tech Stack Change**: Switched from Electron to **Python + PySide6** as Node.js is not available in the current environment. PySide6 provides superior native performance for screen-hooking and drawing on Windows.

## Proposed Changes

### Core Architecture (Python)

#### [NEW] `main.py`
- Entry point for the application.
- `QApplication` lifecycle management.
- System Tray (`QSystemTrayIcon`) and Global Hotkey listener (`pynput`).
- IPC-like signals for communication between windows.

#### [NEW] `capture_overlay.py`
- A frameless, transparent `QWidget` spanning all monitors.
- Handles mouse events for area selection.
- Uses `mss` for high-performance screen grabbing.

#### [NEW] `editor_window.py`
- Based on `QGraphicsView` for high-fidelity annotations.
- **Tools**: Rect, Highlight, Text, Blur/Cover, Arrow.
- **Properties**: Color picker and line thickness.

#### [NEW] `browser_window.py`
- The main gallery/explorer interface.
- QListView/QGridView for browsing collections.
- Integration with standard Windows "Save As" dialogs.

### Dependencies
- `PySide6`: The UI framework.
- `mss`: Fast screen capture.
- `Pillow`: Image processing.
- `pynput`: Global keyboard/mouse hooks.

## Open Questions

> [!IMPORTANT]
> 1. **Hotkeys**: `Ctrl+Alt+S` (Area) and `Ctrl+Alt+F` (Full) will be the new defaults.
> 2. **Environment**: I will use a virtual environment if possible, or direct `pip install` to user site-packages.

## Verification Plan

### Manual Verification
- **Hotkey Test**: Press `Ctrl+Alt+S` -> Select area -> Editor opens.
- **Annotation Test**: Draw a red box -> Add text -> Save -> Verify PNG.
- **Gallery Test**: Open gallery -> See history -> Delete/Save as.
