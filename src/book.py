from .metadata import ImporterMetadata

class LinkedBook():
    def __init__(self, file_path: str, metadata: ImporterMetadata, library_path: str):
        self.file_path = file_path
        self.metadata = metadata
        self.library_path = library_path

    def get_file_path(self) -> str:
        return self.file_path
    
    def title(self) -> str:
        return self.metadata.title
    
    def extension(self) -> str:
        return self.metadata.extension
    
    def format(self) -> str:
        return self.extension().lstrip('.')
    
    def author(self) -> str:
        return self.metadata.author
    
    def get_calibre_metadata(self) -> dict:
        return self.metadata.to_calibre_metadata()
    
    def get_metadata(self) -> ImporterMetadata:
        return self.metadata
        
        