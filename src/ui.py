from calibre.gui2.actions import InterfaceAction
from calibre.gui2 import error_dialog, info_dialog
import os
from calibre_plugins.symlink_importer.db import FolderCollection

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

    def create_menu(self):
        from PyQt5.QtWidgets import QMenu, QAction
        menu = QMenu()
        config_action = QAction('Configuración', self.gui)
        config_action.triggered.connect(self.open_config)
        menu.addAction(config_action)
        return menu

    def open_config(self):
        info_dialog(self.gui, 'Configuración', 'Aquí irá la configuración del plugin.', show=True)

    def apply_action(self):
        library_id = os.path.basename(self.gui.current_db.library_path)
        folders_db = FolderCollection(library_id)
        folders = folders_db.get_folders()
        if not folders:
            error_dialog(
                self.gui,
                'Sin carpetas configuradas',
                'No tienes carpetas configuradas para sincronizar. Ve a configuración para añadir una.',
                show=True
            )
            return
        # Placeholder de sincronización
        info_dialog(
            self.gui,
            'Sincronización',
            f'Se iniciaría la sincronización de {len(folders)} carpeta(s).',
            show=True
        )

    def apply_settings(self):
        pass  # Placeholder para compatibilidad futura
