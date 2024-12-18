import os
import sys

from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import Qt, QTimer, QDir, QSignalBlocker
from PySide6.QtGui import QCloseEvent, QIcon, QAction
from PySide6.QtWidgets import (QApplication, QLabel, QCalendarWidget, QFrame, QTreeView,
                             QTableWidget, QFileSystemModel, QPlainTextEdit, QToolBar,
                             QWidgetAction, QComboBox, QSizePolicy, QInputDialog)

import PySide6QtAds as QtAds

UI_FILE = os.path.join(os.path.dirname(__file__), 'mainwindow.ui')
MainWindowUI, MainWindowBase = loadUiType(UI_FILE)

class MainWindow(MainWindowUI, MainWindowBase):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.OpaqueSplitterResize, True)
        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.XmlCompressionEnabled, False)
        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.FocusHighlighting, True)
        # Enable AutoHide functionality
        QtAds.CDockManager.setAutoHideConfigFlags(QtAds.CDockManager.DefaultAutoHideConfig)
        QtAds.CDockManager.setAutoHideConfigFlag(QtAds.CDockManager.AutoHideShowOnMouseOver, True)
        self.dock_manager = QtAds.CDockManager(self)

        # Set central widget
        text_edit = QPlainTextEdit()
        text_edit.setPlaceholderText("This is the central editor. Enter your text here.")
        central_dock_widget = QtAds.CDockWidget("CentralWidget")
        central_dock_widget.setWidget(text_edit)
        central_dock_area = self.dock_manager.setCentralWidget(central_dock_widget)
        central_dock_area.setAllowedAreas(QtAds.DockWidgetArea.OuterDockAreas)

        # create other dock widgets
        table = QTableWidget()
        table.setColumnCount(3)
        table.setRowCount(10)
        table_dock_widget = QtAds.CDockWidget("Table 1")
        table_dock_widget.setWidget(table)
        table_dock_widget.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromDockWidget)
        table_dock_widget.resize(250, 150)
        table_dock_widget.setMinimumSize(200, 150)
         # Add Table 1 as auto-hide widget on the left side
        self.dock_manager.addAutoHideDockWidget(QtAds.SideBarLeft, table_dock_widget)
        self.menuView.addAction(table_dock_widget.toggleViewAction())

        table = QTableWidget()
        table.setColumnCount(5)
        table.setRowCount(1020)
        table_dock_widget = QtAds.CDockWidget("Table 2")
        table_dock_widget.setWidget(table)
        table_dock_widget.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromDockWidget)
        table_dock_widget.resize(250, 150)
        table_dock_widget.setMinimumSize(200, 150)
        # Add Table 2 as auto-hide widget on the bottom
        self.dock_manager.addAutoHideDockWidget(QtAds.SideBarBottom, table_dock_widget)
        self.menuView.addAction(table_dock_widget.toggleViewAction())

        properties_table = QTableWidget()
        properties_table.setColumnCount(3)
        properties_table.setRowCount(10)
        properties_dock_widget = QtAds.CDockWidget("Properties")
        properties_dock_widget.setWidget(properties_table)
        properties_dock_widget.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromDockWidget)
        properties_dock_widget.resize(250, 150)
        properties_dock_widget.setMinimumSize(200, 150)
        # Add Properties as auto-hide widget on the right side
        self.dock_manager.addAutoHideDockWidget(QtAds.SideBarRight, properties_dock_widget)
        self.menuView.addAction(properties_dock_widget.toggleViewAction())

        self.create_perspective_ui()

    def create_perspective_ui(self):
        save_perspective_action = QAction("Create Perspective", self)
        save_perspective_action.triggered.connect(self.save_perspective)
        perspective_list_action = QWidgetAction(self)
        self.perspective_combobox = QComboBox(self)
        self.perspective_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.perspective_combobox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.perspective_combobox.textActivated.connect(self.dock_manager.openPerspective)
        perspective_list_action.setDefaultWidget(self.perspective_combobox)
        self.toolBar.addSeparator()
        self.toolBar.addAction(perspective_list_action)
        self.toolBar.addAction(save_perspective_action)

    def save_perspective(self):
        perspective_name, ok = QInputDialog.getText(self, "Save Perspective", "Enter Unique name:")
        if not ok or not perspective_name:
            return

        self.dock_manager.addPerspective(perspective_name)
        blocker = QSignalBlocker(self.perspective_combobox)
        self.perspective_combobox.clear()
        self.perspective_combobox.addItems(self.dock_manager.perspectiveNames())
        self.perspective_combobox.setCurrentText(perspective_name)

    def closeEvent(self, event: QCloseEvent):
        self.dock_manager.deleteLater()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()
    app.exec()
