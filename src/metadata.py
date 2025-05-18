from calibre.ebooks.metadata.book.base import Metadata

class ImporterMetadata():
    def __init__(self, title: str, author: str, extension: str, path: str | None = None):
        self.title = title
        self.author = author
        self.extension = extension
        self.path = path

    def to_calibre_metadata(self) -> Metadata:
        return Metadata(self.title, [self.author])
