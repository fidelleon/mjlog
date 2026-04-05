"""MDI main window for MJlog."""

from PySide6.QtWidgets import QMainWindow

from mjlog.gui.ui.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    """Main MDI window for MJlog application."""

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionInitializeDatabase.triggered.connect(
            self.on_init_db_requested
        )

    def on_init_db_requested(self):
        """Handle Initialize database action."""
        from mjlog.gui.windows.read_data_window import ReadDataWindow

        child_window = ReadDataWindow(self.ui.mdiArea)
        self.ui.mdiArea.addSubWindow(child_window)
        child_window.show()
