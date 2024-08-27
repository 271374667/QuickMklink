from pathlib import Path

from src.core import paths


class Entry:
    @staticmethod
    def get_entry() -> Path:
        result = paths.ROOT / 'QuickMklink.exe'
        pyinstaller_result = paths.ROOT.parent / 'QuickMklink.exe'
        if result.exists():
            return result
        elif pyinstaller_result.exists():
            return pyinstaller_result
        else:
            return paths.ENTRY_PY_FILE


if __name__ == '__main__':
    print(Entry.get_entry())
