class FileOperationError(Exception):
    """Raised when a file operation fails."""

    def __init__(self, result: str):
        super().__init__(f"File Operation Error: {result}")


class FileMoveCancelledError(FileOperationError):
    """Raised when the user cancels a file move operation."""

    def __init__(self):
        super().__init__("File move operation cancelled by user.")


class FileCopyCancelledError(FileOperationError):
    """Raised when the user cancels a file copy operation."""

    def __init__(self):
        super().__init__("File copy operation cancelled by user.")


class FileDeleteCancelledError(FileOperationError):
    """Raised when the user cancels a file delete operation."""

    def __init__(self):
        super().__init__("File delete operation cancelled by user.")
