# Integrated Browser & Editor Plan

Goal: Provide the annotation tools directly within the Browser's preview pane, alongside the Zoom controls.

## User Review Required

> [!IMPORTANT]
> The separate "Editor" window will be removed. All editing will now happen in the Browser's right-hand pane. 
> When you capture a screen, the Browser will automatically open and select the new capture for immediate editing.

## Proposed Changes

### [MODIFY] [browser_window.py](file:///c:/OpenCode/MySnapshot/browser_window.py)
- **UI Redesign**: Add a `Toolbox` widget (Rectangle, Highlight, Cover, Arrow, Text) to the same horizontal row as the Zoom buttons.
- **Canvas Implementation**: Replace the static `QLabel` with a `QGraphicsView` and `AnnotationScene` (ported from `editor_window.py`).
- **State Management**: Track the currently active tool and color within `BrowserWindow`.
- **Save Edits**: Add a specific "`💾 Apply Edits`" button to finalize changes on the disk.

### [MODIFY] [main.py](file:///c:/OpenCode/MySnapshot/main.py)
- **Capture Workflow**: Update `handle_capture` to simply open the Browser and trigger a "Selection" of the latest file.
- **Cleanup**: Remove redundant `open_editor` and `ImageEditor` code.

## Verification Plan

### Manual Verification
- **Capture -> Edit**: Capture a screen -> Browser opens -> Draw a rectangle -> Save -> Verify thumbnail updates.
- **History Edit**: Select an old image -> Zoom in 200% -> Add text -> Save.
- **Tools**: Ensure all tools (Rect, High, Cover, Arrow, Text) work as expected on the canvas.
