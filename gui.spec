# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

root_dir = os.path.abspath('.')
scripts_dir = os.path.join(root_dir, 'scripts')

a = Analysis(
    ['scripts\\gui.py'],
    pathex=[scripts_dir],
    binaries=[],
    datas=[('.env', '.')],
    hiddenimports=[
        'main',
        'record_audio',
        'select_device',
        'record_audio',
        'generate_voice',
        'translate',
        'transcribe',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],
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
    name='gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
