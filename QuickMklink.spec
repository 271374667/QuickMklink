# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['E:/load/python/Project/QuickMklink/QuickMklink.py'],
    pathex=[],
    binaries=[],
    datas=[('E:/load/python/Project/QuickMklink/assets', 'assets/'), ('E:/load/python/Project/QuickMklink/bin', 'bin/'), ('E:/load/python/Project/QuickMklink/locale', 'locale/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='QuickMklink',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon=['E:\\load\\python\\Project\\QuickMklink\\assets\\images\\logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='QuickMklink',
)
