import loguru

from src.utils.clipboard import Clipboard


class ClipboardManager:
    def __init__(self):
        self._clipboard = Clipboard()

    def append_text(self, text: str):
        clipboard_text: str = self._clipboard.get_clipboard_text()
        if clipboard_text.startswith('[QuickMklink'):
            clipboard_text += f'[QuickMklink]{text}[/QuickMklink]'
        else:
            clipboard_text = f'[QuickMklink]{text}[/QuickMklink]'
        self._clipboard.set_clipboard_text(clipboard_text)

    def get_current_text(self) -> str:
        return self._clipboard.get_clipboard_text()

    def clear(self):
        self._clipboard.set_clipboard_text('mklink task finished')
        loguru.logger.debug('Clipboard cleared.')


if __name__ == '__main__':
    cm = ClipboardManager()
    cm.append_text('E:\\load\\python\\Project\\VideoFusion\\assets\\images\\logo.png')
    print(cm.get_current_text())
