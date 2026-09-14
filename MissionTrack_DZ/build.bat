@echo off
echo Building executable with PyInstaller for Windows...
call venv\Scripts\activate.bat
pyinstaller --noconfirm --onedir --windowed --add-data "Amiri.ttf;." --name "MissionTrack" ui_main.py
echo Build complete. Check the "dist\MissionTrack" directory.
pause
