"""
This module provides a `FileController` class that allows for file operations such as moving, copying, and deleting files with a system progress bar on Windows.

Usage
-----

To use the `FileController` class, you need to create an instance of the class and call its methods to perform file operations.

Example:
    ```python
    from src.utils.system import FileController

    fc = FileController()
    fc.move_files_with_progress(r"C:\path\to\source\*", r"C:\path\to\destination")
    fc.copy_files_with_progress(r"C:\path\to\source\*", r"C:\path\to\destination")
    fc.delete_files_with_progress(r"C:\path\to\source\*")
    ```

Classes
-------

FileController
    A class to perform file operations with a system progress bar.

    Methods
    -------
    move_files_with_progress(source: str, destination: str)
        Move files from the source path to the destination path with a system progress bar.

        Args:
            source (str): The source path of the files to be moved.
            destination (str): The destination path where the files should be moved.

    copy_files_with_progress(source: str, destination: str)
        Copy files from the source path to the destination path with a system progress bar.

        Args:
            source (str): The source path of the files to be copied.
            destination (str): The destination path where the files should be copied.

    delete_files_with_progress(source: str)
        Delete files from the source path with a system progress bar.

        Args:
            source (str): The source path of the files to be deleted.

Notes
-----

- This module is designed to work on Windows operating systems.
- Ensure that the source and destination paths are valid and accessible.
- The methods use the `ctypes` library to call Windows API functions for file operations.
- The progress bar is provided by the system and may not be visible in all environments.

"""

import ctypes
import ctypes.wintypes

import loguru


class FileController:
    def __init__(self):
        self._SHFileOperation = ctypes.windll.shell32.SHFileOperationW
        self._FO_MOVE = 0x0001
        self._FO_COPY = 0x0002
        self._FO_DELETE = 0x0003
        self._FOF_NOCONFIRMATION = 0x0010
        self._FOF_NOCONFIRMMKDIR = 0x0200
        self._FOF_NOERRORUI = 0x0400
        self._FOF_SIMPLEPROGRESS = 0x0100

    def _file_operation(self, wFunc, source, destination=None):
        class SHFILEOPSTRUCT(ctypes.Structure):
            _fields_ = [
                ("hwnd", ctypes.wintypes.HWND),
                ("wFunc", ctypes.c_uint),
                ("pFrom", ctypes.c_wchar_p),
                ("pTo", ctypes.c_wchar_p),
                ("fFlags", ctypes.c_short),
                ("fAnyOperationsAborted", ctypes.wintypes.BOOL),
                ("hNameMappings", ctypes.c_void_p),
                ("lpszProgressTitle", ctypes.c_wchar_p)
            ]

        file_op = SHFILEOPSTRUCT()
        file_op.hwnd = None
        file_op.wFunc = wFunc
        file_op.pFrom = source + '\0'
        file_op.pTo = destination + '\0' if destination else None
        file_op.fFlags = self._FOF_NOCONFIRMATION | self._FOF_NOCONFIRMMKDIR | self._FOF_NOERRORUI | self._FOF_SIMPLEPROGRESS
        file_op.fAnyOperationsAborted = False
        file_op.hNameMappings = None
        file_op.lpszProgressTitle = None

        result = self._SHFileOperation(ctypes.byref(file_op))
        if result != 0:
            loguru.logger.error(f"Error: {result}")
        else:
            loguru.logger.success(f"Operation successful: {source} to {destination if destination else 'deleted'}")

    def move_files_with_progress(self, source: str, destination: str):
        """
        Move files with a system progress bar.

        Args:
            source (str): The source path of the files to be moved.
            destination (str): The destination path where the files should be moved.
        """
        self._file_operation(self._FO_MOVE, source, destination)

    def copy_files_with_progress(self, source: str, destination: str):
        """
        Copy files with a system progress bar.

        Args:
            source (str): The source path of the files to be copied.
            destination (str): The destination path where the files should be copied.
        """
        self._file_operation(self._FO_COPY, source, destination)

    def delete_files_with_progress(self, source: str):
        """
        Delete files with a system progress bar.

        Args:
            source (str): The source path of the files to be deleted.
        """
        self._file_operation(self._FO_DELETE, source)


# Example usage
if __name__ == '__main__':
    fc = FileController()
    fc.move_files_with_progress(r"C:\path\to\source\*", r"C:\path\to\destination")
    fc.copy_files_with_progress(r"C:\path\to\source\*", r"C:\path\to\destination")
    fc.delete_files_with_progress(r"C:\path\to\source\*")
