"""
context_menu.py

This module provides a `ContextMenu` class for managing Windows context menu options.
It allows adding, removing, and checking the existence of context menu options for directories and files.

Usage:
    from context_menu import ContextMenu
    from pathlib import Path

    cm = ContextMenu()
    icon_path = Path(r"C:\path\to\icon.ico")

    # Add a context menu option to directories
    cm.add_right_click_option_in_dir("MyOption", r"notepad.exe", icon_path)

    # Remove a context menu option from directories
    cm.remove_right_click_option_in_dir("MyOption")

    # Add a context menu option to files
    cm.add_right_click_option_in_file("MyOption", r"notepad.exe", icon_path)

    # Remove a context menu option from files
    cm.remove_right_click_option_in_file("MyOption")

    # Check if a context menu option exists in directories
    exists_in_dir = cm.is_right_click_option_in_dir("MyOption")

    # Check if a context menu option exists in files
    exists_in_file = cm.is_right_click_option_in_file("MyOption")

Note:
    - Ensure you have the necessary permissions to modify the Windows registry.
    - Run the script as an administrator to avoid permission errors.
    - The `ico_path` parameter is optional. If provided, it should be a valid path to an icon file.

Examples:
    ```python
    from context_menu import ContextMenu
    from pathlib import Path

    cm = ContextMenu()
    icon_path = Path(r"C:\path\to\icon.ico")

    # Add a context menu option to directories
    cm.add_right_click_option_in_dir("MyOption", r"notepad.exe", icon_path)

    # Check if the option exists
    if cm.is_right_click_option_in_dir("MyOption"):
        print("Option exists in directory context menu.")

    # Remove the context menu option from directories
    cm.remove_right_click_option_in_dir("MyOption")

    # Add a context menu option to files
    cm.add_right_click_option_in_file("MyOption", r"notepad.exe", icon_path)

    # Check if the option exists
    if cm.is_right_click_option_in_file("MyOption"):
        print("Option exists in file context menu.")

    # Remove the context menu option from files
    cm.remove_right_click_option_in_file("MyOption")
    ```

Classes:
    ContextMenu: A class to manage Windows context menu options.

Methods:
    add_right_click_option_in_dir(name: str, command: str, ico_path: Path | None = None) -> bool:
        Adds a new option to the directory context menu.

    add_right_click_option_in_file(name: str, command: str, ico_path: Path | None = None) -> bool:
        Adds a new option to the file context menu.

    remove_right_click_option_in_dir(name: str) -> bool:
        Removes an option from the directory context menu.

    remove_right_click_option_in_file(name: str) -> bool:
        Removes an option from the file context menu.

    is_right_click_option_in_dir(name: str) -> bool:
        Checks if a directory context menu option exists.

    is_right_click_option_in_file(name: str) -> bool:
        Checks if a file context menu option exists.
"""

import winreg as reg
from pathlib import Path

import loguru


