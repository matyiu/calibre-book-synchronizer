__license__ = "GPLv3"
__version__ = "1.0.0"
__author__ = "Jefferson Valle"

from calibre.customize import InterfaceActionBase

class SymlinkImporterPlugin(InterfaceActionBase):
    name = 'Symlink Importer'
    description = 'This Calibre plugin allows users to select a folder as a book source. Books are not moved or deleted upon import, and any changes in the original folder are synced with the Calibre Library.'
    supported_platforms = ['linux']
    author = 'Jefferson Valle'
    version = (1, 0, 0)
    minimum_calibre_version = (0, 8, 0)
    actual_plugin = 'calibre_plugins.symlink_importer.ui:SymlinkImporterUI'