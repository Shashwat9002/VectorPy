"""PySide6 desktop interface for Cyber City."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QEasingCurve, QMimeData, QPoint, QPropertyAnimation, Qt, Signal
from PySide6.QtGui import QAction, QColor, QDrag, QFont, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from database import CityStorage
from models.city import BUILDING_PROFILES, BuildingType, CityMap
from simulation import SimulationEngine

BUILDING_COLORS: dict[BuildingType, str] = {
    BuildingType.FIREWALL_TOWER: "#ff6b6b",
    BuildingType.TRAINING_ACADEMY: "#4ecdc4",
    BuildingType.DATA_LIBRARY: "#45b7d1",
    BuildingType.BACKUP_STATION: "#96ceb4",
    BuildingType.INCIDENT_HQ: "#feca57",
    BuildingType.RESIDENTIAL_BLOCK: "#a29bfe",
}


class BuildingList(QListWidget):
    """Palette of draggable building types."""

    def __init__(self) -> None:
        super().__init__()
        self.setDragEnabled(True)
        self.setObjectName("buildingPalette")
        self.setMinimumWidth(250)
        for building_type in BuildingType:
            profile = BUILDING_PROFILES[building_type]
            item = QListWidgetItem(
                f"{building_type.value}\n"
                f"Defense {profile['defense']} • Awareness {profile['awareness']} • "
                f"Resilience {profile['resilience']}"
            )
            item.setData(Qt.ItemDataRole.UserRole, building_type.value)
            item.setToolTip(str(profile["description"]))
            self.addItem(item)

    def startDrag(self, supported_actions: Qt.DropActions) -> None:
        item = self.currentItem()
        if item is None:
            return
        mime_data = QMimeData()
        mime_data.setText(str(item.data(Qt.ItemDataRole.UserRole)))
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec(supported_actions)


class CityTile(QFrame):
    """Single grid cell that accepts dropped buildings."""

    buildingDropped = Signal(int, int, str)

    def __init__(self, row: int, column: int) -> None:
        super().__init__()
        self.row = row
        self.column = column
        self.building_type: BuildingType | None = None
        self.risk_level = 0
        self.setAcceptDrops(True)
        self.setMinimumSize(86, 72)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.label = QLabel("Empty", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.addWidget(self.label)
        self._refresh_style()

    def dragEnterEvent(self, event) -> None:  # type: ignore[no-untyped-def]
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event) -> None:  # type: ignore[no-untyped-def]
        self.buildingDropped.emit(self.row, self.column, event.mimeData().text())
        event.acceptProposedAction()

    def set_building(self, building_type: BuildingType | None) -> None:
        self.building_type = building_type
        self.label.setText("Empty" if building_type is None else building_type.value.replace(" ", "\n"))
        self._refresh_style()

    def set_risk_level(self, risk_level: int) -> None:
        self.risk_level = max(0, min(100, risk_level))
        self._refresh_style()

    def flash(self) -> None:
        animation = QPropertyAnimation(self, b"pos", self)
        start = self.pos()
        animation.setStartValue(start)
        animation.setKeyValueAt(0.25, start + QPoint(6, 0))
        animation.setKeyValueAt(0.5, start + QPoint(-6, 0))
        animation.setEndValue(start)
        animation.setDuration(420)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def paintEvent(self, event) -> None:  # type: ignore[no-untyped-def]
        super().paintEvent(event)
        if self.risk_level > 0:
            painter = QPainter(self)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(255, 82, 82, min(170, 30 + self.risk_level)))
            painter.drawRect(0, self.height() - 7, int(self.width() * self.risk_level / 100), 7)

    def _refresh_style(self) -> None:
        if self.building_type is None:
            color = "#172033"
            border = "#26344f"
        else:
            color = BUILDING_COLORS[self.building_type]
            border = "#dff9fb"
        self.setStyleSheet(
            f"CityTile {{ background: {color}; border: 1px solid {border}; border-radius: 10px; }}"
            "QLabel { color: #f8fbff; font-weight: 700; }"
        )
        self.update()


class CyberCityWindow(QMainWindow):
    """Main application window."""

    def __init__(self, storage: CityStorage | None = None) -> None:
        super().__init__()
        self.city = CityMap()
        self.storage = storage or CityStorage(Path.home() / ".cyber_city" / "cities.db")
        self.engine = SimulationEngine()
        self.tiles: dict[tuple[int, int], CityTile] = {}
        self.risk_progress = QProgressBar()
        self.status_log = QTextEdit()
        self.save_selector = QComboBox()
        self.setWindowTitle("Cyber City: A Digital Defense Simulator")
        self.resize(1240, 780)
        self._build_actions()
        self._build_layout()
        self._apply_theme()
        self.refresh_city()
        self._append_log("Welcome to Cyber City. Drag civic defense buildings onto the grid.")

    def place_building(self, row: int, column: int, building_name: str) -> None:
        building_type = BuildingType(building_name)
        self.city.place_building(building_type, row, column)
        self.refresh_city()
        self._append_log(f"Placed {building_type.value} at district {row + 1}-{column + 1}.")

    def run_incident(self) -> None:
        report = self.engine.generate_incident(self.city)
        projected_risk = self.engine.projected_risk_after_incident(self.city, report)
        target_tile = self._find_tile_for_target(report.target)
        if target_tile is not None:
            target_tile.flash()
        self._append_log(
            f"Fictional {report.actor} story event targeted {report.target}. "
            f"Risk pressure +{report.risk_delta}. Lesson: {report.lesson}"
        )
        self.risk_progress.setValue(projected_risk)
        self._update_tile_risk(projected_risk)

    def save_city(self) -> None:
        name, accepted = QInputDialog.getText(self, "Save City", "City name:", text="Learning District")
        if not accepted or not name.strip():
            return
        self.storage.save_city(name.strip(), self.city)
        self._refresh_saves()
        self._append_log(f"Saved city layout as {name.strip()}.")

    def load_city(self) -> None:
        name = self.save_selector.currentText()
        if not name:
            QMessageBox.information(self, "Load City", "No saved city is available yet.")
            return
        self.city = self.storage.load_city(name)
        self.refresh_city()
        self._append_log(f"Loaded city layout {name}.")

    def clear_city(self) -> None:
        self.city = CityMap(rows=self.city.rows, columns=self.city.columns)
        self.refresh_city()
        self._append_log("Cleared the city grid for a new design.")

    def refresh_city(self) -> None:
        for tile in self.tiles.values():
            tile.set_building(None)
        for building in self.city.buildings:
            self.tiles[(building.row, building.column)].set_building(building.building_type)
        scores = self.city.city_score()
        self.risk_progress.setValue(scores["risk"])
        self._update_tile_risk(scores["risk"])
        self.score_label.setText(
            f"Defense {scores['defense']}  •  Awareness {scores['awareness']}  •  "
            f"Resilience {scores['resilience']}"
        )
        self._refresh_saves()

    def _build_actions(self) -> None:
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_city)
        load_action = QAction("Load", self)
        load_action.triggered.connect(self.load_city)
        clear_action = QAction("New City", self)
        clear_action.triggered.connect(self.clear_city)
        toolbar = self.addToolBar("City")
        toolbar.addAction(save_action)
        toolbar.addAction(load_action)
        toolbar.addAction(clear_action)

    def _build_layout(self) -> None:
        root = QWidget()
        main_layout = QHBoxLayout(root)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        title = QLabel("Building Palette")
        title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        left_layout.addWidget(title)
        left_layout.addWidget(BuildingList())
        simulate_button = QPushButton("Run Fictional Incident")
        simulate_button.clicked.connect(self.run_incident)
        left_layout.addWidget(simulate_button)
        self.save_selector.currentIndexChanged.connect(lambda _: None)
        load_button = QPushButton("Load Selected City")
        load_button.clicked.connect(self.load_city)
        left_layout.addWidget(self.save_selector)
        left_layout.addWidget(load_button)
        splitter.addWidget(left_panel)

        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        heading = QLabel("Cyber City Planning Grid")
        heading.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        center_layout.addWidget(heading)
        grid = QGridLayout()
        grid.setSpacing(8)
        for row in range(self.city.rows):
            for column in range(self.city.columns):
                tile = CityTile(row, column)
                tile.buildingDropped.connect(self.place_building)
                self.tiles[(row, column)] = tile
                grid.addWidget(tile, row, column)
        center_layout.addLayout(grid)
        splitter.addWidget(center_panel)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.score_label = QLabel()
        self.score_label.setWordWrap(True)
        right_layout.addWidget(QLabel("City Readiness"))
        right_layout.addWidget(self.score_label)
        right_layout.addWidget(QLabel("Risk Visualization"))
        self.risk_progress.setRange(0, 100)
        self.risk_progress.setFormat("%p% fictional risk")
        right_layout.addWidget(self.risk_progress)
        right_layout.addWidget(QLabel("Education Log"))
        self.status_log.setReadOnly(True)
        right_layout.addWidget(self.status_log)
        splitter.addWidget(right_panel)
        splitter.setSizes([260, 720, 300])
        self.setCentralWidget(root)

    def _apply_theme(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow, QWidget { background: #0f172a; color: #e2e8f0; font-family: Inter, Arial; }
            QListWidget, QTextEdit, QComboBox { background: #111827; border: 1px solid #334155; border-radius: 8px; padding: 8px; }
            QPushButton { background: #2563eb; color: white; border: 0; border-radius: 8px; padding: 10px; font-weight: 700; }
            QPushButton:hover { background: #1d4ed8; }
            QProgressBar { border: 1px solid #334155; border-radius: 8px; text-align: center; background: #111827; height: 24px; }
            QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #22c55e, stop:0.55 #facc15, stop:1 #ef4444); border-radius: 8px; }
            """
        )

    def _append_log(self, message: str) -> None:
        self.status_log.append(f"• {message}")

    def _refresh_saves(self) -> None:
        current = self.save_selector.currentText()
        self.save_selector.blockSignals(True)
        self.save_selector.clear()
        self.save_selector.addItems(self.storage.list_cities())
        if current:
            index = self.save_selector.findText(current)
            if index >= 0:
                self.save_selector.setCurrentIndex(index)
        self.save_selector.blockSignals(False)

    def _update_tile_risk(self, risk: int) -> None:
        for tile in self.tiles.values():
            tile.set_risk_level(risk if tile.building_type is None else max(0, risk - 25))

    def _find_tile_for_target(self, target: str) -> CityTile | None:
        for building in self.city.buildings:
            if building.display_name == target:
                return self.tiles[(building.row, building.column)]
        return next(iter(self.tiles.values()), None)


def launch() -> int:
    """Start the Qt event loop."""

    application = QApplication.instance() or QApplication([])
    window = CyberCityWindow()
    window.show()
    return application.exec()
