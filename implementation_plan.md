# MySnapshot - Screen Capture & Management Tool

MySnapshot is a modern desktop application that allows users to capture their screen (full or selective area), organize captures into collections, and browse them using a premium, Explorer-like interface.

## User Review Required

> [!IMPORTANT]
> **Privacy Permissions**: On Windows, global shortcuts and screen recording usually work out of the box, but some antivirus or security settings might flag the tool.
> **Storage Path**: The app will default to a `MySnapshot` folder in the user's Pictures directory. Users can change this in settings (to be added later).

## Proposed Changes

### Core Architecture (Main Process)

#### [NEW] `main/index.js`
- Initialize Electron app and window management.
- Register global hotkeys.
- Create System Tray icon.
- Handle IPC for saving, managing collections, and **opening the Editor window**.

#### [NEW] `main/preload.js`
- Securely expose necessary APIs (FS, IPC, Clipboard).

### Image Editor (Renderer - React + Konva)

#### [NEW] `renderer/editor/EditorApp.jsx`
- Opens immediately after a capture or from the Gallery.
- **Canvas Annotation**: Using `react-konva`.
- **Tools**:
    - **Shape**: Rectangle (border only or solid "Cover").
    - **Highlight**: Semi-transparent yellow/color overlay.
    - **Text**: Add text with customizable color and font size.
    - **Crop**: Real-time cropping of the current image.
- **Action Bar**: Save, Copy to Clipboard, Close.

### Dashboard & Browser (Renderer - React)

#### [NEW] `renderer/dashboard/index.html` & `renderer/dashboard/App.jsx`
- The main "Explorer" interface.
- **Collection Sidebar**: List folders/collections.
- **Gallery Grid**: Display captured PNGs with hover effects.
- **Preview Pane**: Collapsible right panel for detailed viewing and "Save As" actions.

#### [NEW] `renderer/styles/` (Vanilla CSS)
- **Design System**: Define a professional dark-themed palette using HSL.
- **Glassmorphism**: Use `backdrop-filter: blur()` for the sidebar and modals.
- **Layout**: CSS Grid for the gallery and Flexbox for the sidebar.

## Open Questions

> [!IMPORTANT]
> 1. **Default Hotkeys**: Are `Alt+Shift+S` (Area) and `Alt+Shift+F` (Full) acceptable, or would you prefer something else?
> 2. **Multi-monitor**: Should the capture selection span all monitors or just the active one? (Planning for all monitors).

## Verification Plan

### Automated Tests
- Run `npm test` (if unit tests are added).
- Manual verification of IPC calls for file existence and saving logic.

### Manual Verification
- **Capture Flow**: Trigger hotkey -> Select area -> Verify PNG exists in correct collection folder.
- **Tray Flow**: Minimize to tray -> Right click -> Verify capture starts.
- **Explorer Flow**: Browse collections -> Switch views -> Preview image -> Save As to external location.
