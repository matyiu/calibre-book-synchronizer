import json
from typing import List, Dict, Any

class FolderCollection:
    def __init__(self, library_id: str, path: str = "calibre-symlink-importer-folders.json"):
        self.library_id = library_id
        self.path = path
        self._data = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def get_folders(self) -> List[Dict[str, Any]]:
        for entry in self._data:
            if entry["id"] == self.library_id:
                return entry.get("folders", [])
        return []

    def add_folder(self, folder: Dict[str, Any]):
        for entry in self._data:
            if entry["id"] == self.library_id:
                entry.setdefault("folders", []).append(folder)
                self._save()
                return
        self._data.append({"id": self.library_id, "folders": [folder]})
        self._save()

    def remove_folder(self, folder_path: str):
        for entry in self._data:
            if entry["id"] == self.library_id:
                entry["folders"] = [f for f in entry.get("folders", []) if f["path"] != folder_path]
                self._save()
                return

    def set_folders(self, folders: List[Dict[str, Any]]):
        for entry in self._data:
            if entry["id"] == self.library_id:
                entry["folders"] = folders
                self._save()
                return
        self._data.append({"id": self.library_id, "folders": folders})
        self._save()

class SyncedBookCollection:
    def __init__(self, library_id: str, path: str = "calibre-symlink-importer-synced.json"):
        self.library_id = library_id
        self.path = path
        self._data = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def get_books(self) -> List[Dict[str, Any]]:
        for entry in self._data:
            if entry["id"] == self.library_id:
                return entry.get("books", [])
        return []

    def add_book(self, book: Dict[str, Any]):
        for entry in self._data:
            if entry["id"] == self.library_id:
                entry.setdefault("books", []).append(book)
                self._save()
                return
        self._data.append({"id": self.library_id, "books": [book]})
        self._save()

    def remove_book(self, book_id: str):
        for entry in self._data:
            if entry["id"] == self.library_id:
                entry["books"] = [b for b in entry.get("books", []) if b["id"] != book_id]
                self._save()
                return

    def set_books(self, books: List[Dict[str, Any]]):
        for entry in self._data:
            if entry["id"] == self.library_id:
                entry["books"] = books
                self._save()
                return
        self._data.append({"id": self.library_id, "books": books})
        self._save() 