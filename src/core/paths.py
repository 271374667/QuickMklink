from pathlib import Path

# Path to the root of the project
ROOT = Path(__file__).parent.parent.parent

# Path to the src directory
LOCALE_DIR = ROOT / 'locale'
BIN_DIR = ROOT / 'bin'
ASSETS_DIR = ROOT / 'assets'
OUTPUT_DIR = ROOT / 'output'

# Path to the file
LOG_FILE = ROOT / 'QuickMklink.log'
CONFIG_FILE = ROOT / 'config.json'
ENTRY_PY_FILE = ROOT / 'QuickMklink.py'
COPY_BAT_FILE = BIN_DIR / 'copy.bat'
MOVE_BAT_FILE = BIN_DIR / 'move.bat'
LOGO_FILE = ASSETS_DIR / 'images' / 'logo.ico'

if __name__ == '__main__':
    print(MOVE_BAT_FILE)
