"""Read data MDI child window."""

from PySide6.QtCore import Signal

from mjlog.gui.ui.read_data_window_ui import Ui_ReadDataWindow


class ReadDataWindow(Ui_ReadDataWindow):
    """MDI child window for reading data from database."""

    data_loaded = Signal(list)

    def __init__(self, parent=None):
        from PySide6.QtWidgets import QWidget

        self.widget = QWidget(parent)
        super().__init__()
        self.setupUi(self.widget)

        self.readButton.clicked.connect(self.on_read_clicked)
        self.data_loaded.connect(self.on_data_loaded)

    def on_read_clicked(self):
        """Handle Read local data button click."""
        self.statusLabel.setText("Loading...")
        try:
            from mjlog.db.models import Entry
            from mjlog.db.session import get_session

            session = get_session()
            try:
                entries = session.query(Entry).all()
                self.data_loaded.emit(entries)
            finally:
                session.close()
        except Exception as e:
            self.statusLabel.setText(f"Error: {e}")

    def on_data_loaded(self, entries):
        """Handle data loaded signal."""
        count = len(entries)
        self.statusLabel.setText(f"Loaded {count} entries")
        if count > 0:
            for entry in entries:
                print(f"  - {entry}")

    def show(self):
        """Show the widget."""
        self.widget.show()
