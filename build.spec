# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['cli.py'],
             pathex=['C:\\Users\\tdog1\\Desktop\\TarkovNovichok'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [('offline.jpg','.\\maps\\offline.jpg', "DATA")]
a.datas += [('reserve.jpg','.\\maps\\reserve.jpg', "DATA")]
a.datas += [('customs.png','.\\maps\\customs.png', "DATA")]
a.datas += [('factory.png','.\\maps\\factory.png', "DATA")]
a.datas += [('interchange.jpg','.\\maps\\interchange.jpg', "DATA")]
a.datas += [('shoreline.png','.\\maps\\shoreline.png', "DATA")]
a.datas += [('woods.png','.\\maps\\woods.png', "DATA")]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Tarkov Novichok',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Tarkov Novichok')
