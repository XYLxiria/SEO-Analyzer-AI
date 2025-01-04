# testingproduction06.spec
# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

a = Analysis(
    ['Z:\\SKRIPSI\\SEOChecker\\testingproduction06.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('Z:\\SKRIPSI\\SEOChecker\\nltk_data\\corpora\\stopwords', 'nltk_data/corpora/stopwords'),
        ('Z:\\SKRIPSI\\SEOChecker\\nltk_data\\tokenizers\\punkt', 'nltk_data/tokenizers/punkt'),
        ('Z:\\SKRIPSI\\SEOChecker\\nltk_data\\tokenizers\\punkt\\PY3', 'nltk_data/tokenizers/punkt/PY3'),
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AnalisaSEO',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon='Z:\\SKRIPSI\\SEOChecker\\Assets\\favicon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AnalisaSEO',
)
