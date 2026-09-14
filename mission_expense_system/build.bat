@echo off
echo Building executable with PyInstaller for Windows...
call venv\Scripts\activate.bat
pyinstaller --noconfirm --onedir --windowed --name "MissionExpenseSystem" main.py
echo Build complete. Check the "dist\MissionExpenseSystem" directory.
pause
