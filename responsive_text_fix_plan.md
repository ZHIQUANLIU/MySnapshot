# Button Scaling & Text Editing Implementation Plan

Goal: Enhance the responsiveness of toolbar buttons and make text annotations fully interactive and editable.

## User Review Required

> [!IMPORTANT]
> - **Text Editing**: Once a text label is added, you will be able to click on it to edit the content directly. Double-clicking will also trigger the editor mode.
> - **Aggressive Scaling**: Button font sizes will now react more noticeably to window resizing, filling the available button space better.

## Proposed Changes

### [MODIFY] [browser_window.py](file:///c:/OpenCode/MySnapshot/browser_window.py)
 - **ResponsiveButton Enhancement**:
    - Update the `resizeEvent` calculation. Instead of a narrow 10-15pt range, it will now use a more dynamic formula (`min(width/12, height*0.4)`) and a wider range (e.g., 8pt to 22pt).
 - **AnnotationScene Text Logic**:
    - Implement `Qt.TextEditorInteraction` flag for `QGraphicsTextItem`.
    - Add a logic to `mousePressEvent` or a separate `mouseDoubleClickEvent` to ensure clicked text items gain focus and become editable.
    - Set the text cursor to the end of the line when editing starts.

## Verification Plan

### Manual Verification
 - **Visual Test**: Drag the window corners and verify that the button labels (like "SAVE APPLY CHANGES") grow much larger and shrink much smaller than before.
 - **Annotation Test**: Select "Text", click on the canvas, and verify that you can immediately type "Hello World".
 - **Revision Test**: Click away, then double-click the "Hello World" text to modify it to "My Screenshot".
