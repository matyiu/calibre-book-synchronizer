from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QFileDialog, QWidget, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt
from .db import FolderCollection
import datetime

INTRO_TEXT = (
    "Este plugin permite sincronizar libros desde carpetas externas."
    "Ningún archivo será movido, eliminado ni copiado en la biblioteca."
    "Solo se crearán enlaces simbólicos a los archivos originales."
)

class ConfigDialog(QDialog):
    def __init__(self, library_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración de Sincronizar carpetas")
        self.resize(600, 400)
        self.library_id = library_id
        self.folders_db = FolderCollection(library_id)
        self.init_ui()
        self.load_folders()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(INTRO_TEXT))

        # Tabla de carpetas
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Carpeta", "Acciones"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Botón añadir carpeta
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Añadir nueva carpeta")
        self.add_btn.clicked.connect(self.add_folder)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Botón cerrar
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def load_folders(self):
        self.table.setRowCount(0)
        folders = self.folders_db.get_folders()
        for folder in folders:
            self.add_folder_row(folder["path"])

    def add_folder_row(self, path):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(path))
        btn = QPushButton("Eliminar")
        btn.clicked.connect(lambda _, p=path: self.remove_folder(p))
        w = QWidget()
        l = QHBoxLayout(w)
        l.addWidget(btn)
        l.setAlignment(Qt.AlignCenter)
        l.setContentsMargins(0, 0, 0, 0)
        self.table.setCellWidget(row, 1, w)

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecciona una carpeta para sincronizar")
        if folder:
            if any(folder == self.table.item(row, 0).text() for row in range(self.table.rowCount())):
                QMessageBox.warning(self, "Carpeta duplicada", "Esta carpeta ya está en la lista.")
                return
            now = datetime.datetime.now().isoformat()
            self.folders_db.add_folder({
                "path": folder,
                "added_at": now,
                "options": {"include_subfolders": True}
            })
            self.add_folder_row(folder)

    def remove_folder(self, path):
        self.folders_db.remove_folder(path)
        self.load_folders() 