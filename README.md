# 📸 MySnapshot

**MySnapshot** is a modern, all-in-one desktop application designed for high-speed screen captures, professional-grade annotations, and efficient image management. Built with Python and PySide6, it offers a seamless workflow from capture to sharing.

---

## ✨ Key Features

### 1. 🚀 Quick Capture
- **Global Hotkey**: Press `Ctrl + Alt + S` to trigger the transparent capture overlay.
- **Precision Selection**: Real-time selection box with a dimming mask to highlight your focus.
- **Auto-Open**: After capture, the app automatically opens the integrated browser and selects the new image for immediate editing.

### 2. 🎨 Integrated Browser & Editor
- **All-in-One Interface**: No more switching windows. Browsing, zooming, and annotating happen in one unified workplace.
- **Annotation Suite**: 
  - 🟦 **Rectangle**: Draw boxes to frame content.
  - 🖊️ **Highlight**: Semi-transparent pens to emphasize text.
  - 🛡️ **Cover**: Solid blocks to redact sensitive information.
  - ↗️ **Arrow**: Point things out clearly.
  - 🔠 **Text**: Simple, double-click-to-edit text labels.
- **Dynamic Zoom**: Smoothly zoom in and out (up to 800%) using the toolbar or mouse.

### 3. 📋 Instant Sharing
- **Copy to Clipboard**: With a single click, copy your fully annotated image to the clipboard and paste it instantly into chat apps, documents, or emails.
- **Export**: Save your creations as PNG or JPG to any location.

### 4. 📁 Smart Collections
- **Automatic Organization**: Saves all screenshots into categorized collections in your `Pictures/MySnapshot` folder.
- **History Browser**: A clean sidebar to switch between different capture sessions.

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- PySide6
- mss (High-speed screen capture)
- Pillow (Image processing)

### Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/MySnapshot.git
   cd MySnapshot
   ```

2. **Install dependencies**:
   ```bash
   pip install PySide6 mss pillow
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

---

## ⌨️ Shortcuts
- **Capture**: `Ctrl + Alt + S`
- **Open Browser**: `Ctrl + Alt + B` (or via System Tray)
- **Exit**: Right-click the Tray icon -> Exit

---

## 🎨 UI & Design
- **Modern Aesthetic**: A clean, light-themed interface inspired by professional design systems.
- **Responsive Buttons**: Toolbar buttons automatically scale their font size to adapt to different window dimensions.
- **Unified Toolbar**: Neatly aligned and grouped controls for maximum usability.

---

## 📂 Project Structure
- `main.py`: Entry point, Tray icon, and global hotkey handling.
- `browser_window.py`: The core "All-in-One" UI featuring the Gallery and Annotation Canvas.
- `capture_overlay.py`: The transparent screen selection engine.
- `utils.py`: Storage and collection management logic.
- `styles.py`: Global QSS definitions for the premium look.

---

## ⚖️ License
MIT License. Feel free to use and contribute!
