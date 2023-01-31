from distutils.command.clean import clean
import PyInstaller.__main__

PyInstaller.__main__.run([
    'lol_a_abp.py',
    '--icon=utils/icon.ico',
    '--onefile',
    '--windowed',
    '--add-data=Champions/*;Champions',
    '--add-data=utils/*;utils',
    '--clean'
])