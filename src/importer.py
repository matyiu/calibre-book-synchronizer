import os
import hashlib

from .book import LinkedBook
from .db import FolderCollection, SyncedBookCollection, BookCollection
from calibre.ebooks.metadata.meta import get_metadata
from calibre.gui2.ui import MainWindow
from .metadata import ImporterMetadata
try:
    from calibre.db.legacy import LibraryDatabase
except ImportError:
    from calibre.db.backend import DB as LibraryDatabase

class Importer:
    def __init__(self, library_id: str, gui: MainWindow):
        self.library_id = library_id
        self.gui: MainWindow = gui
        self.folders_db = FolderCollection(library_id)
        self.synced_db = SyncedBookCollection(library_id)
        self.library_path = self.gui.current_db.library_path
        self.db: LibraryDatabase = self.gui.current_db
        self.book_db = BookCollection(self.db)

    def _get_book_hash(self, file_path: str) -> str:
        h = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)

        return h.hexdigest()

    def _get_book_id(self, file_path: str, metadata: ImporterMetadata) -> str:
        title = metadata.title
        author = metadata.author
        base = os.path.splitext(os.path.basename(file_path))[0]

        return f"{title}_{author}_{base}"

    def _extract_metadata(self, file_path: str) -> ImporterMetadata:
        extension = os.path.splitext(file_path)[1]

        try:
            with open(file_path, 'rb') as f:
                mi = get_metadata(f, extension)
                print(f"[SymlinkImporter] Metadatos extraídos de {file_path}: {mi}")

            title = getattr(mi, 'title', None)
            author = getattr(mi, 'authors', None)

            if not title:
                title = os.path.splitext(os.path.basename(file_path))[0]
            if not author:
                author = ['Desconocido']
            if not isinstance(author, str):
                author = author[0]

            return ImporterMetadata(title, author, extension)

        except Exception as e:
            print(f"[SymlinkImporter] Error extrayendo metadatos de {file_path}: {e}")
            return ImporterMetadata(os.path.splitext(os.path.basename(file_path))[0], 'Desconocido', extension)

    def sync_books(self):
        folders = self.folders_db.get_folders()
        exts = ('.epub', '.pdf')
        found_books = []

        for folder in folders:
            for root, dirs, files in os.walk(folder['path']):
                for file in files:
                    if file.lower().endswith(exts):
                        found_books.append(os.path.join(root, file))

        already_synced = 0
        new_books = 0
        not_able_to_sync = 0

        synced_books = self.synced_db.get_books()
        synced_hashes = set(b['hash'] for b in synced_books)

        for file_path in found_books:
            try:
                file_hash = self._get_book_hash(file_path)
            except Exception as e:
                print(f"[SymlinkImporter] Error calculando hash de {file_path}: {e}")
                not_able_to_sync += 1
                continue

            if file_hash in synced_hashes:
                already_synced += 1
                print(f"[SymlinkImporter] Libro ya sincronizado: {file_path}")
                continue

            # Extraer metadatos
            book = LinkedBook(file_path, self._extract_metadata(file_path), self.library_path)

            try:
                calibre_id = self.db.add_books([book.get_file_path()], [book.format()], [book.get_calibre_metadata()], add_duplicates=False)
                print(f"[SymlinkImporter] add_books({book.get_calibre_metadata()}) -> {calibre_id}")
            except Exception as e:
                print(f"[SymlinkImporter] Error añadiendo libro a Calibre: {e}")
                continue

            # Registrar en SyncedBookCollection
            book_id = self._get_book_id(file_path, book.get_metadata())
            self.synced_db.add_book({
                'folder': os.path.dirname(file_path),
                'file_path': file_path,
                'calibre_id': calibre_id,
                'id': book_id,
                'hash': file_hash
            })
            new_books += 1
        return {
            'total': len(found_books),
            'already_synced': already_synced,
            'new_books': new_books
        } 