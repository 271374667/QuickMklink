import shutil
import subprocess

from src.core.paths import LOGO_FILE, OUTPUT_DIR, BIN_DIR, ASSETS_DIR, LOCALE_DIR, ENTRY_PY_FILE

print('start')
command: str = f'nuitka "{ENTRY_PY_FILE}" --standalone --enable-plugin=tk-inter --output-dir="{OUTPUT_DIR}" --windows-icon-from-ico="{LOGO_FILE}" --windows-uac-uiaccess'
print("command:", command)

subprocess.run(command, shell=True)

# 将bin, assets, locale目录复制到输出目录
shutil.copytree(BIN_DIR, OUTPUT_DIR/ 'QuickMklink.dist' / 'bin', dirs_exist_ok=True)
shutil.copytree(ASSETS_DIR, OUTPUT_DIR/ 'QuickMklink.dist' / 'assets', dirs_exist_ok=True)
shutil.copytree(LOCALE_DIR, OUTPUT_DIR/ 'QuickMklink.dist' / 'locale', dirs_exist_ok=True)

print('finished')
