from calibre.library import db
from calibre.ebooks.metadata.meta import get_metadata
import os
from PyQt5.QtWidgets import QDialog

class SymlinkImporter(QDialog):
    name = 'SymlinkImporter'
    action_spec = ('SymlinkImporter', None)