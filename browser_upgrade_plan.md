# Browser Upgrade: List View & Deletion

Enhancing the image browser to support a professional list view and full management of captures and collections.

## Proposed Changes

### [MODIFY] [utils.py](file:///c:/OpenCode/MySnapshot/utils.py)
- Add `delete_image(filename)`: Safely remove a snapshot from the current collection.
- Add `delete_collection(name)`: Remove an entire collection folder and its contents.
- Handle edge cases (e.g., deleting the currently active collection).

### [MODIFY] [browser_window.py](file:///c:/OpenCode/MySnapshot/browser_window.py)
- **UI Rewrite**: Replace the rigid grid layout with a `QListWidget`.
- **List View**: Display items with a small thumbnail, filename, and metadata (date/size).
- **Image Deletion**: 
    - Add a "Delete" button in the Preview Pane.
    - Add a confirmation dialog before deletion.
- **Collection Deletion**:
    - Add a right-click context menu to the Sidebar collections.
    - Allow users to delete a collection (with a warning).

## Open Questions

> [!IMPORTANT]
> 1. **Current Collection Deletion**: If you delete the currently active collection, should I automatically switch to the "Default" collection?
> 2. **Trash vs Permanent**: Should deletions be permanent (`os.remove`) or moved to the Recycle Bin (requires additional libraries like `send2trash`)? I recommend permanent for simplicity, but please confirm.

## Verification Plan

### Manual Verification
- **List View**: Verify that capturing an image adds a new item to the list.
- **Delete Image**: Delete an image -> Verify it disappears from UI and disk.
- **Delete Collection**: Right-click sidebar -> Delete -> Verify folder and UI update.
- **Switching**: Switch collections -> Verify list updates correctly.
