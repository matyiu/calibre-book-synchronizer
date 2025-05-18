from calibre.gui2.actions import InterfaceAction
from calibre.gui2 import error_dialog, info_dialog
import os
from calibre.ebooks.metadata.meta import get_metadata
from calibre_plugins.symlink_importer.main import SymlinkImporter
from calibre_plugins.symlink_importer.db import FolderCollection
from calibre_plugins.symlink_importer.config_dialog import ConfigDialog
from calibre_plugins.symlink_importer.importer import Importer

class SymlinkImporterUI(InterfaceAction):
    name = 'SymlinkImporter'
    action_spec = (
        'Sincronizar carpetas',
        None,
        'Sincroniza libros desde carpetas externas mediante enlaces simbólicos.',
        None
    )

    def genesis(self):
        self.qaction.setMenu(self.create_menu())
        self.qaction.triggered.connect(self.apply_action)

    def create_menu(self):
        from PyQt5.QtWidgets import QMenu, QAction
        menu = QMenu()
        config_action = QAction('Configuración', self.gui)
        config_action.triggered.connect(self.open_config)
        menu.addAction(config_action)
        return menu

    def open_config(self):
        library_id = os.path.basename(self.gui.current_db.library_path)
        dlg = ConfigDialog(library_id, parent=self.gui)
        dlg.exec_()

    def apply_action(self):
        library_id = os.path.basename(self.gui.current_db.library_path)
        folders_db = FolderCollection(library_id)
        folders = folders_db.get_folders()
        if not folders:
            dlg = ConfigDialog(library_id, parent=self.gui)
            dlg.exec_()
            return

        importer = Importer(library_id, self.gui)
        summary = importer.sync_books()
        msg = (
            f"Total de libros encontrados: {summary['total']} | "
            f"Ya sincronizados: {summary['already_synced']} | "
            f"Nuevos a sincronizar: {summary['new_books']}"
        )
        self.gui.status_bar.showMessage(msg, 10000)

    def apply_settings(self):
        pass
