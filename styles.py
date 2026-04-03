STYLESHEET = """
QMainWindow, QDialog, QWidget {
    background-color: #F9F9FB;
    color: #333333;
    font-family: 'Segoe UI', 'Inter', 'Roboto', sans-serif;
}

/* Modern List Widget Styling */
QListWidget {
    background-color: #FFFFFF;
    border: none;
    border-right: 1px solid #E0E0E0;
    outline: none;
}

QListWidget::item {
    padding: 12px;
    border-bottom: 1px solid #F5F5F7;
    color: #5F6368;
    border-radius: 8px;
    margin: 4px 8px;
}

QListWidget::item:hover {
    background-color: #F1F3F4;
}

QListWidget::item:selected {
    background-color: #E8F0FE;
    color: #1A73E8;
    font-weight: 600;
}

/* Premium Button Styling */
QPushButton {
    background-color: #FFFFFF;
    color: #3C4043;
    border: 1px solid #DADCE0;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #F8F9FA;
    border-color: #1A73E8;
    color: #1A73E8;
}

QPushButton:pressed {
    background-color: #E8F0FE;
}

QPushButton:disabled {
    color: #BDC1C6;
    border-color: #F1F3F4;
    background-color: #FFFFFF;
}

/* Primary Action Button (Blue) */
#ApplyBtn {
    background-color: #1A73E8;
    color: white;
    border: none;
}

#ApplyBtn:hover {
    background-color: #1765CC;
}

#ApplyBtn:pressed {
    background-color: #1557B0;
}

/* Danger Button (Red) */
#DeleteBtn {
    color: #D93025;
    border-color: #FAD2CF;
}

#DeleteBtn:hover {
    background-color: #FEF7F6;
    border-color: #D93025;
}

/* Sidebar Styling */
#Sidebar {
    background-color: #F8F9FA;
    border-right: 1px solid #E0E0E0;
}

/* Graphics View Area */
QGraphicsView {
    background-color: #F1F3F4;
    border: 1px solid #DADCE0;
    border-radius: 8px;
}

/* Toolbar Frame */
#ToolbarFrame {
    background-color: #FFFFFF;
    border-bottom: 1px solid #E0E0E0;
    padding: 5px;
}
"""
