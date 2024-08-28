import subprocess
import time

from src.core import paths

command = f'pyinstaller --noconfirm --onedir --console --icon {paths.LOGO_FILE} --clean --uac-admin --add-data "{paths.ASSETS_DIR};assets/" --add-data "{paths.BIN_DIR};bin/" --add-data "{paths.LOCALE_DIR};locale/"  "{paths.ENTRY_PY_FILE}"'
print("command:", command)

start_time = time.time()
subprocess.run(command, shell=True)
print(f'finished, use time: {time.time() - start_time}')
