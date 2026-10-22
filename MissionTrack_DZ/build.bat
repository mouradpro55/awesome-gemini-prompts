@echo off
echo Building executable with PyInstaller for Windows...
call venv\Scripts\activate.bat
pyinstaller --noconfirm --onedir --windowed --add-data "Amiri.ttf;." --add-data "templates;templates" --name "MissionTrack_DZ" main.py
echo Build complete. Check the "dist\MissionTrack_DZ" directory.
pause
