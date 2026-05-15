from enum import StrEnum

class FileSystemItemType(StrEnum):
    """
    Enum representing the type of a file system item.
    """
    FOLDER = "folder"
    FILE = "file"
