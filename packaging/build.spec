# PyInstaller spec file for packaging BaraChat client

block_cipher = None

a = Analysis(
    ['../client/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../client/gui/qml', 'gui/qml'),  # QML files
        ('../client/assets', 'assets'),     # Assets
    ],
    hiddenimports=[
        'PySide6',
        'aiohttp',
        'websockets',
        'nacl',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BaraChat',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

