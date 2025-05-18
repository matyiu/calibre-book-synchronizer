import os
import hashlib
from calibre_plugins.symlink_importer.db import FolderCollection, SyncedBookCollection
from calibre.ebooks.metadata.meta import get_metadata
from calibre.ebooks.metadata.book.base import Metadata
from calibre.gui2.ui import MainWindow
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

    def _get_book_hash(self, file_path):
        # Hash SHA256 del contenido del archivo
        h = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()

    def _get_book_id(self, file_path, metadata):
        # ID único: título + autor + nombre de archivo
        title = metadata.get('title', 'Desconocido')
        author = metadata.get('authors', ['Desconocido'])[0]
        base = os.path.splitext(os.path.basename(file_path))[0]
        return f"{title}_{author}_{base}"

    def _get_metadata(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                format = os.path.splitext(file_path)[1].lower()
                mi = get_metadata(f, format)
            title = getattr(mi, 'title', None)
            authors = getattr(mi, 'authors', None)
            if not title:
                title = os.path.splitext(os.path.basename(file_path))[0]
            if not authors:
                authors = ['Desconocido']
            if isinstance(authors, str):
                authors = [authors]
            print(f"[SymlinkImporter] Metadatos extraídos de {file_path}: Título='{title}', Autor(es)={authors}")
            # Devuelve también el objeto Metadata para add_books
            return {
                'title': title,
                'authors': authors,
                'mi': mi
            }
        except Exception as e:
            print(f"[SymlinkImporter] Error extrayendo metadatos de {file_path}: {e}")
            # Usa el nombre de archivo como título si todo falla
            mi = Metadata(os.path.splitext(os.path.basename(file_path))[0], ['Desconocido'])
            return {
                'title': os.path.splitext(os.path.basename(file_path))[0],
                'authors': ['Desconocido'],
                'mi': mi
            }

    def _symlink_path(self, metadata, ext):
        author = metadata['authors'][0] if metadata['authors'] else 'Desconocido'
        title = metadata['title'] or 'Desconocido'
        author_dir = author.replace('/', '_')
        title_dir = title.replace('/', '_')
        dest_dir = os.path.join(self.library_path, author_dir, title_dir)
        os.makedirs(dest_dir, exist_ok=True)
        filename = f"{title} - {author}{ext}"
        return os.path.join(dest_dir, filename)

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
        synced_books = self.synced_db.get_books()
        synced_hashes = set(b['hash'] for b in synced_books)
        for file_path in found_books:
            try:
                file_hash = self._get_book_hash(file_path)
            except Exception as e:
                print(f"[SymlinkImporter] Error calculando hash de {file_path}: {e}")
                continue
            if file_hash in synced_hashes:
                already_synced += 1
                continue
            # Extraer metadatos
            metadata = self._get_metadata(file_path)
            ext = os.path.splitext(file_path)[1]
            symlink_path = self._symlink_path(metadata, ext)
            mi = metadata['mi']
            # Crear symlink si no existe
            if not os.path.exists(symlink_path):
                try:
                    os.symlink(file_path, symlink_path)
                    print(f"[SymlinkImporter] Symlink creado: {symlink_path} -> {file_path}")
                except FileExistsError:
                    print(f"[SymlinkImporter] Symlink ya existe: {symlink_path}")
                except Exception as e:
                    print(f"[SymlinkImporter] Error creando symlink: {e}")
            # Añadir a Calibre usando la API
            try:
                ids = self.db.add_books([symlink_path], (ext), [mi], add_duplicates=False)
                print(f"[SymlinkImporter] add_books({symlink_path}, {ext}, {mi}) -> {ids}")
                calibre_id = str(ids[0]) if ids else ''
            except Exception as e:
                print(f"[SymlinkImporter] Error añadiendo libro a Calibre: {e}")
                calibre_id = ''
            # Registrar en SyncedBookCollection
            book_id = self._get_book_id(file_path, metadata)
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