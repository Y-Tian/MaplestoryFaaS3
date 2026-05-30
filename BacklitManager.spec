# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

block_cipher = None

# PyInstaller does not define __file__ when executing .spec files.
# Use SPECPATH (injected by PyInstaller) and fall back to current working directory.
project_root = Path(globals().get("SPECPATH", Path.cwd())).resolve()
pic_files = [(str(path), "resources") for path in project_root.joinpath("resources").glob("*.png")]

a = Analysis(
    ["main.py"],
    pathex=[str(project_root)],
    binaries=[],
    datas=pic_files,
    hiddenimports=[
        "comtypes",
        "comtypes.client",
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
    name="BacklitManager",
    debug=False,
    exclude_binaries=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="BacklitManager",
)
