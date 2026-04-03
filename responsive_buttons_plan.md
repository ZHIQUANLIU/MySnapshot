# Responsive Button Text Implementation Plan

Goal: Ensure that button text in the MySnapshot toolbar scales dynamically based on the button's width and height, providing a professional and adaptive user experience.

## User Review Required

> [!IMPORTANT]
> I will create a custom `ResponsiveButton` class that overrides the standard `resizeEvent`. This will ensure that as you resize the window, the labels like "Zoom In" and "Rect" will shrink or grow to fit perfectly.

## Proposed Changes

### [MODIFY] [browser_window.py](file:///c:/OpenCode/MySnapshot/browser_window.py)
 - **Custom Subclass**: Create `class ResponsiveButton(QPushButton)` within `browser_window.py`.
 - **Adaptive Logic**: Inside `resizeEvent`, calculate a dynamic `pointSize` based on `rect().width()` and `rect().height()`, with hardcoded min/max limits to prevent text from becoming too small or too large.
 - **Toolbar Overhaul**: Replace all `QPushButton` instances in the `_init_ui` toolbar with `ResponsiveButton`.
 - **Layout Dynamics**: Use `QSizePolicy.Expanding` for buttons to ensure they benefit from the shared space in the horizontal layout.

## Verification Plan

### Manual Verification
 - **Window Resizing**: Drag the edge of the MySnapshot window to make it very wide and very narrow.
 - **Text Readability**: Ensure that even at extreme scales, the text remains legible and centered within the button.
 - **Icon Alignment**: Check that the emojis/icons scale harmoniously with the text.
