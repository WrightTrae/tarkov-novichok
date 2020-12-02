# -*- mode: python ; coding: utf-8 -*-
from glob import glob

block_cipher = None


a = Analysis(['cli.py'],
             pathex=['C:\\Users\\tdog1\\Desktop\\TarkovNovichok'],
             binaries=[],
             datas=[('C:\\Program Files (x86)\\Tesseract-OCR\\', '.\\Tesseract-OCR\\'), ('.\\maps\\', '.\\maps\\')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [('config.cfg', '.\\config.cfg', "DATA")]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Tarkov Novi',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Tarkov Novi')  