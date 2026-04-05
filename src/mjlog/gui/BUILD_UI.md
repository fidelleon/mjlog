# Rebuilding UI Files from Qt Designer

This directory contains Qt Designer `.ui` files that define the GUI layout. These are compiled to Python using `pyside6-uic`.

## Files

- `main_window.ui` → `main_window_ui.py` (MainWindow with menu bar and MDI area)
- `read_data_window.ui` → `read_data_window_ui.py` (MDI child with button and status label)

## Editing UI Files

### Option 1: Using Qt Designer (Recommended)
```bash
cd src/mjlog/gui/ui/
pyside6-designer main_window.ui &
```

This opens a visual editor where you can:
- Drag/drop widgets
- Configure layouts
- Set properties
- Connect signals (basic support)

### Option 2: Edit XML directly
The `.ui` files are valid XML. You can edit them in any text editor, but Qt Designer is more reliable.

## Compiling UI Files

After editing a `.ui` file, regenerate the Python code:

```bash
cd /path/to/MJlog
uv run pyside6-uic src/mjlog/gui/ui/main_window.ui -o src/mjlog/gui/ui/main_window_ui.py
uv run pyside6-uic src/mjlog/gui/ui/read_data_window.ui -o src/mjlog/gui/ui/read_data_window_ui.py
```

Or use the convenience script (if created):
```bash
./scripts/build_ui.sh
```

## Integration in Code

Python modules inherit from the auto-generated UI classes:

```python
from mjlog.gui.ui.main_window_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Now add signal/slot connections, custom logic, etc.
```

## Gitignore

Auto-generated `*_ui.py` files are ignored in `.gitignore`. Only commit `.ui` XML files.

## Design Workflow

1. Open `.ui` file in Qt Designer
2. Make visual changes
3. Save the `.ui` file
4. Compile: `pyside6-uic [file].ui -o [file]_ui.py`
5. Test in Python
6. Commit both `.ui` (source) and Python changes

## Notes

- **Never manually edit `*_ui.py` files** — they are auto-generated and will be overwritten
- Add custom logic in wrapper classes (e.g., `MainWindow`, `ReadDataWindow`)
- Keep the `.ui` files as the source of truth for layout
