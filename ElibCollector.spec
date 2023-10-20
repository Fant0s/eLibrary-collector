# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:/Users/sasha/Desktop/selenPars/interface.py'],
    pathex=[],
    binaries=[('./driver/chromedriver.exe', './driver')],
    datas=[('C:/Users/sasha/Desktop/selenPars/venv/Lib/site-packages/dotenv', 'dotenv/'), ('C:/Users/sasha/Desktop/selenPars/venv/Lib/site-packages/openpyxl', 'openpyxl/'), ('C:/Users/sasha/Desktop/selenPars/venv/Lib/site-packages/packaging', 'packaging/'), ('C:/Users/sasha/Desktop/selenPars/venv/Lib/site-packages/pandas', 'pandas/'), ('C:/Users/sasha/Desktop/selenPars/venv/Lib/site-packages/requests', 'requests/'), ('C:/Users/sasha/Desktop/selenPars/venv/Lib/site-packages/selenium', 'selenium/'), ('C:/Users/sasha/Desktop/selenPars/venv/Lib/site-packages/selenium_stealth', 'selenium_stealth/'), ('C:/Users/sasha/Desktop/selenPars/venv/Lib/site-packages/tqdm', 'tqdm/'), ('C:/Users/sasha/Desktop/selenPars/venv/Lib/site-packages/webdriver_manager', 'webdriver_manager/')],
    hiddenimports=['pandas', 'openpyxl', 'xlrd', 'http.cookies', 'tqdm'],
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
    name='ElibCollector',
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
    icon=['C:\\Users\\sasha\\Desktop\\selenPars\\icon.ico'],
)
