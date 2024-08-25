from pathlib import Path

from src.core import paths


class Entry:
    @staticmethod
    def get_entry() -> Path:
        result = list(paths.ROOT.glob('*.exe'))
        if result:
            return result[0]
        else:
            return paths.ENTRY_PY_FILE


if __name__ == '__main__':
    print(Entry.get_entry())
