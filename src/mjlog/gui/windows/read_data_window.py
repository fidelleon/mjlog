"""Read data MDI child window."""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

from mjlog.gui.ui.read_data_window_ui import Ui_ReadDataWindow


class ReadDataWindow(QWidget):
    """MDI child window for reading data from database."""

    data_loaded = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ReadDataWindow()
        self.ui.setupUi(self)

        self.ui.readButton.clicked.connect(self.on_read_clicked)
        self.data_loaded.connect(self.on_data_loaded)

    def on_read_clicked(self):
        """Handle Read local data button click."""
        self.ui.statusLabel.setText("Loading...")
        try:
            from mjlog.db.models import DXCCEntity
            from mjlog.db.session import get_session

            session = get_session()
            try:
                entities = session.query(DXCCEntity).all()
                self.data_loaded.emit(entities)
            finally:
                session.close()
        except Exception as e:
            self.ui.statusLabel.setText(f"Error: {e}")

    def on_data_loaded(self, entities):
        """Handle data loaded signal."""
        count = len(entities)
        self.ui.statusLabel.setText(f"Loaded {count} DXCC entities")
        if count > 0:
            for entity in entities:
                print(f"  - {entity}")
