from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['kivymd.icon_definitions'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
    optimize=0,
)

a.datas += [('fonts/Prompt-Regular.ttf', 'C:\\Users\\u1\\PycharmProjects\\exe_files\\CalcApp\\Prompt-Regular.ttf', 'DATA')]

#kivy
a.datas += [('math.kv', 'C:\\Users\\u1\\PycharmProjects\\exe_files\\CalcApp\math.kv', 'DATA')]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('v', None, 'OPTION')],
    exclude_binaries=True,
    name='main',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app_icon.ico'],
)
coll = COLLECT(
    exe, Tree('C:\\Users\\u1\\PycharmProjects\\exe_files\\CalcApp\\'),
    a.binaries,
    a.datas, *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
