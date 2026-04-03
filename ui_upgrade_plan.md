# UI Polish: Light Mode & Editor Visibility

This plan addresses feedback regarding the application's appearance and the missing toolbar in the editor.

## Proposed Changes

### [MODIFY] [styles.py](file:///c:/OpenCode/MySnapshot/styles.py)
- **Light Mode Transition**: 
    - Change background to `#F5F5F7` (Light Grey/White).
    - Change text to `#333333` (Dark Charcoal).
    - Update button colors to be more vibrant against the light background.
    - Add subtle shadows for the "premium" feel.

### [MODIFY] [editor_window.py](file:///c:/OpenCode/MySnapshot/editor_window.py)
- **Toolbar Refactoring**: 
    - Move `QToolBar` from `QMainWindow.addToolBar` directly into the `QVBoxLayout` of the central widget. This ensures it is treated as a standard widget and is always visible within the window's layout.
    - **Styled Icons**: Add emoji prefixes (e.g., "🟦 Rect", "🖊️ Text") to buttons to make them immediately recognizable.
    - Set a minimum height for the toolbar.

### [MODIFY] [browser_window.py](file:///c:/OpenCode/MySnapshot/browser_window.py)
- **Preview Scaling**:
    - Increase the `preview_pane` minimum width to `450px`.
    - Increase the `preview_label` minimum height to `500px`.
    - Set `scaledContents = True` on the preview label or use a larger `QPixmap` scaling factor.

## Open Questions

> [!IMPORTANT]
> 1. **Light Mode**: Is a "Mac-style" light theme (White background, Blue accents) acceptable?
> 2. **Toolbar Position**: Should the editor toolbar stay at the top, or would you prefer it on the left? (Staying at top for now).

## Verification Plan

### Manual Verification
- **Editor Tool Check**: Open editor -> Verify tools (Rect, Text, etc.) are clearly visible at the top.
- **Browser Theme Check**: Open browser -> Verify background is light and text is readable.
- **Preview Check**: Click a thumbnail -> Verify the preview image is significantly larger than before.
