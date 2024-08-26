import sys

import loguru

from src.common.entry import Entry
from src.core.paths import LOGO_FILE, COPY_BAT_FILE, MOVE_BAT_FILE
from src.i18n import I18n
from src.utils.context_menu import ContextMenu

_ = I18n().trans


class ContextMenuManager:
    def __init__(self):
        self._copy_text = _('Copy with mklink')
        self._move_text = _('Move with mklink')
        self._paste_text = _('Paste your files here with mklink')

        self._context_menu = ContextMenu()
        self._entry = Entry()

    def setup_right_click_menu(self):
        if not self._context_menu.is_right_click_option_in_dir(self._paste_text):
            if Entry.get_entry().name.endswith('.py'):
                python_exe = sys.executable
                self._context_menu.add_right_click_option_in_dir(self._paste_text,
                                                                 f'"{python_exe}" "{self._entry.get_entry()}" --path "%V"',
                                                                 LOGO_FILE)
            else:
                self._context_menu.add_right_click_option_in_dir(self._paste_text,
                                                                 f'"{self._entry.get_entry()}" --path "%V"',
                                                                 LOGO_FILE)

        if not self._context_menu.is_right_click_option_in_file(self._copy_text):
            self._context_menu.add_right_click_option_in_file(self._copy_text, f'"{COPY_BAT_FILE}" "%1"', LOGO_FILE)

        if not self._context_menu.is_right_click_option_in_file(self._move_text):
            self._context_menu.add_right_click_option_in_file(self._move_text, f'"{MOVE_BAT_FILE}" "%1"', LOGO_FILE)

        loguru.logger.debug('Setup right click menu finished.')

    def uninstallation(self):
        self._context_menu.remove_right_click_option_in_dir(self._paste_text)
        self._context_menu.remove_right_click_option_in_file(self._copy_text)
        self._context_menu.remove_right_click_option_in_file(self._move_text)

        loguru.logger.debug('Uninstallation finished.')


if __name__ == '__main__':
    context_menu_manager = ContextMenuManager()
    # context_menu_manager.setup_right_click_menu()
    context_menu_manager.uninstallation()
