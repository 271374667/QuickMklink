from pathlib import Path

# Path to the root of the project
ROOT = Path(__file__).parent.parent.parent

# Path to the src directory
LOCALE_DIR = ROOT / 'locale'

# Path to the file
CONFIG_FILE = ROOT / 'config.json'
ENTRY_PY_FILE = ROOT / 'QuickMklink.py'

if __name__ == '__main__':
    print(ENTRY_PY_FILE)
