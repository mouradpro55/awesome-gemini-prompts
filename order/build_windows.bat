@echo off
echo ========================================================
echo Building MissionTrack DZ for Windows
echo ========================================================
echo.

echo Installing requirements...
pip install -r requirements.txt

echo.
echo Compiling executable with PyInstaller...
pyinstaller --noconfirm --onedir --windowed --name "MissionTrack_DZ_Modern" --add-data "Amiri.ttf;." --add-data "Template.xlsx;." modern_ui.py

echo.
echo Build complete.
echo You can test the application from dist\MissionTrack_DZ_Modern\MissionTrack_DZ_Modern.exe
pause
