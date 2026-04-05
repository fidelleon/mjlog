"""Countries viewer window for DXCC entities."""

from PySide6.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
    QCheckBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from mjlog.db.session import get_session
from mjlog.db.models import DXCCEntity
from mjlog.gui.settings import load_window_state, save_window_state


class CountriesWindow(QWidget):
    """MDI child window showing DXCC countries in a read-only table."""

    WINDOW_NAME = "CountriesWindow"

    def __init__(self, mdi_area):
        super().__init__()
        self.mdi_area = mdi_area
        self.setWindowTitle("DXCC Countries")
        self.setGeometry(0, 0, 900, 600)

        self.all_entities = []

        main_layout = QVBoxLayout(self)

        # Create filter controls
        filter_layout = QHBoxLayout()

        # special_use filter
        self.check_special_use = QCheckBox("Show Special Use")
        self.check_special_use.stateChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.check_special_use)

        # deleted filter
        self.check_deleted = QCheckBox("Show Deleted")
        self.check_deleted.stateChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.check_deleted)

        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        # Create read-only table
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSortingEnabled(True)

        # Set up columns
        columns = [
            "Prefix",
            "Entity Code",
            "Name",
            "DXCC Name",
            "Continent",
            "ITU Zone",
            "CQ Zone",
            "Latitude",
            "Longitude",
            "UTC Offset",
            "Special Use",
            "Deleted",
        ]
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        # Load all entities from database
        session = get_session()
        try:
            self.all_entities = session.query(DXCCEntity).order_by(
                DXCCEntity.entity_code
            ).all()
        finally:
            session.close()

        # Load saved state
        self.load_state()

        # Initial population
        self.apply_filters()

        # Auto-resize columns to content
        self.table.resizeColumnsToContents()

        main_layout.addWidget(self.table)

    def load_state(self) -> None:
        """Load checkboxes and column widths from saved state."""
        state = load_window_state(self.WINDOW_NAME)

        # Restore checkbox states
        show_special_use = state.get("show_special_use", True)
        show_deleted = state.get("show_deleted", False)
        self.check_special_use.setChecked(show_special_use)
        self.check_deleted.setChecked(show_deleted)

        # Restore column widths
        column_widths = state.get("column_widths", {})
        for col_idx, width in column_widths.items():
            try:
                self.table.setColumnWidth(int(col_idx), width)
            except (ValueError, IndexError):
                pass

    def closeEvent(self, event: QCloseEvent) -> None:
        """Save window state before closing."""
        state = {
            "show_special_use": self.check_special_use.isChecked(),
            "show_deleted": self.check_deleted.isChecked(),
            "column_widths": {
                str(i): self.table.columnWidth(i)
                for i in range(self.table.columnCount())
            },
        }
        save_window_state(self.WINDOW_NAME, state)
        super().closeEvent(event)

    def apply_filters(self):
        """Filter table based on checkbox selections."""
        show_special_use = self.check_special_use.isChecked()
        show_deleted = self.check_deleted.isChecked()

        filtered_entities = [
            e for e in self.all_entities
            if (show_special_use or not e.special_use) and
            (show_deleted or not e.deleted)
        ]

        self.table.setRowCount(len(filtered_entities))

        for row, entity in enumerate(filtered_entities):
            items = [
                str(entity.prefix),
                str(entity.entity_code),
                str(entity.name),
                str(entity.dxcc_name),
                str(entity.continent),
                str(entity.itu_zone if entity.itu_zone else ""),
                str(entity.cq_zone_id if entity.cq_zone_id else ""),
                str(entity.latitude if entity.latitude else ""),
                str(entity.longitude if entity.longitude else ""),
                str(entity.utc_offset if entity.utc_offset else ""),
                "Yes" if entity.special_use else "No",
                "Yes" if entity.deleted else "No",
            ]

            for col, item_text in enumerate(items):
                table_item = QTableWidgetItem(item_text)
                table_item.setFlags(
                    table_item.flags() & ~Qt.ItemIsEditable
                )
                self.table.setItem(row, col, table_item)
