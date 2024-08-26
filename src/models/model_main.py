from src.common.context_menu_manager import ContextMenuManager


class ModelMain:
    def __init__(self):
        self._context_menu_manager = ContextMenuManager()

    def register_right_click_menu(self):
        self._context_menu_manager.setup_right_click_menu()

    def unregister_right_click_menu(self):
        self._context_menu_manager.uninstallation()
