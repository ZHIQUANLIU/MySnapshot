# UI Modernization & Clarity Fix Plan

Goal: Provide a premium, clear, and professional UI for the MySnapshot Integrated Browser.

## User Review Required

> [!IMPORTANT]
> - All toolbar buttons will now include both an **Emoji/Icon AND Text** for maximum clarity (e.g., "➖ Zoom Out", "🎨 Select Color").
> - The toolbar will be visually structured into "View Controls" and "Annotation Tools".
> - Button styles will be updated to a more modern, flat design with smooth transitions.

## Proposed Changes

### [MODIFY] [styles.py](file:///c:/OpenCode/MySnapshot/styles.py)
- **Modern Tokens**: Update `QPushButton` to have a more premium feel with subtle borders and shadows.
- **List Styling**: Make the image list and sidebar look like a modern macOS/Windows 11 app (rounded corners, better spacing).
- **Tool-specific styling**: Create special classes for action buttons (Apply, Delete).

### [MODIFY] [browser_window.py](file:///c:/OpenCode/MySnapshot/browser_window.py)
- **Toolbar Labels**: Update all `QPushButton` creation codes to include descriptive text.
- **Layout Grouping**: reorganize the toolbar into logical sections:
    - **Group A (View)**: Zoom Out, Zoom In.
    - **Group B (Draw)**: Rect, High, Cover, Arrow, Text, Color.
    - **Group C (Actions)**: Apply Changes.
- **Visual Spacing**: Add margins between the GraphicsView and the toolbar.

## Verification Plan

### Manual Verification
- **Visual Audit**: Open the browser and check if all buttons have text labels.
- **Interaction Check**: Hover over toolbar buttons to ensure they respond smoothly.
- **Layout Check**: Verify the split between the sidebar and the canvas feels balanced.