class ContextMenu:
    def __init__(self):
        self._dir_shell_key = r'Directory\\Background\\shell'
        self._file_shell_key = r'*\\shell'

    def add_right_click_option_in_dir(self, name: str, command: str, ico_path: Path | None = None) -> bool:
        """Adds a new option to the directory context menu.

        Args:
            name (str): The name of the context menu option.
            command (str): The command to be executed when the option is selected.
            ico_path (Path|None): The path to the icon file for the context menu option.

        Returns:
            bool: True if the option was added successfully, False otherwise.
        """
        key_path = f"{self._dir_shell_key}\\{name}"
        try:
            key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path)
            reg.SetValue(key, '', reg.REG_SZ, name)
            if ico_path is not None and ico_path.exists():
                reg.SetValueEx(key, 'Icon', 0, reg.REG_SZ, str(ico_path))
                loguru.logger.debug(f"Successfully added icon {ico_path} to {name}.")
            command_key = reg.CreateKey(key, 'command')
            reg.SetValue(command_key, '', reg.REG_SZ, command)
            reg.CloseKey(key)
            reg.CloseKey(command_key)
            loguru.logger.debug(f"Successfully added {name} to right-click menu.")
            return True
        except Exception as e:
            loguru.logger.error(f"Failed to add {name} to right-click menu: {e}")
            return False

    def add_right_click_option_in_file(self, name: str, command: str, ico_path: Path | None = None) -> bool:
        """Adds a new option to the file and directory context menu.

        Args:
            name (str): The name of the context menu option.
            command (str): The command to be executed when the option is selected.
            ico_path (Path): The path to the icon file for the context menu option.

        Returns:
            bool: True if the option was added successfully, False otherwise.
        """
        success = True
        key_paths = [f"{self._file_shell_key}\\{name}", f"Directory\\shell\\{name}"]

        for key_path in key_paths:
            try:
                key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path)
                reg.SetValue(key, '', reg.REG_SZ, name)
                if ico_path is not None and ico_path.exists():
                    reg.SetValueEx(key, 'Icon', 0, reg.REG_SZ, str(ico_path))
                    loguru.logger.debug(f"Successfully added icon {ico_path} to {name}.")
                command_key = reg.CreateKey(key, 'command')
                reg.SetValue(command_key, '', reg.REG_SZ, command)
                reg.CloseKey(key)
                reg.CloseKey(command_key)
                loguru.logger.debug(f"Successfully added {name} to right-click menu at {key_path}.")
            except Exception as e:
                loguru.logger.error(f"Failed to add {name} to right-click menu at {key_path}: {e}")
                success = False
        return success

    def remove_right_click_option_in_dir(self, name: str) -> bool:
        """Removes an option from the directory context menu.

        Args:
            name (str): The name of the context menu option to remove.

        Returns:
            bool: True if the option was removed successfully, False otherwise.
        """
        key_path = f"{self._dir_shell_key}\\{name}"
        try:
            reg.DeleteKey(reg.HKEY_CLASSES_ROOT, f"{key_path}\\command")
            reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key_path)
            loguru.logger.debug(f"Successfully removed {name} from right-click menu.")
            return True
        except Exception as e:
            loguru.logger.error(f"Failed to remove {name} from right-click menu: {e}")
            return False

    def remove_right_click_option_in_file(self, name: str) -> bool:
        """Removes an option from the file and directory context menu.

        Args:
            name (str): The name of the context menu option to remove.

        Returns:
            bool: True if the option was removed successfully, False otherwise.
        """
        success = True
        key_paths = [f"{self._file_shell_key}\\{name}", f"Directory\\shell\\{name}"]
        for key_path in key_paths:
            try:
                reg.DeleteKey(reg.HKEY_CLASSES_ROOT, f"{key_path}\\command")
                reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key_path)
                loguru.logger.debug(f"Successfully removed {name} from right-click menu at {key_path}.")
            except Exception as e:
                loguru.logger.error(f"Failed to remove {name} from right-click menu at {key_path}: {e}")
                success = False
        return success

    def is_right_click_option_in_dir(self, name: str) -> bool:
        """Checks if a directory context menu option exists.

        Args:
            name (str): The name of the context menu option.

        Returns:
            bool: True if the option exists, False otherwise.
        """
        key_path = f"{self._dir_shell_key}\\{name}"
        try:
            reg.OpenKey(reg.HKEY_CLASSES_ROOT, key_path)
            return True
        except FileNotFoundError:
            return False

    def is_right_click_option_in_file(self, name: str) -> bool:
        """Checks if a file or directory context menu option exists.

        Args:
            name (str): The name of the context menu option.

        Returns:
            bool: True if the option exists, False otherwise.
        """
        key_paths = [f"{self._file_shell_key}\\{name}", f"Directory\\shell\\{name}"]
        for key_path in key_paths:
            try:
                reg.OpenKey(reg.HKEY_CLASSES_ROOT, key_path)
                return True
            except FileNotFoundError:
                continue
        return False

    def _create_key(self, path: str, sub_key: str) -> reg.HKEYType:
        """Creates a new registry key or opens it if it already exists.

        Args:
            path (str): The registry path where the key will be created.
            sub_key (str): The name of the key to create.

        Returns:
            reg.HKEYType: A handle to the opened registry key.
        """
        return reg.CreateKey(reg.HKEY_CLASSES_ROOT, f"{path}\\{sub_key}")

    def _delete_key(self, path: str, sub_key: str) -> bool:
        """Deletes a registry key.

        Args:
            path (str): The registry path from which the key will be deleted.
            sub_key (str): The name of the key to delete.

        Returns:
            bool: True if the key was deleted successfully, False otherwise.
        """
        try:
            reg.DeleteKey(reg.HKEY_CLASSES_ROOT, f"{path}\\{sub_key}")
            loguru.logger.debug(f"Successfully removed {sub_key} from right-click menu.")
            return True
        except PermissionError:
            loguru.logger.error(
                f"Permission denied: Failed to remove {sub_key} from right-click menu. Please run the script as an administrator.")
            return False
        except FileNotFoundError:
            loguru.logger.error(f"Failed to remove {sub_key} from right-click menu.")
            return False

    def _set_command_and_icon(self, key: reg.HKEYType, command: str, ico_path: Path):
        """Sets the command and icon for the context menu option.

        Args:
            key (reg.HKEYType): The registry key handle where command and icon will be set.
            command (str): The command to execute when the context menu option is selected.
            ico_path (Path): The path to the icon file.
        """
        reg.SetValue(key, "command", reg.REG_SZ, command)
        reg.SetValueEx(key, "Icon", 0, reg.REG_SZ, str(ico_path))


if __name__ == '__main__':
    window_ico_path: Path = Path(r"E:\load\python\Project\VideoFusion\assets\images\logo.ico")
    cm = ContextMenu()
    # cm.add_right_click_option_in_dir("MyCustomOption", r'cmd /c echo "%V" > t.txt', window_ico_path)
    # cm.remove_right_click_option_in_dir("MyCustomOption")
    # cm.add_right_click_option_in_file("MyCustomOption", r"notepad.exe", window_ico_path)
    # cm.add_right_click_option_in_file("MyCustomOption", r'cmd /c echo [QuickMklink]"%1"[/QuickMklink] | clip',
    #                                   window_ico_path)

    # cm.add_right_click_option_in_file("MyCustomOption", r'cmd /c for %i in (%*) do @echo %i >> "%~dp0WritingFilePaths.txt"',
    #                                   window_ico_path)
    cm.remove_right_click_option_in_file("MyCustomOption")
    # print(cm.is_right_click_option_in_file("MyCustomOption"))
    # print(cm.is_right_click_option_in_dir("MyCustomOption"))
