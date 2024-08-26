from tkinter import ttk, Tk, BooleanVar, Checkbutton

from src.core.paths import LOGO_FILE
from src.dialog.message_dialog import MessageDialog
from src.i18n import I18n
from src.settings import ABOUT_TEXT

_ = I18n().trans


class ComboBox(ttk.Combobox):
    @property
    def current_index(self) -> int:
        return self.current()

    @property
    def current_item(self) -> str:
        return self.get()

    @property
    def items(self) -> list[str]:
        return self['values']

    @items.setter
    def items(self, items: list[str]):
        self['values'] = items

    def add_item(self, item: str):
        items = self['values']
        items.append(item)
        self.items = items

    def add_items(self, value: list[str]):
        items = self['values']
        items.extend(value)
        self.items = items

    def remove_item(self, item: str):
        items = self['values']
        items.remove(item)
        self.items = items

    def set_current_item(self, item: str):
        self.set(item)

    def set_current_item_index(self, index: int):
        self.current(index)

    def clear(self):
        self.items = []

    def connect(self, func):
        self.bind('<<ComboboxSelected>>', func)


class ViewMain:
    def __init__(self):
        self._root = Tk()
        self._root.title('QuickMklink')
        self._root.iconbitmap(LOGO_FILE)
        self._root.geometry('280x170')
        self._root.resizable(False, False)

        # Variables
        self.show_cmd_var = BooleanVar(value=False)

        # Widgets
        self.cb_show_cmd = Checkbutton(self._root, text=_('Close command line After Finished?'), variable=self.show_cmd_var,
                                       onvalue=True, offvalue=False)
        self.pb_register_right_click_menu = ttk.Button(self._root, text=_('Register right click menu'))
        self.pb_uninstall_right_click_menu = ttk.Button(self._root, text=_('Uninstall right click menu'))
        self.cb_language = ComboBox(self._root, state='readonly')
        self._lb_language = ttk.Label(self._root, text=_('Language'))
        self._pb_about = ttk.Button(self._root, text=_('About'),
                                    command=lambda: MessageDialog().info(
                                        title=_("About"),
                                        message=ABOUT_TEXT))
        self._pack()

    @property
    def root(self) -> Tk:
        return self._root

    def _pack(self):
        padding = {'padx': 10, 'pady': 10}
        self.cb_show_cmd.pack()
        self.pb_register_right_click_menu.pack()
        self.pb_uninstall_right_click_menu.pack()
        self._lb_language.pack()
        self.cb_language.pack()
        self._pb_about.pack(**padding)


if __name__ == '__main__':
    v = ViewMain()
    v.root.mainloop()
